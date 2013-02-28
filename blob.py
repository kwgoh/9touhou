import os
import urllib
import webapp2
import datetime

from google.appengine.ext import blobstore
from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.ext.webapp import blobstore_handlers

class MainHandler(webapp2.RequestHandler):
  def get(self):
    upload_url = blobstore.create_upload_url('/upload')

class BlobData(db.Model):
    file_name = db.StringProperty(required=True)
    file_desc = db.StringProperty()
    file_date = db.DateProperty()
    file_owner = db.StringProperty()
    file_blob_key = db.StringProperty(required=True)

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

app = webapp2.WSGIApplication([('/', MainHandler),
                               ('/blobform', BlobFormHandler),
                               ('/file/upload', UploadHandler),
                               ('/file/serve/([^/]+)?', ServeHandler),
							   ('/file/list', ListBlobHandler)],
                              debug=True)