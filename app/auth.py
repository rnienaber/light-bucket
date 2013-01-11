from xml.dom import minidom
from urllib import urlencode, quote
from datetime import datetime
from urlparse import urlparse

from bottle import request
import requests

from config import config

def redirect_url(request, show_token=False):
  #return url
  parts = request.urlparts
  realm = '{0}://{1}'.format(parts[0], parts[1])
  if show_token:
    return_url = realm + config.admin_show_token_url_path
  else:
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
  claimed_id = request.query.get('openid.claimed_id')
  if not claimed_id: return
    
  parsed_url = urlparse(claimed_id)
  if not parsed_url: return
  
  query = parsed_url.query.split('=')
  if len(query) < 2: return
  
  return query[1]
  
def is_authenticated(request):
  auth_cookie = get_auth_cookie(request)
  if not auth_cookie: return
  return [u for u in config.users if u['id'] == auth_cookie]
  
def set_auth_cookie(request, response):
  open_id = parse_response(request)
  if not open_id: return response
  
  #run through known user ids
  found_users = [u for u in config.users if u['id'] == open_id]
  if not found_users: return response

  cookie_details = {'name': config.auth_cookie_name,
                    'value': open_id,
                    'expires': datetime.today() + config.auth_cookie_timeout,
                    'path': config.landing_page}

  if config.auth_cookie_secret:
    cookie_details['secret'] = config.auth_cookie_secret
  
  response.set_cookie(**cookie_details)
  return response
  
def get_auth_cookie(request):
  secret = config.auth_cookie_secret if config.auth_cookie_secret else None
  return request.get_cookie(config.auth_cookie_name, secret=secret)