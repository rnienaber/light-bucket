from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.models.photo import Photo

class PhotoSyncer(object):
  def __init__(self, database_file, photo_dir, testing=False):
    connect_string = 'sqlite:///' + database_file
    engine = create_engine(connect_string, echo=testing)    
    session = sessionmaker(bind=engine)

    self.Photos = session().query(Photo)

  def all_photos(self):
    return self.Photos.all()

  def fix_folders(self):
    photo =  self.Photos.first()
    r = FOLDER_REGEX.search(photo.folder)
    return ''.join(list(r.groups()) + ['/', photo.filename])


# get timestamps for photos
# get all timestamps for photos from cache
# remove all photos where timestamps are the same as in db
# update photos with different timestamps from db
# regenerate cache
