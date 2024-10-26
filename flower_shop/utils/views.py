from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from .response_code import RETCODE


# 重写LoginRequiredMixin，使其返回json数据
class LoginRequiredJSONMixin(LoginRequiredMixin):
    def handle_no_permission(self):
        return JsonResponse({'code': RETCODE.SESSIONERR, 'errmsg': '您未登录'})
