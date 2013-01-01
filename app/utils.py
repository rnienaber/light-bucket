import os

def get_all_files(file):
  cur_dir = os.path.dirname(file)
  files = [p for p in os.walk(cur_dir).next()[2] if p.endswith('.py')]
  return [os.path.splitext(f)[0] for f in files if '__init__.py' != f]
