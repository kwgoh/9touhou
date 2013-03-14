import os
import urllib
import webapp2
import datetime

from google.appengine.ext import blobstore
from google.appengine.api import memcache
from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.ext.webapp.util import run_wsgi_app

import json

class MainHandler(webapp2.RequestHandler):
  def get(self):
    upload_url = blobstore.create_upload_url('/upload')

class BlobData(db.Model):
  file_name = db.StringProperty(required=True)
  file_desc = db.StringProperty()
  file_date = db.DateTimeProperty(auto_now_add=True)
  file_owner = db.StringProperty()
  file_blob_key = db.StringProperty(required=True)
  
  def to_dict(self):
       d = dict([(p, unicode(getattr(self, p))) for p in self.properties()])
       d["id"] = self.key().id()
       return d

            
  @staticmethod
  def get_entities():
    #update ModelCount when adding
    theQuery = BlobData.all()

    objects = theQuery.run()

    entities = []
    for object in objects:
      entity = {'f_name': object.file_name,
              'f_desc': object.file_desc,
              'f_date': object.file_date,
              'f_owner': object.file_owner,
              'f_blob': object.file_blob_key}
      entities.append(entity)
    result = {'method':'get_entities',
              'en_type': 'Blob',
              'entities': entities}       
    return result  

class SongData(db.Model):
  song_name = db.StringProperty(required=True,default='Unknown')
  song_composer = db.StringProperty(required=True,default='Unknown')
  song_details = db.StringProperty()
  song_date = db.DateTimeProperty(auto_now_add=True)
  song_upload_by = db.StringProperty()
  song_blob_key = db.StringProperty(required=True)
  
  def to_dict(self):
       d = dict([(p, unicode(getattr(self, p))) for p in self.properties()])
       d["id"] = self.key().id()
       return d

            
  @staticmethod
  def get_entities():
    #update ModelCount when adding
    theQuery = SongData.all()

    objects = theQuery.run()

    entities = []
    for object in objects:
      entity = {'s_name': object.song_name,
              's_comp': object.song_composer,
              's_details': object.song_details,
              's_date': object.song_date,
              's_uploadby': object.song_upload_by,
              's_blob': object.song_blob_key}
      entities.append(entity)
    result = {'method':'get_entities',
              'en_type': 'Song',
              'entities': entities}       
    return result
    
class User(db.Model):
  user_name = db.StringProperty(required=True)
  user_password = db.StringProperty(required=True)
  user_isadmin = db.BooleanProperty(required=True)
  #user_points = db.IntegerProperty(required=True)
  #user_isplayer = db.BooleanProperty(required=True)
  
  def to_dict(self):
       d = dict([(p, unicode(getattr(self, p))) for p in self.properties()])
       d["id"] = self.key().id()
       return d

            
  @staticmethod
  def add(data):
     
    jsonData = json.loads(data)
    entity = User(user_name=jsonData['u_name'],
                    user_password=jsonData['u_pwd'],
                    user_isadmin=bool(False))
    
    entity.put()
    
    result = {'u_name':jsonData['u_name'],
              'u_admin': bool(False)}
        
    return result
    
  @staticmethod
  def get_entity(model_id):
    theobject = User.get_by_id(int(model_id))
    
    result = {'u_name':theobject.user_name,
              'u_admin': theobject.user_isadmin}
    return result
    
  @staticmethod
  def clear():
    count = 0
    for object in User.all():
      count += 1
      object.delete()
    
    result = {'items_deleted': count}
    return result
  
  #You can't name it delete since db.Model already has a delete method
  @staticmethod
  def remove(model_id):
    #update model count when deleting
    entity = User.get_by_id(int(model_id))
    
    if entity:
        entity.delete()
    
        result = {'method':'delete_model_success',
                  'id': model_id
                  }
    else:
        result = {'method':'delete_model_not_found'}
    
    return result

  #data is a dictionary that must be merged with current json data and stored. 
  @staticmethod
  def edit_entity(model_id, data):
    jsonData = json.loads(data)
    entity = User.get_by_id(int(model_id))
    
    if jsonData['u_name']!='':
      entity.user_name=jsonData['u_name']
    if jsonData['u_pwd']!='':
      entity.user_password=jsonData['u_pwd']
    if jsonData['u_admin']!='':
      entity.user_isadmin=jsonData['u_admin']
    entity.put()
    
    result = {'id': entity.key().id(), 
              'data': json.dumps(jsonData)
              }
    return result

