from bottle import route, redirect, request, HTTPResponse
from config import config

from app import auth

@route('/login')
def login():
  redirect(auth.redirect_url(request))

@route(config.admin_auth_url_path)
def authenticated():
  res = HTTPResponse("", status=302, Location=config.landing_page)
  return auth.set_auth_cookie(request, res)

@route('/admin/get_token')
def get_token():
  redirect(auth.redirect_url(request, show_token=True))
  
@route(config.admin_show_token_url_path)
def show_token():
  return 'ID: {0}'.format(auth.parse_response(request))
