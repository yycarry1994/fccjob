from django.http import StreamingHttpResponse, HttpResponse
from django.shortcuts import render
import os
from pydocx import PyDocX
from django.conf import settings
from interview.models import Candidate
from django.utils.encoding import escape_uri_path
# Create your views here.


def get_file_content(filename, chunk_size=1024):
    """
    文件读取生成器
    :param filename:
    :param chunk_size:
    :return:
    """
    with open(filename, 'rb') as f:
        while True:
            content = f.read(chunk_size)
            if not content:
                break
            yield content


def read_resume(request, pk):
    instance = Candidate.objects.get(pk=pk)
    file_path = str(instance.resume)
    response = StreamingHttpResponse(get_file_content(file_path))

    # 如果要提高用户下载，必须添加相关的响应头
    # Content-Type
    response['Content-Type'] = 'application/octet-stream'
    # Content-Disposition
    # response['Content-Disposition'] = f"attachment; filename*=UTF-8''{instance.name}"
    response['Content-Disposition'] = f"attachment; filename*=UTF-8''{escape_uri_path(file_path.split('/')[-1])}"

    return response


# def upload_resume(request, pk):
#     instance = Candidate.objects.get(pk=pk)
#     file = request.file.get('resume')
#     instance.resume = file
#     instance.save()
#     return HttpResponse({'msg': '成功'})




# def read_resume(request, pk):
#     instance = Candidate.objects.get(pk=pk)
#     file_path = str(instance.resume)
#     load_html = PyDocX.to_html(file_path)
#     new_doc_html = os.path.join(''.join(file_path.split('/')[:-1]), 'resume.html')
#     with open(new_doc_html, 'w', encoding='utf-8') as file:
#         file.writelines('<meta charset="UTF-8">\n')
#         file.write(load_html)
#     return new_doc_html

