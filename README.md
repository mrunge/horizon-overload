horizon-overload
================

Simple script, that fires 1000s of requests against horizon, to see, where 
it breaks.

To use it, create a user and a password and adjust the following values

  ::
    _url = 'http://...'
    _user = 'demo'
    _pass = 'demo'


Please note the missing '/' at the end of the URL. The number of clients
can be adjusted at the bottom in __main__, the same for the
number of requests.

