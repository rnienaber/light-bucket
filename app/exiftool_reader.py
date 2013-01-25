import os
from subprocess import Popen, PIPE
import simplejson as json

from config import config

def get_exif(relative_image_path, tag_list=None):
  return get_exifs(relative_image_path, tag_list).values()[0]

def get_exifs(relative_image_paths, tag_list=None):
  if not isinstance(relative_image_paths, list):
    relative_image_paths = [relative_image_paths]
  
  file_paths = [get_photo_path(config.photo_dir, f) for f in relative_image_paths]

  tags = normalize_tags(tag_list)
  tool_output = get_tags(file_paths)

  abs_len = len(os.path.abspath(config.photo_dir))
  abs_len += 1 if config.photo_dir.startswith('.') else 0

  result = {}
  for info in tool_output:
    file_path = info['SourceFile'].strip(' .')
    relative_file_path = file_path[abs_len:].strip('/')

    keypairs = parse_exif_output(info, tags)
    result[relative_file_path] = keypairs

  return result
  
def update_exif(relative_image_path, tags):
  full_path = os.path.abspath(os.path.join(config.photo_dir, relative_image_path))
  arguments = [full_path, '-overwrite_original_in_place']
  for k in tags.keys():
    key = k.lower()
    argument = ''
    if key == 'comment': argument = 'xpcomment'
    if key == 'keywords': argument = 'xpkeywords'
    if key == 'title': argument = 'xptitle'
    if key == 'subject': argument = 'xpsubject'
    if key == 'person_in_image': argument = 'personinimage'
    
    if argument == '': continue
   
    arguments.append('-{0}={1}'.format(argument, tags[k]))
  
  execute(arguments)

def get_photo_path(photo_dir, relative_image_path):
  file_path = os.path.join(photo_dir, relative_image_path)
  if not os.path.exists(file_path):
    raise IOError("image file '" + file_path + "' doesn't exist")
  return file_path

def normalize_tags(tag_list):
  tags = [] 
  if not tag_list in ['', None]:
    tags = [t.strip().lower() for t in tag_list.split(',')]
  return tags

def get_tags(file_paths):
  switches = r'-j -q -personinimage -gpslatitude -gpslongitude -xpcomment -xpkeywords -xpsubject -createdate -datecreated -xpsubject -xpcomment -xptitle -make -model -c %.8f -d %Y-%m-%dT%H:%M:%S -S'.split(' ')
  all_files = [os.path.abspath(f) for f in file_paths]

  return json.loads(execute(switches + all_files))
    
def execute(arguments):
  command = [config.perl_executable_path, config.exiftool_script_path]

  full_command = command + arguments

  process = Popen(full_command, stdout=PIPE)
  return process.communicate()[0].strip()

def parse_exif_output(info, tags):
  result = {}
  def add_key(exif_tag, processed_tag, processor=None):
      if processed_tag.lower() in tags or tags == []:
          if exif_tag in info:
              value = info[exif_tag]
              processed = processor(value) if processor else value
              result[processed_tag] = processed

  add_key('GPSLongitude', 'longitude', gps_to_decimal)
  add_key('GPSLatitude', 'latitude', gps_to_decimal)
  add_key('XPComment', 'comment')
  add_key('XPKeywords', 'keywords', clean_list)
  add_key('XPTitle', 'title')
  add_key('XPSubject', 'subject')
  add_key('Make', 'make')
  add_key('Model', 'model')
  add_key('DateCreated', 'date')
  add_key('CreateDate', 'date')
  add_key('PersonInImage', 'person_in_image', clean_list)

  return result

def gps_to_decimal(value):
  decimal, direction = value.split(' ') 
  multiplier = -1 if direction in ['W', 'S'] else 1

  return float(decimal) * multiplier

def clean_list(value):
  value_list = value if isinstance(value, list) else value.split(',')
  return ','.join([l.strip() for l in value_list])
