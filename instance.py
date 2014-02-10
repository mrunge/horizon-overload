import cookielib
import HTMLParser
import multiprocessing
import random
import urllib
import urllib2


class Loginformparser(HTMLParser.HTMLParser):
    """Parses a csrfmiddlewaretoken from an HTTP request."""

    def __init__(self, *args, **kwargs):
        HTMLParser.HTMLParser.__init__(self, *args, **kwargs)
        self.csrftoken = ""
        self.region = ""

    def handle_starttag(self, tag, attrs):
        if tag == 'input':
            dattrs = dict(attrs)
            if dattrs.get('name', '') == 'csrfmiddlewaretoken':
                self.csrftoken = dattrs.get('value', '')
            if dattrs.get('name', '') == 'region':
                self.region = dattrs.get('value', '')


class Instance(object):
    """Logs into a horizon instance."""

    # _url = 'http://192.168.36.106/dashboard'
    #_url = 'http://192.168.36.112/dashboard'
    _url = 'http://localhost:8000'
    _user = 'demo'
    _pass = 'demo'

    def __init__(self, number, *args, **kwargs):
        super(Instance, self).__init__(*args, **kwargs)
        self.cookiejar = cookielib.CookieJar()
        self.opener = urllib2.build_opener(
            urllib2.HTTPCookieProcessor(self.cookiejar))
        self.number = number

    def login(self):
        """Log in a user."""
        request = self.opener.open(self._url)
        page = request.read()
        p = Loginformparser()
        p.feed(page)
        params = urllib.urlencode({'username': self._user,
                                   'password': self._pass,
                                   'csrfmiddlewaretoken': p.csrftoken,
                                   'region': p.region})
        request = self.opener.open(self._url + '/auth/login/', params)

    def get_anything(self, scope='project', subpage=None):
        """Access subpages within the dashboard

        Attributes:
            * scope: Either project or admin
            * subpage: one of 'instances', 'volumes', ''
            to select an instance, volume or overview
        """

        if scope not in ['project', 'admin']:
            scope = 'project'
        if subpage in ['instances', 'volumes', '', 'images_and_snapshots',
                       'access_and_security', 'network_topology',
                       'networks', 'routers']:
            if subpage is not '':
                subpage += '/'
            url_to_open = self._url + '/' + scope + '/' + subpage
            try:
                request = self.opener.open(url_to_open)
                page = request.read()
            except urllib2.HTTPError:
                print url_to_open

    def logout(self):
        try:
            request = self.opener.open(self._url + '/auth/logout/')
            page = request.read()
        except urllib2.HTTPError:
            print "logout"


class TestCase(multiprocessing.Process):
    """Run a testcase."""
    def __init__(self, num=0, counter=10, *args, **kwargs):
        super(TestCase, self).__init__(*args, **kwargs)
        self.counter = counter
        self.number = num

    def run(self):
        i = Instance(self.number)
        i.login()
        for count in range(counter):
            #scope = random.choice(['project', 'admin'])
            scope = 'project'
            subpage = random.choice(['instances', 'volumes', '',
                                     'images_and_snapshots',
                                     'access_and_security',
                                     'network_topology',
                                     'networks',
                                     'routers'])
            i.get_anything(scope, subpage)
        i.logout()

if __name__ == '__main__':
    counter = 10000
    for num in range(9):
        tc = TestCase(num, counter)
        tc.start()
