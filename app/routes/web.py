import os
from bottle import route, static_file

from utils import get_summary, view
#placeholder for config that is assigned on startup
from config import config

from models.index import Index
from models.year import Year
from models.month import Month
from models.album import Album


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
  print Year(year).to_view_data()
  return Year(year).to_view_data()

@route('/<filepath:path>')
def server_static(filepath):
  return static_file(filepath, root=config.public_dir)
