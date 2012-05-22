import cherrypy
from google.appengine.api import users

import handlers
import sys
from models.package import Package

class Packages(handlers.Base):
    @cherrypy.expose
    def index(self, name = None, page = 1):
        if cherrypy.request.method == 'POST':
            return self.index_post(name)

        offset = (page - 1) * 10
        packages = Package.all().order('-updated').fetch(10, offset)
        return self.render("packages/index", packages = packages)
        raise cherrypy.HTTPRedirect("/")

    def index_post(self, name):
        if not users.is_current_user_admin():
            raise cherrypy.HTTPError(403, "Only admins may create packages.")

        if not Package.create_unless_exists(name):
            self.flash('A package named "%s" already exists.' % name)
            raise cherrypy.HTTPRedirect('/packages/create')

        self.flash('Package "%s" created successfully.' % name)
        # TODO(nweiz): redirect to actual package page
        raise cherrypy.HTTPRedirect('/packages/')

    @cherrypy.expose
    def create(self):
        if not users.get_current_user():
            raise cherrypy.HTTPRedirect(
                users.create_login_url(cherrypy.url()))
        elif not users.is_current_user_admin():
            self.flash('Currently only admins may create packages.')
            raise cherrypy.HTTPRedirect('/packages/')

        return self.render("packages/create")