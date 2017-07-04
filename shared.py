
from flask import Flask, render_template, redirect, request

from google.appengine.api import users

def render_login_template(template, **kwargs):

    user = users.get_current_user()
    if user:
        login_url = users.create_logout_url(request.url)
        url_linktext = 'logout'
    else:
        login_url = users.create_login_url(request.url)
        url_linktext = 'login'

    return render_template(template, login_url=login_url, url_linktext=url_linktext, **kwargs)