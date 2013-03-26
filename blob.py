import os
import urllib
import webapp2
import datetime
import time

from google.appengine.ext import blobstore
from google.appengine.api import memcache
from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.ext.webapp.util import run_wsgi_app

import json

def handle_404(request, response, exception):
    response.headers['Content-Type'] = 'text/html; charset=UTF-8'
    response.write('<html><body>')
    response.write('<link href="http://9touhou.appspot.com/app/css/bootstrap.css" rel="stylesheet">')
    response.write('<div class="hero-unit">')
    response.write('<img src="http://9touhou.appspot.com/app/img/chirumiru_chiruno.jpg" style="display:block; margin-left:auto; margin-right:auto"/>')
    response.write('<h3 style="text-align:center">WHEEEEEEEEEEEE........</h3>')
    response.write('<p class="lead" style="text-align:center">Looks like nothing of note exists here. Did you get the address right?</p>')
    response.write('<p class="lead" style="text-align:center">Click <a href="http://9touhou.appspot.com">here</a> to return to the main website.</p>')
    response.write('<p style="text-align:center">Error Type: 404.</p>')
    response.write('</div></body></html>')
    response.set_status(404)

def handle_500(request, response, exception):
    response.headers['Content-Type'] = 'text/html; charset=UTF-8'
    response.write('<html><body>')
    response.write('<link href="http://9touhou.appspot.com/app/css/bootstrap.css" rel="stylesheet">')
    response.write('<div class="hero-unit">')
    response.write('<img src="http://9touhou.appspot.com/app/img/ICECAR.jpg" style="display:block; margin-left:auto; margin-right:auto"/>')
    response.write('<h3 style="text-align:center">WHEEEEEEEEEEEE........</h3>')
    response.write('<p class="lead" style="text-align:center">Something funny happened, and the site is now misbehaving.</p>')
    response.write('<p class="lead" style="text-align:center">Please refresh the page in a little while, or click <a href="http://9touhou.appspot.com">here</a> to return to the main website.</p>')
    response.write('<p style="text-align:center">Error Type: 500.</p>')
    response.write('</div></body></html>')
    response.set_status(500)

#def blob_decode(str):
    #encoding = chardet.detect(str)['encoding']
    #return str.decode(encoding)
    
class MainHandler(webapp2.RequestHandler):
  def get(self):
    upload_url = blobstore.create_upload_url('/upload')

class UTC(datetime.tzinfo):
  def utcoffset(self, dt):
    return datetime.timedelta(hours=0)
    
  def dst(self, dt):
    return datetime.timedelta(0)
    
  def tzname(self, dt):
    return "UTC"
    
class SGT(datetime.tzinfo):
  def utcoffset(self, dt):
    return datetime.timedelta(hours=8)
    
  def dst(self, dt):
    return datetime.timedelta(0)
    
  def tzname(self, dt):
    return "SGT"
    
class BlobData(db.Model):
  file_name = db.StringProperty(required=True)
  file_purpose = db.StringProperty()
  file_desc = db.StringProperty()
  file_date = db.DateTimeProperty()
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
    utc = UTC()
    sgt = SGT()
    entities = []
    for object in objects:
      file_date = object.file_date.replace(tzinfo=utc)
      file_date = file_date.astimezone(sgt)
      entity = {'f_name': object.file_name,
              'id': object.key().id(),
              'f_purpose': object.file_purpose,
              'f_desc': object.file_desc,
              'f_date': file_date.strftime("%Y-%m-%d %H:%M:%S"),
              'f_owner': object.file_owner,
              'f_blob': object.file_blob_key}
      entities.append(entity)
    result = {'method':'get_entities',
              'en_type': 'Blob',
              'entities': entities}       
    return result  
    
  #You can't name it delete since db.Model already has a delete method
  @staticmethod
  def remove(model_id):
    #update model count when deleting
    entity = BlobData.get_by_id(int(model_id))
    
    if entity:
        delete_blob_key = entity.file_blob_key
        b_name = entity.file_name
        entity.delete()
        
        if delete_blob_key:
            delete_key = blobstore.BlobKey(delete_blob_key)
            delete_blob = blobstore.BlobInfo(delete_key)
            delete_blob.delete()
        
        # Logging
        l_msg = b_name + " was deleted."
        new_log = Log(log_message=l_msg)
        new_log.put()    
        
        result = {'method':'delete_model_success',
                  'id': model_id
                  }
    else:
        result = {'method':'delete_model_not_found'}
    
    return result  
    
