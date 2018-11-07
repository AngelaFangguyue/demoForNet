# -*- coding: utf-8 -*-

import urllib
import urllib2
import hmac
import hashlib
import base64


# 第一步进行关联（associate）操作
# openid.session_type为DH-SHA1, DH-SHA256, no-encryption
# 使用DH主要是为了在不安全通道中交换密钥，由于我们的服务是走https的，
# 所以这里使用了no-encryption
# 即发起关联只需要以HTTP POST的方式向OpenID Server提交如下固定数据


ASSOCIATE_DATA = {
    'openid.mode': 'associate',
    'openid.assoc_type': 'HMAC-SHA256',  # OpenID消息签名算法，or HAMC-SHA1
    'openid.session_type': 'no-encryption',
}
ASSOCIATE_DATA = urllib.urlencode(ASSOCIATE_DATA)


def check_authentication(request,
                         idp="https://login.netease.com/openid/"):
    """ check_authentication communication """
    check_auth = {}
    is_valid_map = {
        'false': False,
        'true': True,
    }
    request.update({'openid.mode': 'check_authentication'})
    for k, v in request.iteritems():
        if type(v) is unicode:
            request.update({k: v.encode('utf-8')})
    authentication_data = urllib.urlencode(request)
    auth_resp = urllib2.urlopen(idp, authentication_data)
    for line in auth_resp.readlines():
        line = line.strip()
        if not line:
            continue
        k, v = line.split(":", 1)
        check_auth[k] = v

    is_valid = check_auth.get('is_valid', 'false')
    return is_valid_map[is_valid]


def LinkStart(host, returnUrl):
    ASSOC_RESP = urllib2.urlopen('https://login.netease.com/openid/', ASSOCIATE_DATA)
    ASSOC = {}
    # OpenID Server会以行为单位，分别返回如下内容：
    # assoc_handle:{HMAC-SHA256}{5279ff11}{w6nbEA==}
    # expires_in:86400
    # mac_key:g5PWpAb+pbwuTTGDt+95tWKRxN5RAhxDjpqHGwZ2OWw=
    # assoc_type:HMAC-SHA256
    # 这些值需要存储在session或者其它地方，当用户跳转回后，需要使用这些数据校验签名
    for line in ASSOC_RESP.readlines():
        line = line.strip()
        if not line:
            continue
        k, v = line.split(":")
        ASSOC[k] = v

    # 第二步，构造重定向URL，发起请求认证
    #已经associate完成，构造checkid_setup的内容（请求认证）
    REDIRECT_DATA = dict()
    REDIRECT_DATA = {
            'openid.ns': 'http://specs.openid.net/auth/2.0',  # 固定字符串
            'openid.mode': 'checkid_setup',  # 固定字符串
            'openid.assoc_handle': ASSOC['assoc_handle'],  # 第一步获取的assoc_handle值
            #'openid.assoc_handle' : None,
            'openid.return_to': '%s%s' % (host, returnUrl),  # 当用户在OpenID Server登录成功后，你希望它跳转回来的地址
            'openid.claimed_id': 'http://specs.openid.net/auth/2.0/identifier_select',  # 固定字符串
            'openid.identity': 'http://specs.openid.net/auth/2.0/identifier_select',  # 固定字符串
            'openid.realm': '%s/'% (host, ),  # 声明你的身份（站点URL），通常这个URL要能覆盖openid.return_to
            'openid.ns.sreg': 'http://openid.net/extensions/sreg/1.1',  # 固定字符串
            'openid.sreg.required': "nickname,email,fullname",  #,fullname", # 三个可以全部要求获取，或者只要求一个
            # "openid.ns.ax": "http://openid.net/srv/ax/1.0",
            # "openid.ax.mode": "fetch_request",
            # "openid.ax.type.dep": "https://login.netease.com/openid/dep/",
            # "openid.ax.type.dep3": "https://login.netease.com/openid/dep3/",
            # "openid.ax.type.empno": "https://login.netease.com/openid/empno/",
            # "openid.ax.type.title": "https://login.netease.com/openid/title/",
            # "openid.ax.required": "dep,dep3,empno,title",
        }
        
    REDIRECT_DATA = urllib.urlencode(REDIRECT_DATA)

    #实际应用中，需要交由浏览器进行Redirect的URL，用户在这里完成交互认证
    REDIRECT_URL = "https://login.netease.com/openid/?%s" % REDIRECT_DATA

    return REDIRECT_URL, ASSOC


