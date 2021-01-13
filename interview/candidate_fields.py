# 页面展示字段
default_fieldsets = (
    (None, {'fields': (('username', "gender", "phone"), ("email", "apply_position", "city"), ("major", "degree"),
                       ("bachelor_school", "master_school", "doctor_school"), "candidate_remark",
                       ("paper_score", "test_score_of_general_ability", "last_editor"))}),
    ('第一轮面试记录', {'fields': (
    ("first_score", "first_learning_ability", "first_professional_competency"), "first_advantage", "first_disadvantage",
    ("first_result", "first_recommend_position"), ("first_interviewer_user", "first_remark"))}),
    ('第二轮面试记录', {'fields': ("second_score", ("second_learning_ability", "second_pursue_of_excellence"),
                            ("second_communication_ability", "second_pressure_score"), "second_advantage",
                            "second_disadvantage", ("second_result", "second_recommend_position"),
                            ("second_interviewer_user", "second_remark"))}),
    ('第三轮面试记录', {'fields': (
    ("hr_score", "hr_responsibility", "hr_communication_ability"), ("hr_logic_ability", "hr_potential", "hr_stability"),
    "hr_advantage", "hr_disadvantage", "hr_result", ("hr_interviewer_user", "hr_remark"))}),
)

# 一面面试官需要展示的字段
default_fieldsets_first = (
    (None, {'fields': (('username', "gender", "phone"), ("email", "apply_position", "city"), ("major", "degree"),
                       ("bachelor_school", "master_school", "doctor_school"), "candidate_remark",
                       ("paper_score", "test_score_of_general_ability", "last_editor"))}),
    ('第一轮面试记录', {'fields': (
    ("first_score", "first_learning_ability", "first_professional_competency"), "first_advantage", "first_disadvantage",
    ("first_result", "first_recommend_position"), ("first_interviewer_user", "first_remark"))})
)

# 二面面试官需要展示的字段
default_fieldsets_second = (
    (None, {'fields': (('username', "gender", "phone"), ("email", "apply_position", "city"), ("major", "degree"),
                       ("bachelor_school", "master_school", "doctor_school"), "candidate_remark",
                       ("paper_score", "test_score_of_general_ability", "last_editor"))}),
    ('第二轮面试记录', {'fields': ("second_score", ("second_learning_ability", "second_pursue_of_excellence"),
                            ("second_communication_ability", "second_pressure_score"), "second_advantage",
                            "second_disadvantage", ("second_result", "second_recommend_position"),
                            ("second_interviewer_user", "second_remark"))}),
)
