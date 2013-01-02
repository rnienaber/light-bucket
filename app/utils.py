import os
import bottle
import yaml

def get_all_files(file):
  cur_dir = os.path.dirname(file)
  files = [p for p in os.walk(cur_dir).next()[2] if p.endswith('.py')]
  return [os.path.splitext(f)[0] for f in files if '__init__.py' != f]
  
def get_summary(dir):
  summary_path = os.path.join(dir, 'summary.yaml')
  if not os.path.exists(summary_path):
    return {}
    
  with open(summary_path, 'r') as summary_file:
    return yaml.safe_load(summary_file)
    


