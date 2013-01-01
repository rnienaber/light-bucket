import os, sys
import simplejson as json

from simplejson import encoder
encoder.FLOAT_REPR = lambda f: ('%f' % f).rstrip('0').rstrip('.')

def to_json(obj):
   return json.dumps(obj) 
