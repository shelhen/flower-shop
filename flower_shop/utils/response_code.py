# coding:utf-8

class RETCODE:
    OK                  = "0"
    IMAGECODEERR        = "4001"
    THROTTLINGERR       = "4002"
    NECESSARYPARAMERR   = "4003"
    USERERR             = "4004"
    PWDERR              = "4005"
    CPWDERR             = "4006"
    MOBILEERR           = "4007"
    SMSCODERR           = "4008"
    ALLOWERR            = "4009"
    SESSIONERR          = "4101"
    DBERR               = "5000"
    EMAILERR            = "5001"
    TELERR              = "5002"
    NODATAERR           = "5003"
    NEWPWDERR           = "5004"
    OPENIDERR           = "5005"
    PARAMERR            = "5006"
    STOCKERR            = "5007"


err_msg = {
    RETCODE.OK                 : u"成功",
    RETCODE.IMAGECODEERR       : u"图形验证码错误",
    RETCODE.THROTTLINGERR      : u"访问过于频繁",
    RETCODE.NECESSARYPARAMERR  : u"缺少必传参数",
    RETCODE.USERERR            : u"用户名错误",
    RETCODE.PWDERR             : u"密码错误",
    RETCODE.CPWDERR            : u"密码不一致",
    RETCODE.MOBILEERR          : u"手机号错误",
    RETCODE.SMSCODERR          : u"短信验证码有误",
    RETCODE.ALLOWERR           : u"未勾选协议",
    RETCODE.SESSIONERR         : u"用户未登录",
    RETCODE.DBERR              : u"数据错误",
    RETCODE.EMAILERR           : u"邮箱错误",
    RETCODE.TELERR             : u"固定电话错误",
    RETCODE.NODATAERR          : u"无数据",
    RETCODE.NEWPWDERR          : u"新密码数据",
    RETCODE.OPENIDERR          : u"无效的openid",
    RETCODE.PARAMERR           : u"参数错误",
    RETCODE.STOCKERR           : u"库存不足",
}
