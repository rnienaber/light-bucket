from bottle import request, redirect

class StripSlashesPlugin(object):
  api = 2
  def apply(self, callback, route):
    def wrapper(*args, **kwargs):
      if request.path != '/' and request.path.endswith('/'):
        redirect(request.path.rstrip('/'), 301)
      
      return callback(*args, **kwargs)
    return wrapper