class SongData(db.Model):
  song_name = db.StringProperty(required=True,default='Unknown')
  song_composer = db.StringProperty(required=True,default='Unknown')
  song_details = db.StringProperty()
  song_date = db.DateTimeProperty()
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
    utc = UTC()
    sgt = SGT()
    entities = []
    for object in objects:
      song_date = object.song_date.replace(tzinfo=utc)
      song_date = song_date.astimezone(sgt)
      entity = {'s_name': object.song_name,
              'id': object.key().id(),
              's_comp': object.song_composer,
              's_details': object.song_details,
              's_date': song_date.strftime("%Y-%m-%d %H:%M:%S"),
              's_uploadby': object.song_upload_by,
              's_blob': object.song_blob_key}
      entities.append(entity)
    result = {'method':'get_entities',
              'en_type': 'Song',
              'entities': entities}       
    return result
    
  #You can't name it delete since db.Model already has a delete method
  @staticmethod
  def remove(model_id):
    #update model count when deleting
    entity = SongData.get_by_id(int(model_id))
    
    if entity:
        delete_blob_key = entity.song_blob_key
        s_name = entity.song_name
        entity.delete()
        
        if delete_blob_key:
            delete_key = blobstore.BlobKey(delete_blob_key)
            delete_blob = blobstore.BlobInfo(delete_key)
            delete_blob.delete()
            
        # Logging
        l_msg = s_name + " was deleted."
        new_log = Log(log_message=l_msg)
        new_log.put()    
        
        result = {'method':'delete_model_success',
                  'id': model_id
                  }
    else:
        result = {'method':'delete_model_not_found'}
    
    return result  
    
class User(db.Model):
  user_name = db.StringProperty(required=True)
  user_password = db.StringProperty(required=True)
  user_isadmin = db.BooleanProperty(required=True)
  user_points = db.IntegerProperty(required=True, default=0)
  
  def to_dict(self):
       d = dict([(p, unicode(getattr(self, p))) for p in self.properties()])
       d["id"] = self.key().id()
       return d

            
  @staticmethod
  def add(data):
     
    jsonData = json.loads(data)
    entity = User(user_name=jsonData['u_name'],
                    user_password=jsonData['u_pwd'],
                    user_isadmin=bool(False),
                    user_points=0)
    
    entity.put()
    
    # Logging
    l_msg = entity.user_name + " has registered."
    new_log = Log(log_message=l_msg)
    new_log.put()
    
    result = {'u_name':jsonData['u_name'],
              'u_admin': bool(False),
              'u_points': 0}
        
    return result
            
  @staticmethod
  def get_entities():
    #update ModelCount when adding
    theQuery = User.all()

    objects = theQuery.run()
    entities = []
    for object in objects:
      entity = {'u_name':object.user_name,
              'id': object.key().id(),
              'u_admin': str(object.user_isadmin),
              'u_points': object.user_points}
      entities.append(entity)
    result = {'method':'get_entities',
              'en_type': 'User',
              'entities': entities}      
    return result
    
  @staticmethod
  def get_entity(model_id):
    theobject = User.get_by_id(int(model_id))
    
    result = {'u_name':theobject.user_name,
              'id': theobject.key().id(),
              'u_admin': str(theobject.user_isadmin),
              'u_points': theobject.user_points}
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
    if jsonData['u_points']!='':
      entity.user_points=jsonData['u_points']
    entity.put()
    
    result = {'id': entity.key().id(), 
              'data': json.dumps(jsonData)
              }
    return result

class Challenge_Songs(db.Model):
  challenge_id = db.IntegerProperty(required=True,default=0)
  song_name = db.StringProperty(required=True,default="")
  difficulty = db.StringProperty(required=True,default="BSC")
    
