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
              'u_pwd': jsonData['u_pwd'],
              'u_admin': bool(False)}
        
    return result
    
  @staticmethod
  def get_entity(model_id):
    theobject = User.get_by_id(int(model_id))
    
    result = {'u_name':theobject.user_name,
              'u_pwd': theobject.user_pwd,
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

class Challenge(db.Model):
  challenge_name = db.StringProperty(required=True)
  challenge_description = db.StringProperty()
  challenge_hint = db.StringProperty()
  challenge_points = db.IntegerProperty()
  challenge_admin_notes = db.StringProperty()
  challenge_date = db.DateTimeProperty(auto_now_add=True)
  challenge_expiry = db.DateTimeProperty()
  challenge_blob_key = db.StringProperty()
  
  def to_dict(self):
       d = dict([(p, unicode(getattr(self, p))) for p in self.properties()])
       d["id"] = self.key().id()
       return d

            
  @staticmethod
  def add(data):
     
    jsonData = json.loads(data)
    entity = Challenge(challenge_name=jsonData['c_name'],
                    challenge_description=jsonData['c_desc'],
                    challenge_hint=jsonData['c_hint'],
                    challenge_points=int(jsonData['c_points']),
                    challenge_admin_notes=jsonData['c_notes'],
                    challenge_blob_key=jsonData['c_blob'],)
    
    entity.put()
    
    result = {'c_name':jsonData['c_name'],
              'c_desc': jsonData['c_desc'],
              'c_hint': jsonData['c_hint'],
              'c_points': jsonData['c_points'],
              'c_notes': jsonData['c_notes'],
              'c_blob': jsonData['c_blob']}
        
    return result
  
  @staticmethod
  def get_entities():
    #update ModelCount when adding
    theQuery = Challenge.all()

    objects = theQuery.run()

    entities = []
    for object in objects:
      entity = {'c_name': object.challenge_name,
              'c_desc': object.challenge_description,
              'c_hint': object.challenge_hint,
              'c_points': object.challenge_points,
              'c_notes': object.challenge_admin_notes,
              'c_blob': object.challenge_blob_key}
      entities.append(entity)
    result = {'method':'get_entities',
              'en_type': 'Challenge',
              'entities': entities}       
    return result
    
  @staticmethod
  def get_entity(model_id):
    theobject = Challenge.get_by_id(int(model_id))
    
    result = {'c_name': theobject.challenge_name,
              'c_desc': theobject.challenge_description,
              'c_hint': theobject.challenge_hint,
              'c_points': theobject.challenge_points,
              'c_notes': theobject.challenge_admin_notes,
              'c_blob': theobject.challenge_blob_key}
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
    if jsonData['c_hint']!='':
      entity.challenge_hint=jsonData['c_hint']
    if jsonData['c_points']!='':
      entity.challenge_points=int(jsonData['c_points'])
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
    self.response.out.write("""Name of file:<br> <input type="text" name="filename"><br> Description:<br> <input type="text" name="filedescription"><br><hr/> Upload File: <input type="file" name="file"><br> <input type="hidden" name="fileowner" ng-model="name"> <input type="submit" name="submit" value="Submit"> </form></body></html>""")

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
  def get(self):
    # Query interface constructs a query using instance methods
    q = BlobData.all()


    # GqlQuery interface constructs a query using a GQL query string
    q = db.GqlQuery("SELECT * FROM BlobData")


    self.response.out.write('<html><body>')
    self.response.out.write('<table>')
    self.response.out.write('<thead></thead>')
    self.response.out.write('<tbody>')
    # Query is not executed until results are accessed
    for p in q.run():
      self.response.out.write('<tr>')
      self.response.out.write('<td>%s</td>' % p.file_name)
      self.response.out.write('<td>%s</td>' % p.file_desc)
      self.response.out.write('<td>%s</td>' % p.file_owner)
      self.response.out.write('<td><a href="/file/serve/%s">Link</a></td>' % p.file_blob_key)
      self.response.out.write('</tr>')

    self.response.out.write('</tbody>')
    self.response.out.write('<table>')
    self.response.out.write('</body></html>')

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
    result = {'u_name':'Invalid Username/Password',
              'u_admin':'Password!'}
    for object in objects:
      if jsonData['u_name']==object.user_name:
        if jsonData['u_pwd']==object.user_password:
          result = {'u_name':object.user_name,
              'u_pwd': object.user_password,
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
    result = {'u_name':'Invalid Username/Password',
              'u_admin':'Password!'}    
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
    
app = webapp2.WSGIApplication([('/', MainHandler),
                               ('/blobform', BlobFormHandler),
                               ('/file/upload', UploadHandler),
                               ('/file/serve/([^/]+)?', ServeHandler),
                               ('/file/list', ListBlobHandler),
                               ('/login/login', LoginHandler),
                               ('/login/register', RegisterHandler),
                               ('/challenge/create', CreateChallengeHandler),
                               ('/challenge/list', ListChallengeHandler)],
                              debug=True)