class Challenge_Songs(db.Model):
  challenge_id = db.IntegerProperty(required=True,default=0)
  song_name = db.StringProperty(required=True,default="")
  difficulty = db.StringProperty(required=True,default="Basic")
    
class Challenge(db.Model):
  challenge_name = db.StringProperty(required=True)
  challenge_description = db.StringProperty()
  challenge_admin_notes = db.StringProperty()
  challenge_date = db.DateTimeProperty(auto_now_add=True)
  challenge_expiry = db.DateTimeProperty()
  
  def to_dict(self):
       d = dict([(p, unicode(getattr(self, p))) for p in self.properties()])
       d["id"] = self.key().id()
       return d

            
  @staticmethod
  def add(data):
     
    jsonData = json.loads(data)
    entity = Challenge(challenge_name=jsonData['c_name'],
                    challenge_description=jsonData['c_desc'],
                    challenge_admin_notes=jsonData['c_notes'],
                    challenge_expiry=jsonData['c_date'])
    
    entity.put()
    
    challengeSongs = jsonData['c_songs'];
    count = 0
    for i in range(len(challengeSongs)):
      csData = challengeSongs[i]
      csong = Challenge_Songs(challenge_id=entity.key().id(),
                    song_name=csData['s_name'],
                    difficulty=csData['s_difficulty'])
      csong.put()
      count = count + 1
    result = {'c_name': jsonData['c_name'],
              'c_desc': jsonData['c_desc'],
              'c_notes': jsonData['c_notes'],
              'c_date': jsonData['c_date'],
              'c_blob': jsonData['c_blob'],
              'c_songs_count': count}
        
    return result
  
  @staticmethod
  def get_entities():
    #update ModelCount when adding

    theQuery = Challenge.all()

    objects = theQuery.run()

    entities = []
    for object in objects:
      c_songs_query = Challenge_Songs.all().filter('challenge_id', object.key().id()).run()
      
      c_songs = []
      
      if c_songs_query:
        for c_s in c_songs_query:
          c_song_blob = ""
          c_song_data = SongData.all().filter('song_name',c_s.song_name).get()
          if c_song_data:
            c_song_blob = c_song_data.song_blob_key
          c_entity = {'s_name': c_s.song_name,
                's_difficulty': c_s.difficulty,
                's_blob': c_song_blob}
          c_songs.append(c_entity)
      
      entity = {'c_name': object.challenge_name,
              'c_desc': object.challenge_description,
              'c_notes': object.challenge_admin_notes,
              'c_date': object.challenge_expiry,
              'c_songs': c_songs}
      entities.append(entity)
    result = {'method':'get_entities',
              'en_type': 'Challenge',
              'entities': entities}       
    return result
    
  @staticmethod
  def get_entity(model_id):
    theobject = Challenge.get_by_id(int(model_id))
    
    c_songs_query = Challenge_Songs.all().filter('challenge_id', theobject.key().id()).run()
    
    c_songs = []
    
    if c_songs_query:
      for c_s in c_songs_query:
        c_song_blob = ""
        c_song_data = SongData.all().filter('song_name',c_s.song_name).get()
        if c_song_data:
          c_song_blob = c_song_data.song_blob_key
        c_entity = {'s_name': c_s.song_name,
              's_difficulty': c_s.difficulty,
              's_blob': c_song_blob}
        c_songs.append(c_entity)
      
    result = {'c_name': theobject.challenge_name,
              'c_desc': theobject.challenge_description,
              'c_notes': theobject.challenge_admin_notes,
              'c_date': object.challenge_expiry,
              'c_songs': c_songs}
    return result
    
  @staticmethod
  def clear():
    count = 0
    for object in Challenge.all():
      count += 1
      object.delete()
    
    result = {'items_deleted': count}
    return result
  
  #You can't name it delete since db.Model already has a delete method
  @staticmethod
  def remove(model_id):
    #update model count when deleting
    entity = Challenge.get_by_id(int(model_id))
    
    if entity:
        entity.delete()
    
        result = {'method':'delete_model_success',
                  'id': model_id
                  }
    else:
        result = {'method':'delete_model_not_found'}
    
    return result

  #data is a dictionary that must be merged with current json data and stored. 
  @staticmethod
  def edit_entity(model_id, data):
    jsonData = json.loads(data)
    entity = Challenge.get_by_id(int(model_id))
    
    if jsonData['c_name']!='':
      entity.challenge_name=jsonData['c_name']
    if jsonData['c_desc']!='':
      entity.challenge_description=jsonData['c_desc']
    if jsonData['c_date']!='':
      entity.challenge_expiry=jsonData['c_date']
    if jsonData['c_notes']!='':
      entity.challenge_admin_notes=jsonData['c_notes']
    if jsonData['c_blob']!='':
      entity.challenge_blob_key=jsonData['c_blob']	  
    entity.put()

    result = {'id': entity.key().id(), 
              'data': json.dumps(jsonData)
              }
    return result
    