class Challenge(db.Model):
  challenge_name = db.StringProperty(required=True)
  challenge_description = db.StringProperty(default="")
  challenge_admin_notes = db.StringProperty(default="")
  challenge_date = db.DateTimeProperty()
  challenge_upload_by = db.StringProperty(default="")
  challenge_expiry = db.DateTimeProperty()
  
  def to_dict(self):
       d = dict([(p, unicode(getattr(self, p))) for p in self.properties()])
       d["id"] = self.key().id()
       return d

            
  @staticmethod
  def add(data):
     
    jsonData = json.loads(data)
    c_expiry = datetime.datetime.strptime(jsonData['c_date'], "%Y-%m-%dT%H:%M:%S.%fZ")
    c_expiry = c_expiry + datetime.timedelta( 0, 23*60*60 )
    entity = Challenge(challenge_name=jsonData['c_name'],
                    challenge_description=jsonData['c_desc'],
                    challenge_admin_notes=jsonData['c_notes'],
                    challenge_date=datetime.datetime.now(SGT()),
                    challenge_upload_by=jsonData['c_uploadby'],
                    challenge_expiry=c_expiry)# 2013-03-26T16:00:00.000Z
                    #2013-03-15T07:13:34.034360
    
    entity.put()
    
    # Logging
    l_msg = entity.challenge_upload_by + " has posted '" + entity.challenge_name + "'."
    new_log = Log(log_message=l_msg)
    new_log.put()
    
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
              'c_uploadby': jsonData['c_uploadby'],
              'c_date': jsonData['c_date'],
              'c_blob': jsonData['c_blob'],
              'c_songs_count': count}
        
    return result
  
  @staticmethod
  def get_entities():
    #update ModelCount when adding

    theQuery = Challenge.all()

    objects = theQuery.run()
    utc = UTC()
    sgt = SGT()
    entities = []
    for object in objects:
      
      challenge_expiry = object.challenge_expiry.replace(tzinfo=utc)
      current_time = datetime.datetime.now().replace(tzinfo=utc)
      if current_time < challenge_expiry:
      
        challenge_expiry = challenge_expiry.astimezone(sgt)
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
                'id': object.key().id(),
                'c_desc': object.challenge_description,
                'c_notes': object.challenge_admin_notes,
                'c_uploadby': object.challenge_upload_by,
                'c_date': challenge_expiry.strftime("%Y-%m-%d %H:%M:%S"),
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
    utc = UTC()
    sgt = SGT()
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
        
    challenge_expiry = theobject.challenge_expiry.replace(tzinfo=utc)
    challenge_expiry = challenge_expiry.astimezone(sgt)  
    result = {'c_name': theobject.challenge_name,
              'id': theobject.key().id(),
              'c_desc': theobject.challenge_description,
              'c_notes': theobject.challenge_admin_notes,
              'c_uploadby': theobject.challenge_upload_by,
              'c_date': challenge_expiry.strftime("%Y-%m-%d %H:%M:%S"),
              'c_songs': c_songs}
    return result
  
  @staticmethod
  def get_name(model_id):
    entity = Challenge.get_by_id(int(model_id))
    
    if entity:
      return entity.challenge_name
    else:
      return "N/A"
  
  #You can't name it delete since db.Model already has a delete method
  @staticmethod
  def remove(model_id):
    #update model count when deleting
    entity = Challenge.get_by_id(int(model_id))
        
    if entity:
        c_songs_query = Challenge_Songs.all().filter('challenge_id', entity.key().id()).run()
        
        c_name = entity.challenge_name        
        entity.delete()
        
        if c_songs_query:
          for c_s in c_songs_query:
            c_s.delete()
            
        result = {'method':'delete_model_success',
                  'id': model_id
                  }
            
        # Logging
        l_msg = c_name + " was deleted."
        new_log = Log(log_message=l_msg)
        new_log.put()          
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
    if jsonData['c_uploadby']!='':
      entity.challenge_upload_by=jsonData['c_uploadby']
    if jsonData['c_date']!='':
      entity.challenge_expiry=jsonData['c_date'].strftime("%Y-%m-%d %H:%M:%S")
    if jsonData['c_notes']!='':
      entity.challenge_admin_notes=jsonData['c_notes']
    if jsonData['c_blob']!='':
      entity.challenge_blob_key=jsonData['c_blob']	  
    entity.put()

    result = {'id': entity.key().id(), 
              'data': json.dumps(jsonData)
              }
    return result

