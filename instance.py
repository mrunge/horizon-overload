import cookielib
import urllib
import urllib2

class Instance(object):
    """Logs into a horizon instance."""

    _url = 'http://localhost/dashboard'
    _user = 'admin'
    _pass = 'admin'

    def __init__(self):
        self.cookiejar=cookielib.CookieJar()
        self.opener=urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cookiejar))
    
    def login(self):
        request = self.opener.open(self._url)
        params = urllib.urlencode({'uername':self._user, 
            'password': self._pass})
        request = self.opener.open(self._url,params)
        print request

if __name__=='__main__':
    i=Instance()
    i.login()