def MyCheck(request, ASSOC):
    try:
        # 第3步，用户成功校验，并跳转至第2步设定的openid.return_to地址
        #做一些基础校验
        if request['openid.mode'] != 'id_res':
            #一定是出错了，成功认证返回的openid.mode一定是id_res
            return False, u"openid.mode 不是 id_res"

        if request['openid.assoc_handle'] != ASSOC['assoc_handle']:
            # 可能consumer没有assoc或者OpenID Server不认可之前的association handle
            # 这种情况下需要做一次check_authentication请求（如果你已经做了associate并且assoc_handle是一致的话
            # 那么不允许做check_authentication操作，一定会返回False ）
            if not check_authentication(request, idp="https://login.netease.com/openid/"):
                return False, u"assoc_handle不一致，check_authentication不成功"
            else:
                ASSOC["checkpass"] = True
                #print u"assoc_handle一致，check_authentication成功"
                #print u"恭喜您，成功完成OpenID认证"
                #print "nickname: %s" % request.GET.get('openid.sreg.nickname', None)
                #print "email: %s" % request.GET.get('openid.sreg.email', None)
                #print "fullname: %s" % request.GET.get('openid.sreg.fullname', None)
                return True, u"恭喜您，成功完成OpenID认证"

        #print u"OpenID Server返回的签名值: %s" % request.GET['openid.sig']
        #构造需要检查签名的内容
        SIGNED_CONTENT = []
        for k in request['openid.signed'].split(","):
            response_data = request["openid.%s" % k]
            SIGNED_CONTENT.append(
                "%s:%s\n" % ( k, response_data ))
        SIGNED_CONTENT = "".join(SIGNED_CONTENT).encode("UTF-8")

        # 使用associate请求获得的mac_key与SIGNED_CONTENT进行assoc_type hash，
        # 检查是否与OpenID Server返回的一致
        SIGNED_CONTENT_SIG = base64.b64encode(
            hmac.new(base64.b64decode(ASSOC['mac_key']),
                     SIGNED_CONTENT, hashlib.sha256).digest())

        #print u"Consumer（本地）计算出来的签名值: %s" % SIGNED_CONTENT_SIG

        if SIGNED_CONTENT_SIG != request['openid.sig']:
            #print u"签名错误，认证不成功"
            return False, u"签名错误，认证不成功"
        else:
            ASSOC["checkpass"] = True
            #print u"恭喜您，成功完成OpenID认证"
            #print "nickname: %s" % request.GET.get('openid.sreg.nickname', None)
            #print "email: %s" % request.GET.get('openid.sreg.email', None)
            #print "fullname: %s" % request.GET.get('openid.sreg.fullname', None)
            return True, u"恭喜您，成功完成OpenID认证"
    except:
        return False, u"验证出错"


class LoginFailed(Exception):pass


class LoginParams(object):

    __slots__ = ["payloads", "session", "redirect", "openid_redirect_to",
                "on_success", "success_args", "netloc", "check_login_func",
                "login_uri"]

    def __init__(self, netloc, 
                    payloads, 
                    session, 
                    login_uri,
                    openid_redirect_to, 
                    on_success,
                    success_args,
                    check_login_func,
                    redirect):
        """
        @params:
            netloc, net location of your web service. eg. `http://mqa.pangu.netease.com:8080`.
            payloads, HTTP GET parameters, for Django, it is `request.GET`. for Flask, it is `request.args`
            session, for Django, it is `request.session`.
            login_uri, path for user to login. eg. `/api/users/login`, or  `/`.
            openid_redirect_to, when openid check pass, path to redirect. eg `/index`.
            on_success, callback function when openid check pass.
            success_args, tuple. 
            check_login_func, function determine whether to login.
            redirect, redirect function supplied by your web framework, for Django, it is `HttpResponseRedirect`
        """
        self.netloc = netloc
        self.payloads = payloads
        self.session = session
        self.login_uri = login_uri
        self.openid_redirect_to = openid_redirect_to
        self.on_success = on_success
        self.success_args = success_args
        self.check_login_func = check_login_func
        self.redirect = redirect


def login(params):
    assert isinstance(params, LoginParams), "invalid params"
    session, redirect = params.session, params.redirect
    uri = params.openid_redirect_to
    if params.check_login_func(session):
        return redirect(uri)
    payloads = params.payloads
    if not payloads.get("openid.sreg.email"):
        _url = payloads.get("url")
        uri = params.login_uri
        url, ASSOC = LinkStart(params.netloc, uri)
        session["ASSOC"] = ASSOC
        if _url:
            session["returnto"] = _url
        return redirect(url)
    else:
        params.on_success(*params.success_args)
        path = session.get("returnto", uri)
        return redirect(path)


__all__ = ["LoginParams", "LoginFailed", "MyCheck"]