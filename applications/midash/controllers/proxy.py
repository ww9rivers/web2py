import io, json, types
from contextlib import closing
import requests as http

def streaming(raw):
    '''A wrapper to stream raw response.'''
    def read_raw(self, chunk_size):
        '''Read specified number of bytes from this stream.
        Seems to be only called once.'''
        size = min(chunk_size, self.tell())
        logger.debug('midash/ProxyStream.reading %d(%d) bytes'%(chunk_size, size))
        return self.really_read(size)

    raw.really_read = raw.read
    raw.read = types.MethodType(read_raw, raw)
    return raw


@auth.requires_login()
def index():
    '''Proxy a request to a requested service.

    request.vars['service']     is the name of the service requested.
    request.vars['_url']        is the path and parameters in request.

    Current session is persisted in models/db.
    '''
    response.view = 'splunkview.html'
    return dict()

@auth.requires_login()
def splunk():
    kwargs = dict(verify=False)
    svc = request.get_vars.get('service')
    # Figure out where the service is from app configuration:
    #- For now, assume it's Splunk on the localhost:8001.
    url = 'https://localhost:8001'
    app = request.env.web2py_original_uri
    #
    # If the session exists, cookie(s) may need to be added back.
    #
    #logger.debug('midash/proxy/splunk: web2py session = %s'%(format(session)))
    sess = session.proxy_session
    if sess is None:
        sess = http.Session()
        resp = sess.get(url, **kwargs)
        resp = splunk_auth(sess, url, app, **kwargs)
    sessid = sess.cookies.get('session_id_8001')
    logger.debug('midash/proxy/splunk: request = %s'%format(request))
    kwargs.update(dict(stream=True))
    resp = sess.get(url+app, **kwargs)
    if (sessid != resp.cookies.get('session_id_8001')):
        resp = splunk_auth(sess, url, app=app, **kwargs)
    logger.debug('midash/proxy/splunk: url = "%s" %s)'%(url, format(resp)))
    for hkey,hval in resp.headers.iteritems():
        logger.debug('midash/proxy/splunk: header[%s] = %s'%(hkey, hval))
    #logger.debug('midash/proxy/splunk: content = %s'%(resp.content))
    #
    # Persist the proxy session and proxy target headers:
    #
    session.proxy_session = sess
    response.headers = resp.headers
    response.headers['X-proxy-app'] = app
    #for hkey in [ 'Conten-Type' ]:
    #    hval = resp.headers.get(hkey.lower())
    #    if hval:
    #        response.headers[hkey] = hval
    return response.stream(streaming(resp.raw), request=request)
    response.view = 'proxy.html'
    return dict(content=XML(resp.content))

def splunk_auth(sess, url, app='%2Fen-US%2F', **kwargs):
    '''The session (sess) should have a 'cval' value in its cookies from Splunk.
    '''
    cval = sess.cookies.get('cval')
    uagent = request.env.user_agent
    if uagent:
        sess.headers['User-Agent'] = uagent
    logger.debug('midash/proxy/splunk_auth: cval = %s, app=%s'%(cval, app))
    return sess.post(url+'/en-US/account/login?return_to='+app,
                     data = dict(username='entmon', password='Try1t0ut@', cval = cval),
                     **kwargs)