class Achievement(db.Model):
  achievement_name = db.StringProperty()
  achievement_points = db.IntegerProperty()
  
class Log(db.Model):
  log_date = db.DateTimeProperty(auto_now_add=True)
  log_message = db.StringProperty()
  
  def to_dict(self):
       d = dict([(p, unicode(getattr(self, p))) for p in self.properties()])
       d["id"] = self.key().id()
       return d
  
  @staticmethod
  def get_entities():
    #update ModelCount when adding
    theQuery = Log.all()
    theQuery.order('-log_date')

    objects = theQuery.run(limit=30)
    utc = UTC()
    sgt = SGT()
    entities = []
    for object in objects:
      l_date = object.log_date.replace(tzinfo=utc)
      l_date = l_date.astimezone(sgt)
      entity = {'l_date':l_date.strftime("%Y-%m-%d %H:%M:%S"),
              'id': object.key().id(),
              'l_msg': object.log_message}
      entities.append(entity)
    result = {'method':'get_entities',
              'en_type': 'Log',
              'entities': entities}      
    return result
    
class RandomNews(db.Model):
  time_stamp = db.DateTimeProperty()
  message = db.StringProperty()
  
#Handlers    
    
class BlobFormHandler(webapp2.RequestHandler):
  def get(self, model_id):
    challenge = ""
    if model_id:
      challenge = Challenge.get_name(int(model_id))
    upload_url = blobstore.create_upload_url('/file/upload')
    self.response.headers['Content-Type'] = 'text/html; charset=UTF-8'
    self.response.out.write('<html ng-app="myApp"><body ng-controller="FormController"><link href="../app/css/bootstrap.css" rel="stylesheet">')
    self.response.out.write('<script src="../app/js/jquery.js"></script>')
    self.response.out.write('<script src="../app/js/jquery-ui-1.10.2.custom.min.js"></script>')
    self.response.out.write('<script src="../app/lib/angular/angular.min.js"></script>')
    self.response.out.write('<script src="../app/lib/angular/angular-ui.min.js"></script>')
    self.response.out.write('<script src="../app/lib/angular/angular-resource.min.js"></script>')
    self.response.out.write('<script src="../app/js/app.js"></script>')
    self.response.out.write('<script src="../app/js/controllers.js"></script>')
    self.response.out.write('<script src="../test/lib/angular/angular-mocks.js"></script>')
    self.response.out.write('<form action="%s" method="POST" enctype="multipart/form-data">' % upload_url)
    self.response.out.write('Name of file:<br> <input type="text" name="filename"><br>')
    self.response.out.write('Description:<br> <input type="text" name="filedescription"><br>')
    self.response.out.write('Upload File: <br><input type="file" name="file"><br>')
    self.response.out.write('Purpose: <br>%s <input type="hidden" name="filepurpose" value="%s"><br>' % (challenge, challenge))
    self.response.out.write('Uploaded By: <br>{{name}} <input type="hidden" name="fileowner" value="{{name}}"><br>')
    self.response.out.write('<input type="submit" name="submit" value="Submit">')
    self.response.out.write('</form></body></html>')

