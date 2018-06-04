from django.core.exceptions import ValidationError

#自定义密码验证规则

class MyValidtor:
    def __init__(self, upper_num=1):
        self.upper_num = upper_num

    def validate(self, password, user=None):
        temp = []
        for _ in password:
            temp.append(_.isupper())
        if temp.count(True) < self.upper_num:
            raise ValidationError(
                ("密码至少要包含%d个大写字母") % self.upper_num,
                code="password is not",
                arams={"upper_num": self.upper_num}
            )

    def get_help_text(self):
        return "你的密码必须还有 %(upper_num)d 个大写字母" % {"upper_num": self.upper_num}