class BlobFormHandler(webapp2.RequestHandler):
  def get(self):
    upload_url = blobstore.create_upload_url('/file/upload')
    self.response.out.write('<html ng-app="myApp"><body ng-controller="FirstController"><link href="app/css/bootstrap.css" rel="stylesheet">')
    self.response.out.write('<script src="app/lib/angular/angular.min.js"></script>')
    self.response.out.write('<script src="app/lib/angular/angular-resource.min.js"></script>')
    self.response.out.write('<script src="app/js/controllers.js"></script>')
    self.response.out.write('<script src="app/js/app.js"></script>')
    self.response.out.write('<script src="test/lib/angular/angular-mocks.js"></script>')
    self.response.out.write('<form action="%s" method="POST" enctype="multipart/form-data">' % upload_url)
    self.response.out.write("""Name of file:<br> <input type="text" name="filename"><br> Description:<br> <input type="text" name="filedescription"><br><hr/> Upload File: <input type="file" name="file"><br> Uploaded By:<br> <input type="text" name="fileowner" ng-model="name" disabled> <input type="submit" name="submit" value="Submit"> </form></body></html>""")

class UploadHandler(blobstore_handlers.BlobstoreUploadHandler):
  def post(self):
    upload_files = self.get_uploads('file')  # 'file' is file upload field in the form
    f_name = self.request.POST.get('filename')
    f_desc = self.request.POST.get('filedescription')
    f_owner = self.request.POST.get('fileowner')
    blob_info = upload_files[0]
    
    try:
        b = BlobData(file_name=f_name,
             file_desc=f_desc,
             file_owner=f_owner,
             file_blob_key=str(blob_info.key()))
        b.date = datetime.datetime.now().date()
        b.put()
    
        #self.redirect('/file/serve/%s' % blob_info.key())
    except BadValueError:
        print "Error in uploading file!"
    #$self.response.out.write(blob_info.key());

class ServeHandler(blobstore_handlers.BlobstoreDownloadHandler):
  def get(self, resource):
    resource = str(urllib.unquote(resource))
    blob_info = blobstore.BlobInfo.get(resource)
    self.send_blob(blob_info)

class ListBlobHandler(webapp2.RequestHandler):
  def respond(self,result):
    """Returns a JSON response to the client.
    """
    callback = self.request.get('callback')
    self.response.headers['Content-Type'] = 'application/json'
    #self.response.headers['Content-Type'] = '%s; charset=%s' % (config.CONTENT_TYPE, config.CHARSET)
    self.response.headers['Access-Control-Allow-Origin'] = '*'
    self.response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS, PATCH, HEAD'
    self.response.headers['Access-Control-Allow-Headers'] = 'Origin, Content-Type, X-Requested-With'
    self.response.headers['Access-Control-Allow-Credentials'] = 'True'

    #Add a handler to automatically convert datetimes to ISO 8601 strings. 
    dthandler = lambda obj: obj.isoformat() if isinstance(obj, datetime.datetime) else None
    if callback:
      content = str(callback) + '(' + json.dumps(result,default=dthandler) + ')'
      return self.response.out.write(content)
        
    return self.response.out.write(json.dumps(result,default=dthandler))
        
  def get(self):
    result = BlobData.get_entities()
    
    return self.respond(result)