class SongFormHandler(webapp2.RequestHandler):
  def get(self):
    upload_url = blobstore.create_upload_url('/file/songupload')
    self.response.headers['Content-Type'] = 'text/html; charset=UTF-8'
    self.response.out.write('<html ng-app="myApp"><body ng-controller="FormController"><link href="app/css/bootstrap.css" rel="stylesheet">')
    self.response.out.write('<script src="app/js/jquery.js"></script>')
    self.response.out.write('<script src="app/js/jquery-ui-1.10.2.custom.min.js"></script>')
    self.response.out.write('<script src="app/lib/angular/angular.min.js"></script>')
    self.response.out.write('<script src="app/lib/angular/angular-ui.min.js"></script>')
    self.response.out.write('<script src="app/lib/angular/angular-resource.min.js"></script>')
    self.response.out.write('<script src="app/js/app.js"></script>')
    self.response.out.write('<script src="app/js/controllers.js"></script>')
    self.response.out.write('<script src="test/lib/angular/angular-mocks.js"></script>')
    self.response.out.write('<form action="%s" method="POST" enctype="multipart/form-data">' % upload_url)
    self.response.out.write('Name of Song:<br> <input type="text" name="s_name"><br>')
    self.response.out.write('Composer:<br> <input type="text" name="s_comp"><br>')
    self.response.out.write('Song Details:<br> <input type="text" name="s_details"><br>')
    self.response.out.write('Upload File: <br><input type="file" name="song"><br>')
    self.response.out.write('Uploaded By: <br>{{name}} <input type="hidden" name="s_uploadby" value="{{name}}"><br>')
    self.response.out.write('<input type="submit" name="submit" value="Submit">')
    self.response.out.write('</form></body></html>')

class UploadHandler(blobstore_handlers.BlobstoreUploadHandler):
  def post(self):
    upload_files = self.get_uploads('file')  # 'file' is file upload field in the form
    f_name = self.request.POST.get('filename')
    #f_name = blob_decode(base64.b64decode(f_name))
    f_desc = self.request.POST.get('filedescription')
    #f_desc = blob_decode(base64.b64decode(f_desc))
    f_owner = self.request.POST.get('fileowner')
    f_purpose = self.request.POST.get('filepurpose')
    if f_purpose is None:
      f_purpose = ""
    
    blob_info = upload_files[0]
    
    try:
        b = BlobData(file_name=f_name,
             file_desc=f_desc,
             file_date=datetime.datetime.now(SGT()),
             file_owner=f_owner,
             file_purpose=f_purpose,
             file_blob_key=str(blob_info.key()))
        b.put()
                    
        # Logging
        l_msg = f_owner + " has submitted '" + f_name + "' for '" + f_purpose + "'."
        new_log = Log(log_message=l_msg)
        #new_log.log_date = file_date
        new_log.put()
        
        self.redirect('/status/success')
        
    except BadValueError:
        print "Error in uploading file!"
        self.redirect('/status/failure')
    

class SongUploadHandler(blobstore_handlers.BlobstoreUploadHandler):
  def post(self):
    upload_song = self.get_uploads('song')  # 'file' is file upload field in the form
    s_name = self.request.POST.get('s_name')
    #s_name = blob_decode(base64.b64decode(s_name))
    s_comp = self.request.POST.get('s_comp')
    #s_comp = blob_decode(base64.b64decode(s_comp))
    s_details = self.request.POST.get('s_details')
    #s_details = blob_decode(base64.b64decode(s_details))
    s_uploadby = self.request.POST.get('s_uploadby')
    blob_info = upload_song[0]
    
    try:
        s = SongData(song_name=s_name,
             song_composer=s_comp,
             song_details=s_details,
             song_date=datetime.datetime.now(SGT()),
             song_upload_by=s_uploadby,
             song_blob_key=str(blob_info.key()))
        s.put()

        # Logging
        l_msg = s_uploadby + " has added the song '" + s_name + "'."
        new_log = Log(log_message=l_msg)
        new_log.put()
        
        self.redirect('/status/success')
        
    except BadValueError:
        print "Error in uploading file!"
        self.redirect('/status/failure')
        
class UploadSuccess(webapp2.RequestHandler):
  def get(self):
    self.response.headers['Content-Type'] = 'text/html; charset=UTF-8'
    self.response.out.write('<html><body><link href="app/css/bootstrap.css" rel="stylesheet">')
    self.response.out.write('<p>Your upload has been successful. You may now close this window.</p>')
    self.response.out.write('</body></html>')

class UploadFailure(webapp2.RequestHandler):
  def get(self):
    self.response.headers['Content-Type'] = 'text/html; charset=UTF-8'
    self.response.out.write('<html><body><link href="app/css/bootstrap.css" rel="stylesheet">')
    self.response.out.write('<p>Your upload was not successful. Please close this window and try uploading again.</p>')
    self.response.out.write('</body></html>')
    
