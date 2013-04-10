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
        b_purpose = entity.file_purpose
        b_owner = entity.file_owner
        entity.delete()
        
        if delete_blob_key:
            delete_key = blobstore.BlobKey(delete_blob_key)
            delete_blob = blobstore.BlobInfo(delete_key)
            delete_blob.delete()
        
        # Logging
        l_msg = "The submission '" + b_name + "' for '" + b_purpose + "' was deleted."
        new_log = Log(log_message=l_msg)
        new_log.put()   
        
        n_msg = "Your submission '" + b_name + "' has been processed for '" + b_purpose + "'."
        new_notification = Notification(notification_message=n_msg,
                                        notification_user=b_owner)
        new_notification.put()
        
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

class Challenge_Theme(db.Model):
  theme_name = db.StringProperty()
    
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
      #if current_time < challenge_expiry:
      
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
    try:
      entity = Challenge.get_by_id(int(model_id))
      
      if entity:
        return entity.challenge_name
      else:
        return "N/A"
    except ValueError:
      return "N/A"
      
  @staticmethod
  def check_if_expired(model_id):
    utc = UTC()
    sgt = SGT()
    try:
      entity = Challenge.get_by_id(int(model_id))
      
      if entity:
        challenge_expiry = entity.challenge_expiry.replace(tzinfo=utc)
        current_time = datetime.datetime.now().replace(tzinfo=utc)
        if current_time >= challenge_expiry:
          return True
        else:
          return False
      else:
        return True
    except ValueError:
      return True
      
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

class Achievement_User(db.Model):
  achievement_id = db.IntegerProperty()
  achievement_user = db.StringProperty()
  
  def to_dict(self):
       d = dict([(p, unicode(getattr(self, p))) for p in self.properties()])
       d["id"] = self.key().id()
       return d

  @staticmethod
  def add(data):
     
    jsonData = json.loads(data)
    
    result = ""
    a_id = int(jsonData['a_id'])
    a_user = jsonData['a_user']
    if a_id:
      achievement = Achievement.get_entity(a_id)
      users = User.all().run()
      for user in users:
        if user.user_name == a_user:
        
          user.user_points += int(achievement['a_points'])
          
          entity = Achievement_User(achievement_id=int(jsonData['a_id']),
                          achievement_user=jsonData['a_user'])
          
          entity.put()
          
          user.put()
        
          # Logging
          l_msg = entity.achievement_user + " has been awarded the achievement: '" + achievement['a_name'] + "'."
          new_log = Log(log_message=l_msg)
          new_log.put()
          
          n_msg = "You have been awarded " + str(achievement['a_points']) + " point(s) for attaining the achievement '" + achievement['a_name'] + "'."
          notify = Notification(notification_user=user.user_name,
                                    notification_message=n_msg)
          notify.put()
          
          result = {'a_id': jsonData['a_id'],
                    'a_user': jsonData['a_user']}
              
    return result

  @staticmethod
  def get_entities():
    #update ModelCount when adding
    theQuery = Achievement_User.all()

    objects = theQuery.run()
    entities = []
    for object in objects:
      entity = {'a_id':object.achievement_id,
              'id': object.key().id(),
              'a_user': object.achievement_user}
      entities.append(entity)
    result = {'method':'get_entities',
              'en_type': 'Achievement_User',
              'entities': entities}      
    return result 
    
class Achievement(db.Model):
  achievement_name = db.StringProperty()
  achievement_points = db.IntegerProperty()
  achievement_upload_by = db.StringProperty()
  
  def to_dict(self):
       d = dict([(p, unicode(getattr(self, p))) for p in self.properties()])
       d["id"] = self.key().id()
       return d

  @staticmethod
  def add(data):
     
    jsonData = json.loads(data)
    
    entity = Achievement(achievement_name=jsonData['a_name'],
                    achievement_points=int(jsonData['a_points']),
                    achievement_upload_by=jsonData['a_uploadby'])
    
    entity.put()
    
    # Logging
    l_msg = entity.achievement_upload_by + " has created the achievement: '" + entity.achievement_name + "'."
    new_log = Log(log_message=l_msg)
    new_log.put()

    result = {'a_name': jsonData['a_name'],
              'a_points': jsonData['a_points'],
              'a_uploadby': jsonData['a_uploadby']}
              
    return result

  @staticmethod
  def get_entity(model_id):
    theobject = Achievement.get_by_id(int(model_id))
    
    result = {'a_name':theobject.achievement_name,
              'id': theobject.key().id(),
              'a_points': theobject.achievement_points,
              'a_uploadby': theobject.achievement_upload_by}
    return result
    
  @staticmethod
  def get_entities():
    #update ModelCount when adding
    theQuery = Achievement.all()

    objects = theQuery.run()
    entities = []
    for object in objects:
      entity = {'a_name':object.achievement_name,
              'id': object.key().id(),
              'a_points': object.achievement_points,
              'a_uploadby': object.achievement_upload_by}
      entities.append(entity)
    result = {'method':'get_entities',
              'en_type': 'Achievement',
              'entities': entities}      
    return result 
    
  #You can't name it delete since db.Model already has a delete method
  @staticmethod
  def remove(model_id):
    #update model count when deleting
    entity = Achievement.get_by_id(int(model_id))
        
    if entity:
        a_name = entity.achievement_name        
        entity.delete()
            
        result = {'method':'delete_model_success',
                  'id': model_id
                  }
            
        # Logging
        l_msg = a_name + " was deleted."
        new_log = Log(log_message=l_msg)
        new_log.put()          
    else:
        result = {'method':'delete_model_not_found'}
    
    return result
    
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