class SongFormHandler(webapp2.RequestHandler):
  def get(self):
    upload_url = blobstore.create_upload_url('/file/songupload')
    self.response.out.write('<html ng-app="myApp"><body ng-controller="FirstController"><link href="app/css/bootstrap.css" rel="stylesheet">')
    self.response.out.write('<script src="app/lib/angular/angular.min.js"></script>')
    self.response.out.write('<script src="app/lib/angular/angular-resource.min.js"></script>')
    self.response.out.write('<script src="app/js/controllers.js"></script>')
    self.response.out.write('<script src="app/js/app.js"></script>')
    self.response.out.write('<script src="test/lib/angular/angular-mocks.js"></script>')
    self.response.out.write('<form action="%s" method="POST" enctype="multipart/form-data">' % upload_url)
    self.response.out.write("""Name of Song<br> <input type="text" name="s_name"><br> Composer<br> <input type="text" name="s_comp"><br> Song Details<br> <input type="text" name="s_details"><br> Uploaded By<br> <input type="text" name="s_uploadby" ng-model="name" disabled><br> Upload File: <input type="file" name="song"><br><input type="submit" name="submit" value="Submit"> </form></body></html>""")


class SongUploadHandler(blobstore_handlers.BlobstoreUploadHandler):
  def post(self):
    upload_song = self.get_uploads('song')  # 'file' is file upload field in the form
    s_name = self.request.POST.get('s_name')
    s_comp = self.request.POST.get('s_comp')
    s_details = self.request.POST.get('s_details')
    s_uploadby = self.request.POST.get('s_uploadby')
    blob_info = upload_song[0]
    
    try:
        s = SongData(song_name=s_name,
             song_composer=s_comp,
             song_details=s_details,
             song_upload_by=s_uploadby,
             song_blob_key=str(blob_info.key()))
        s.date = datetime.datetime.now().date()
        s.put()
    
        #self.redirect('/file/serve/%s' % blob_info.key())
    except BadValueError:
        print "Error in uploading song!"
    #$self.response.out.write(blob_info.key());

class LoginHandler(webapp2.RequestHandler):
  def respond(self,result):
    """Returns a JSON response to the client.
    """
    callback = self.request.get('callback')
    self.response.headers['Content-Type'] = 'application/json'
    #self.response.headers['Content-Type'] = '%s; charset=%s' % (config.CONTENT_TYPE, config.CHARSET)
    self.response.headers['Access-Control-Allow-Origin'] = '*'
    self.response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS, PATCH, HEAD'
    self.response.headers['Access-Control-Allow-Headers'] = 'Origin, Content-Type, X-Requested-With'
    self.response.headers['Access-Control-Allow-Credentials'] = 'True'

    #Add a handler to automatically convert datetimes to ISO 8601 strings. 
    dthandler = lambda obj: obj.isoformat() if isinstance(obj, datetime.datetime) else None
    if callback:
      content = str(callback) + '(' + json.dumps(result,default=dthandler) + ')'
      return self.response.out.write(content)
        
    return self.response.out.write(json.dumps(result,default=dthandler))
        
  def post(self):
    jsonData = json.loads(self.request.body)
    # Query interface constructs a query using instance methods
    q = User.all()
    objects = q.run()
    result = {'error':'Invalid Username/Password!'}  
    for object in objects:
      if jsonData['u_name']==object.user_name:
        if jsonData['u_pwd']==object.user_password:
          result = {'u_name':object.user_name,
              'u_admin': object.user_isadmin}
              
    return self.respond(result)

class RegisterHandler(webapp2.RequestHandler):
  def respond(self,result):
    """Returns a JSON response to the client.
    """
    callback = self.request.get('callback')
    self.response.headers['Content-Type'] = 'application/json'
    #self.response.headers['Content-Type'] = '%s; charset=%s' % (config.CONTENT_TYPE, config.CHARSET)
    self.response.headers['Access-Control-Allow-Origin'] = '*'
    self.response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS, PATCH, HEAD'
    self.response.headers['Access-Control-Allow-Headers'] = 'Origin, Content-Type, X-Requested-With'
    self.response.headers['Access-Control-Allow-Credentials'] = 'True'

    #Add a handler to automatically convert datetimes to ISO 8601 strings. 
    dthandler = lambda obj: obj.isoformat() if isinstance(obj, datetime.datetime) else None
    if callback:
      content = str(callback) + '(' + json.dumps(result,default=dthandler) + ')'
      return self.response.out.write(content)
        
    return self.response.out.write(json.dumps(result,default=dthandler))
        
  def post(self):
    jsonData = json.loads(self.request.body)
    # Query interface constructs a query using instance methods
    q = User.all()
    objects = q.run()
    
    valid = 1
    result = {'error':'Username already exists!'}    
    for object in objects:
      if jsonData['u_name']==object.user_name:
        valid = 0
    
    if valid == 1:
      result = User.add(json.dumps(jsonData))
    
    return self.respond(result)

