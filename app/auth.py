from xml.dom import minidom
from urllib import urlencode, quote
from datetime import datetime

import requests

from config import config

def redirect_url(request):
  #return url
  parts = request.urlparts
  realm = '{0}://{1}'.format(parts[0], parts[1])
  return_url = realm + config.admin_auth_url_path  
  
  #get google url
  url = 'https://www.google.com/accounts/o8/id'
  headers = {'Accept': 'application/xrds+xml'}
  r = requests.get(url, headers=headers)
  xrds = minidom.parseString(r.text)
  google_url = xrds.getElementsByTagName('URI')[0].childNodes[0].nodeValue
  
  #redirect url
  params = {'openid.ns': 'http://specs.openid.net/auth/2.0',
            'openid.claimed_id': 'http://specs.openid.net/auth/2.0/identifier_select',
            'openid.identity': 'http://specs.openid.net/auth/2.0/identifier_select',
            'openid.return_to': return_url,
            'openid.realm': realm,
            'openid.mode': 'checkid_setup'}
            
  encoded_values = ((key, quote(params[key], safe="+")) for key in params)
  query_string = "&".join("%s=%s" % v for v in encoded_values)

  return '{0}?{1}'.format(google_url, query_string)
  
def parse_response(request):
  return {'id': request.query['openid.identity']}
  
def set_auth_cookie(request, response):
  cookie_details = {'name': config.auth_cookie_name,
                    'value': parse_response(request)['id'],
                    'expires': datetime.today() + config.auth_cookie_timeout,
                    'path': config.landing_page}

  if config.auth_cookie_secret:
    cookie_details['secret'] = config.auth_cookie_secret
  
  response.set_cookie(**cookie_details)
  return response
  
def get_auth_cookie(request):
  secret = config.auth_cookie_secret if config.auth_cookie_secret else None
  return request.get_cookie(config.auth_cookie_name, secret=secret)  