class ServeHandler(blobstore_handlers.BlobstoreDownloadHandler):
  def get(self, blob_key):
    if blob_key:
      resource = str(urllib.unquote(blob_key))
      blob_info = blobstore.BlobInfo.get(resource)
      if blob_info:
        self.send_blob(blob_info)
    
class ActionHandler(webapp2.RequestHandler):
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
    
  def list_blob(self):
    result = BlobData.get_entities()
    
    return self.respond(result)

  def delete_blob(self, model_id):
    result = BlobData.remove(model_id)
    
  def login(self):
    jsonData = json.loads(self.request.body)
    # Query interface constructs a query using instance methods
    q = User.all()
    objects = q.run()
    result = {'error':'Invalid Username/Password!'}  
    for object in objects:
      if jsonData['u_name']==object.user_name:
        if jsonData['u_pwd']==object.user_password:
          result = {'u_name':object.user_name,
              'u_admin': object.user_isadmin,
              'u_points': object.user_points}
              
    return self.respond(result)

  def register(self):
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

  def list_users(self):
    result = User.get_entities()
    
    return self.respond(result)
    
  def verify_user(self):
    jsonData = json.loads(self.request.body)
    
    # Query interface constructs a query using instance methods
    q = User.all()
    objects = q.run()
    
    result = {'error':'User does not exist!'}    
    for object in objects:
      if jsonData['u_name']==object.user_name:
        result = {'error':'User details are invalid!'}
        if jsonData['u_admin']==str(object.user_isadmin).lower():
          result = {'u_name':object.user_name,
                    'u_admin':object.user_isadmin,
                    'u_points':object.user_points}
    
    return self.respond(result)
    
  def create_challenge(self):
    jsonData = json.loads(self.request.body)
    result = Challenge.add(json.dumps(jsonData))
    
    return self.respond(result)

  def list_challenge(self):
    result = Challenge.get_entities()
    
    return self.respond(result)

  def delete_challenge(self, model_id):
    result = Challenge.remove(model_id)
    
    return self.respond(result)

  def list_songs(self):
    result = SongData.get_entities()
    
    return self.respond(result)
    
  def delete_songs(self, model_id):
    result = SongData.remove(model_id)
    
    return self.respond(result)
    
  def list_logs(self):
    result = Log.get_entities()
    
    return self.respond(result)
        
app = webapp2.WSGIApplication([
    webapp2.Route('/', handler=MainHandler),
    webapp2.Route('/blobform/<model_id>', handler=BlobFormHandler),
    webapp2.Route('/file/upload', handler=UploadHandler),
    webapp2.Route('/songform', handler=SongFormHandler),
    webapp2.Route('/file/songupload', handler=SongUploadHandler),
    webapp2.Route('/file/serve/<blob_key>', handler=ServeHandler),
    webapp2.Route('/status/success', handler=UploadSuccess),
    webapp2.Route('/status/failure', handler=UploadFailure),
    webapp2.Route('/file/list', handler=ActionHandler, handler_method='list_blob'),
    webapp2.Route('/file/remove/<model_id>', handler=ActionHandler, handler_method='delete_blob'),
    webapp2.Route('/login/login', handler=ActionHandler, handler_method='login'),
    webapp2.Route('/login/register', handler=ActionHandler, handler_method='register'),
    webapp2.Route('/user/list', handler=ActionHandler, handler_method='list_users'),
    webapp2.Route('/user/verify', handler=ActionHandler, handler_method='verify_user'),
    webapp2.Route('/challenge/create', handler=ActionHandler, handler_method='create_challenge'),
    webapp2.Route('/challenge/list', handler=ActionHandler, handler_method='list_challenge'),
    webapp2.Route('/challenge/remove/<model_id>', handler=ActionHandler, handler_method='delete_challenge'),
    webapp2.Route('/songdata/list', handler=ActionHandler, handler_method='list_songs'),
    webapp2.Route('/songdata/remove/<model_id>', handler=ActionHandler, handler_method='delete_songs'),
    webapp2.Route('/log/list', handler=ActionHandler, handler_method='list_logs')],
    debug=True)
app.error_handlers[404] = handle_404
app.error_handlers[500] = handle_500