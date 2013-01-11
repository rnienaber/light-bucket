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
 
  