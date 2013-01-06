import os
from os import path
import platform
import subprocess
from subprocess import PIPE

class Config(object):
  def __init__(self):
    #url paths
    self.photo_url_path = '/photos'
    self.thumbnail_url_path = '/thumbnails'
    
    #disk paths
    self.app_dir = path.abspath(path.dirname(__file__))
    self.template_path = './app/views'
    self.root_dir = path.dirname(self.app_dir)
    self.public_dir = path.join(self.root_dir, 'public')
    self.photo_dir = path.join(self.public_dir, 'photos')
    self.lib_dir = path.join(self.root_dir, 'lib')

    self.exiftool_path = path.join(self.lib_dir, 'exiftool')
    self.exiftool_script_path = path.join(self.exiftool_path, 'exiftool.pl')
    
    self.metadata_cache_file_name = 'metadata.cache'

    #try and find perl interpreter for exiftool
    if platform.system() == 'Windows':
      if os.path.exists(r'C:\Perl64'):
        self.perl_executable_path = r'C:\Perl64\bin\perl.exe'
      else:
        self.perl_executable_path = r'C:\Perl\bin\perl.exe'
    else:
      output = subprocess.Popen(["whereis", "perl"], stdout=PIPE).communicate()[0]
      matches = [l for l in output.split() if 'bin' in l]
      if not matches:
        raise Exception('Perl interpreter could not be found')
        
      self.perl_executable_path = matches[0]
      
    if not os.path.exists(self.perl_executable_path):
      raise Exception('Perl interpreter could not be found')
      
config = Config()