class Notification(db.Model):
  notification_date = db.DateTimeProperty(auto_now_add=True)
  notification_user = db.StringProperty()
  notification_message = db.StringProperty()
  
  def to_dict(self):
       d = dict([(p, unicode(getattr(self, p))) for p in self.properties()])
       d["id"] = self.key().id()
       return d
  
  @staticmethod
  def get_entities(u_name):
    #update ModelCount when adding
    theQuery = Notification.all()
    theQuery.order('-notification_date')

    objects = theQuery.run(limit=30)
    utc = UTC()
    sgt = SGT()
    entities = []
    for object in objects:
      if object.notification_user == u_name:
        n_date = object.notification_date.replace(tzinfo=utc)
        n_date = n_date.astimezone(sgt)
        entity = {'n_date':n_date.strftime("%Y-%m-%d %H:%M:%S"),
                'id': object.key().id(),
                'n_msg': object.notification_message}
        entities.append(entity)
    result = {'method':'get_entities',
              'en_type': 'Notification',
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
      expired = Challenge.check_if_expired(int(model_id))
      if (challenge != "N/A" and expired != True):
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
      elif (challenge != "N/A" and expired == True):
        self.response.out.write('<html><body><link href="../app/css/bootstrap.css" rel="stylesheet">')
        self.response.out.write("We're sorry, but the challenge you are looking for has already expired.")
        self.response.out.write('</body></html>')
      else:
        self.response.out.write('<html><body><link href="../app/css/bootstrap.css" rel="stylesheet">')
        self.response.out.write("We're sorry, but the challenge you are looking for does not exist.")
        self.response.out.write('</body></html>')        
    else:
      self.response.out.write('<html><body><link href="../app/css/bootstrap.css" rel="stylesheet">')
      self.response.out.write("We're sorry, but the challenge you are looking for does not exist.")
      self.response.out.write('</body></html>')

class AchievementFormHandler(webapp2.RequestHandler):
  def get(self):
    achievements = Achievement.get_entities()
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
    self.response.out.write('Purpose: <br><select name="filepurpose">')
    for achievement in achievements['entities']:
      self.response.out.write('<option value="%s">%s</option>' % (achievement['a_name'], achievement['a_name']))
    self.response.out.write('</select><br>')
    self.response.out.write('Uploaded By: <br>{{name}} <input type="hidden" name="fileowner" value="{{name}}"><br>')
    self.response.out.write('<input type="submit" name="submit" value="Submit">')
    self.response.out.write('</form></body></html>')
      
class MissionFormHandler(webapp2.RequestHandler):
  def get(self, reason):
    purpose = ""
    if reason:
      purpose = reason
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
    self.response.out.write('Purpose: <br>%s <input type="hidden" name="filepurpose" value="%s"><br>' % (purpose, purpose))
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

  def score_challenge(self):
    jsonData = json.loads(self.request.body)
    c_id = jsonData['c_id']
    c_rankings = jsonData['c_rankings']
    c_scoreby = jsonData['c_scoreby']
    result = ""
    
    
    if c_id:
      c_name = Challenge.get_name(c_id)
      if c_name != "N/A":
        result = c_scoreby + " has given the results for " + c_name + ": "
        entities = User.all().run()
        
        for entity in entities:
          for ranking in c_rankings:
            if ranking['u_name'] == entity.user_name:
              n_msg = ""
              if ranking['u_earned'] == "1st":
                entity.user_points += 5
                n_msg = "You have been awarded 5 points for getting 1st place for " + c_name + "!"
              if ranking['u_earned'] == "2nd":
                entity.user_points += 3
                n_msg = "You have been awarded 3 points for getting 2nd place for " + c_name + "!"
              if ranking['u_earned'] == "3rd":
                entity.user_points += 2
                n_msg = "You have been awarded 2 points for getting 3rd place for " + c_name + "!"
              if ranking['u_earned'] == "Participation":
                entity.user_points += 1
                n_msg = "You have been awarded 1 point for getting participation for " + c_name + "!"
              result += ranking['u_earned'] + " - " + entity.user_name + " "
              entity.put()
              
              if n_msg != "":
                notify = Notification(notification_user=entity.user_name,
                                    notification_message=n_msg)
                notify.put()
                
        Challenge.remove(c_id)
        
      
    
    r_log = Log(log_message=result)
    r_log.put()
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
    
  def list_notifications(self, u_name):
    result = Notification.get_entities(u_name)
    
    return self.respond(result)
    
  def list_achievements(self):
    result = Achievement.get_entities()
    
    return self.respond(result)
    
  def create_achievement(self):
    jsonData = json.loads(self.request.body)
    result = Achievement.add(json.dumps(jsonData))
    
    return self.respond(result)
 
  def delete_achievement(self, model_id):
    result = Achievement.remove(model_id)
    
    return self.respond(result)
  
  def award_achievement(self):
    
    jsonData = json.loads(self.request.body)
    result = Achievement_User.add(json.dumps(jsonData))
    
    return self.respond(result)
    
  def list_achievement_users(self):
    result = Achievement_User.get_entities()
    
    return self.respond(result)

  def reward_theme(self):
    jsonData = json.loads(self.request.body)
    #This will be changed. Or not.
    t_name = jsonData['t_name']
    t_rewards = jsonData['t_rewards']
    t_scoreby = jsonData['t_scoreby']
    
    result = t_scoreby + " has given the results for those who guessed '" + t_name + "': "
    entities = User.all().run()
    
    for entity in entities:
      for reward in t_rewards:
        if reward['u_name'] == entity.user_name:
          n_msg = ""
          if reward['u_earned'] == "1st":
            entity.user_points += 3
            n_msg = "You have been awarded 3 points for being the 1st person to guess the current challenge theme - '" + t_name + "'!"
          if reward['u_earned'] == "2nd":
            entity.user_points += 2
            n_msg = "You have been awarded 2 points for being the 2nd person to guess the current challenge theme - '" + t_name + "'!"
          if reward['u_earned'] == "3rd":
            entity.user_points += 1
            n_msg = "You have been awarded 1 point for being the 3rd person to guess the current challenge theme - '" + t_name + "'!"
          result += reward['u_earned'] + " - " + entity.user_name + " "
          entity.put()
          
          if n_msg != "":
            notify = Notification(notification_user=entity.user_name,
                                notification_message=n_msg)
            notify.put()

    r_log = Log(log_message=result)
    r_log.put()
    return self.respond(result)            
                    
    
app = webapp2.WSGIApplication([
    webapp2.Route('/', handler=MainHandler),
    webapp2.Route('/missionform/<reason>', handler=MissionFormHandler),
    webapp2.Route('/blobform/<model_id>', handler=BlobFormHandler),
    webapp2.Route('/achievementform', handler=AchievementFormHandler),
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
    webapp2.Route('/challenge/score', handler=ActionHandler, handler_method='score_challenge'),
    webapp2.Route('/songdata/list', handler=ActionHandler, handler_method='list_songs'),
    webapp2.Route('/songdata/remove/<model_id>', handler=ActionHandler, handler_method='delete_songs'),
    webapp2.Route('/log/list', handler=ActionHandler, handler_method='list_logs'),
    webapp2.Route('/notification/list/<u_name>', handler=ActionHandler, handler_method='list_notifications'),
    webapp2.Route('/achievement/list', handler=ActionHandler, handler_method='list_achievements'),
    webapp2.Route('/achievement/create', handler=ActionHandler, handler_method='create_achievement'),
    webapp2.Route('/achievement/remove/<model_id>', handler=ActionHandler, handler_method='delete_achievement'),
    webapp2.Route('/achievement/award', handler=ActionHandler, handler_method='award_achievement'),
    webapp2.Route('/achievement/listusers', handler=ActionHandler, handler_method='list_achievement_users'),
    webapp2.Route('/theme/reward', handler=ActionHandler, handler_method='reward_theme')],
    debug=True)
app.error_handlers[404] = handle_404
#app.error_handlers[500] = handle_500