class CreateChallengeHandler(webapp2.RequestHandler):
  def respond(self,result):
    """Returns a JSON response to the client.
    """
    callback = self.request.get('callback')
    self.response.headers['Content-Type'] = 'application/json'
    #self.response.headers['Content-Type'] = '%s; charset=%s' % (config.CONTENT_TYPE, config.CHARSET)
    self.response.headers['Access-Control-Allow-Origin'] = '*'
    self.response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS, PATCH, HEAD'
    self.response.headers['Access-Control-Allow-Headers'] = 'Origin, Content-Type, X-Requested-With'
    self.response.headers['Access-Control-Allow-Credentials'] = 'True'

    #Add a handler to automatically convert datetimes to ISO 8601 strings. 
    dthandler = lambda obj: obj.isoformat() if isinstance(obj, datetime.datetime) else None
    if callback:
      content = str(callback) + '(' + json.dumps(result,default=dthandler) + ')'
      return self.response.out.write(content)
        
    return self.response.out.write(json.dumps(result,default=dthandler))
        
  def post(self):
    jsonData = json.loads(self.request.body)
    result = Challenge.add(json.dumps(jsonData))
    
    return self.respond(result)

class ListChallengeHandler(webapp2.RequestHandler):
  def respond(self,result):
    """Returns a JSON response to the client.
    """
    callback = self.request.get('callback')
    self.response.headers['Content-Type'] = 'application/json'
    #self.response.headers['Content-Type'] = '%s; charset=%s' % (config.CONTENT_TYPE, config.CHARSET)
    self.response.headers['Access-Control-Allow-Origin'] = '*'
    self.response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS, PATCH, HEAD'
    self.response.headers['Access-Control-Allow-Headers'] = 'Origin, Content-Type, X-Requested-With'
    self.response.headers['Access-Control-Allow-Credentials'] = 'True'

    #Add a handler to automatically convert datetimes to ISO 8601 strings. 
    dthandler = lambda obj: obj.isoformat() if isinstance(obj, datetime.datetime) else None
    if callback:
      content = str(callback) + '(' + json.dumps(result,default=dthandler) + ')'
      return self.response.out.write(content)
        
    return self.response.out.write(json.dumps(result,default=dthandler))
        
  def get(self):
    result = Challenge.get_entities()
    
    return self.respond(result)
    
class ListSongsHandler(webapp2.RequestHandler):
  def respond(self,result):
    """Returns a JSON response to the client.
    """
    callback = self.request.get('callback')
    self.response.headers['Content-Type'] = 'application/json'
    #self.response.headers['Content-Type'] = '%s; charset=%s' % (config.CONTENT_TYPE, config.CHARSET)
    self.response.headers['Access-Control-Allow-Origin'] = '*'
    self.response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS, PATCH, HEAD'
    self.response.headers['Access-Control-Allow-Headers'] = 'Origin, Content-Type, X-Requested-With'
    self.response.headers['Access-Control-Allow-Credentials'] = 'True'

    #Add a handler to automatically convert datetimes to ISO 8601 strings. 
    dthandler = lambda obj: obj.isoformat() if isinstance(obj, datetime.datetime) else None
    if callback:
      content = str(callback) + '(' + json.dumps(result,default=dthandler) + ')'
      return self.response.out.write(content)
        
    return self.response.out.write(json.dumps(result,default=dthandler))
        
  def get(self):
    result = SongData.get_entities()
    
    return self.respond(result)
    
app = webapp2.WSGIApplication([('/', MainHandler),
                               ('/blobform', BlobFormHandler),
                               ('/file/upload', UploadHandler),
                               ('/songform', SongFormHandler),
                               ('/file/songupload', SongUploadHandler),
                               ('/file/serve/([^/]+)?', ServeHandler),
                               ('/file/list', ListBlobHandler),
                               ('/login/login', LoginHandler),
                               ('/login/register', RegisterHandler),
                               ('/challenge/create', CreateChallengeHandler),
                               ('/challenge/list', ListChallengeHandler),
                               ('/songdata/list', ListSongsHandler)],
                              debug=True)