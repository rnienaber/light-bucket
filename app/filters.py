import re
from jinja2 import Environment

_par_re = re.compile(r'\n{2,}')

def nl2p(text):
  result = u'\n'.join(u'<p>%s</p>' % p for p in _par_re.split(text))
  print 'RESULT: ' + result
  return result

#env = Environment()
#env.filters['nl2p'] = nl2p