import csv
from django.contrib import admin, messages
from django.db.models import Q
from django.utils.safestring import mark_safe

from interview.models import Candidate
from django.http.response import HttpResponse

from interview.models import Candidate
from datetime import datetime
from interview import candidate_fields as cf
from interview import dingtalk as dd
from .tasks import send_dingtalk_message

import logging
# Register your models here.
logger = logging.getLogger(__name__)

exportable_fields =(
    'username', 'city', 'phone', 'bachelor_school', 'master_school', 'degree', 'first_result', 'first_interviewer_user',
    'second_result', 'second_interviewer_user', 'hr_result', 'hr_score', 'hr_remark', 'hr_interviewer_user'
)


def export_model_as_csv(modeladmin, request, queryset):
    response = HttpResponse(content_type='text/csv')
    field_list = exportable_fields
    response['Content-Disposition'] = 'attachment; filename=%s-list-%s.csv' % (
        'recruitment-candidates',
        datetime.now().strftime('%Y-%m-%d-%H-%M-%S'),
    )

    # 写入表头
    writer = csv.writer(response)
    writer.writerow(
        [queryset.model._meta.get_field(f).verbose_name.title() for f in field_list]
    )

    for obj in queryset:
        # 单行记录（各个字段的值），写入到csv文件中
        csv_line_list = []
        for field in field_list:
            field_obj = queryset.model._meta.get_field(field)
            field_value = field_obj.value_from_object(obj)
            csv_line_list.append(field_value)
        writer.writerow(csv_line_list)

    logger.info("{} 导出了{}条数据记录".format(request.user, len(queryset)))

    return response


export_model_as_csv.short_description = u'导出为CSV文件'
export_model_as_csv.allowed_permissions = ('export', )


def notify_interviewer(request, queryset, interviewer):
    candidates = ""
    interviewers = []
    for obj in queryset:
        candidates = obj.username + ";" + candidates
        if interviewer == "first_interviewer_user":
            interviewers.append(obj.first_interviewer_user.username)
        elif interviewer == "second_interviewer_user":
            interviewers.append(obj.second_interviewer_user.username)
        else:
            logger.error("程序错误")
    # 这里的消息发送到钉钉， 或者通过 Celery 异步发送到钉钉
    # send ("候选人 %s 进入面试环节，亲爱的面试官，请准备好面试： %s" % (candidates, interviewers))
    interviewers = "; ".join(list(set(interviewers)))
    send_dingtalk_message.delay("候选人 %s 进入面试环节，亲爱的面试官，请准备好面试： %s" % (candidates, interviewers))
    messages.add_message(request, messages.INFO, '已经成功发送面试通知')


def notify_interviewer_first(modeladmin, request, queryset):
    interviewer = "first_interviewer_user"
    notify_interviewer(request, queryset, interviewer)


def notify_interviewer_second(modeladmin, request, queryset):
    interviewer = "second_interviewer_user"
    notify_interviewer(request, queryset, interviewer)


notify_interviewer_first.short_description = u'通知一面面试官'
notify_interviewer_second.short_description = u'通知二面面试官'


# # 通知一面面试官面试
# def notify_interviewer(modeladmin, request, queryset):
#     candidates = ""
#     interviewers = ""
#     for obj in queryset:
#         candidates = obj.username + ";" + candidates
#         interviewers = obj.first_interviewer_user.username + ";" + interviewers
#     # 这里的消息发送到钉钉， 或者通过 Celery 异步发送到钉钉
#     #send ("候选人 %s 进入面试环节，亲爱的面试官，请准备好面试： %s" % (candidates, interviewers) )
#     send_dingtalk_message.delay("候选人 %s 进入面试环节，亲爱的面试官，请准备好面试： %s" % (candidates, interviewers) )
#     messages.add_message(request, messages.INFO, '已经成功发送面试通知')
#
#
# notify_interviewer.short_description = u'通知一面面试官'


class CandidateAdmin(admin.ModelAdmin):
    exclude = ('userid', 'creator', 'created_date', 'modified_date')

    # 表单展示字段
    list_display = (
        'username', 'get_resume', 'city', 'bachelor_school', 'first_score', 'first_result',
        'first_interviewer_user', 'second_result', 'second_interviewer_user',
        'hr_score', 'hr_result', 'hr_interviewer_user', 'last_editor'
    )

    # 搜索字段
    search_fields = ('username', 'phone', 'bachelor_school', 'city')

    # 表单筛选字段
    list_filter = ('city', 'first_result', 'second_result', 'hr_result', 'first_interviewer_user',
                   'second_interviewer_user', 'hr_interviewer_user')

    # 对于表单数据可以操作action
    actions = (export_model_as_csv, notify_interviewer_first, notify_interviewer_second)
    # actions = (export_model_as_csv, notify_interviewer, )

    # 检验用户是否拥有导出权限
    def has_export_permission(self, request):
        opts = self.opts
        return request.user.has_perm("{}.{}".format(opts.app_label, "export"))

    # 查看简历
    def get_resume(self, obj):
        if not obj.resume:
            return None
        return mark_safe(u'<a href="/resume/%s" target="_blank">%s</a' % (obj.id, str(obj.resume).split('/')[-1]))

    # def upload_resume(self, obj):
    #     return mark_safe(u'<form action="/upload/resume/%s/" method="post" enctype="multipart/form-data"><input '
    #                      u'type="file" name="resume"/><input type="submit"/></form>' % obj.id)

    # 对于数据详情页对于不同用户展示不同内容
    def get_fieldsets(self, request, obj=None):
        group_names = self.get_group_names(request.user)

        if "interviewer" in group_names and obj.first_interviewer_user == request.user:
            return cf.default_fieldsets_first
        elif "interviewer" in group_names and obj.first_interviewer_user == request.user:
            return cf.default_fieldsets_second
        else:
            return cf.default_fieldsets

    # 重写get_queryset方法，实现数据集权限控制
    def get_queryset(self, request):
        group_names = self.get_group_names(request.user)

        if request.user.is_superuser or 'hr_user' in group_names:
            return super().get_queryset(request)
        return Candidate.objects.filter(
            Q(first_interviewer_user=request.user) | Q(second_interviewer_user=request.user)
        )

    # 获取登录用户所属那个group
    def get_group_names(self, user):
        group_names = []
        for g in user.groups.all():
            group_names.append(g.name)
        return group_names

    # readonly_fields = ('first_interviewer_user', 'second_interviewer_user', 'hr_interviewer_user',)
    # 只读字段（详情页不能编辑，根据登录用户权限决定）
    def get_readonly_fields(self, request, obj=None):
        group_names = self.get_group_names(request.user)
        read_only_fields = ()

        if 'interviewer' in group_names:
            logger.info("interviewer is in user's group for {}".format(request.user.username))
            read_only_fields = ('first_interviewer_user', 'second_interviewer_user', 'hr_interviewer_user',)
        return read_only_fields

    # list_editable = ('first_interviewer_user','second_interviewer_user',)
    # 定义在表单页面即可直接编辑的字段
    def get_list_editabe(self, request):
        group_names = self.get_group_names(request.user)

        if request.user.is_superuser or 'hr_user' in group_names:
            return ('first_interviewer_user','second_interviewer_user',)
        return ()

    # get_list_editabe需要在父类的get_changelist_instance方法中改变
    def get_changelist_instance(self, request):
        """
        override admin method and list_editable property value
        with values returned by our custom method implementation.
        """
        self.list_editable = self.get_list_editabe(request)
        return super().get_changelist_instance(request)


admin.site.register(Candidate, CandidateAdmin)