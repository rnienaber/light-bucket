import os
from bottle import route, static_file, request, redirect

from utils import get_summary, view
from config import config

from models.index import Index
from models.year import Year
from models.month import Month
from models.album import Album
from models.thumbnail import Thumbnail

@route('/')
@view('index')
def index():
  return Index().to_view_data()
  
@route('/<year:re:\d{4}>/<month:re:\d{2}>/<album>')
@view('album')
def album(year, month, album):
  return Album(year, month, album).to_view_data()

@route('/<year:re:\d{4}>/<month:re:\d{2}>')
@view('month')  
def month(year, month):
  return Month(year, month).to_view_data()
  
@route('/<year:re:\d{4}>')
@view('year')  
def year(year):
  return Year(year).to_view_data()
  
@route(config.thumbnail_url_path + '/<filepath:path>')
def service_thumbnail(filepath):
  thumbnail = Thumbnail(filepath)
  thumbnail_path = thumbnail.get_path()
  if config.debug:
    return static_file(thumbnail.get_path(), None)
  else:
    redirect(request.url, 302) #thumbnail has been created, let apache serve

@route('/<filepath:path>')
def serve_static(filepath):
  return static_file(filepath, config.public_dir)
