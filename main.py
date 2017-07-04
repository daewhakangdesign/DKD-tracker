from flask import Flask, render_template, redirect, request
app = Flask(__name__)
app.config['DEBUG'] = True

from google.appengine.api import memcache

from models import Person
from shared import render_login_template


@app.route('/')
def people():

    people = Person.query().fetch()
    return render_login_template("people.html", people=people)


@app.route('/new-event', methods=["POST"])
def new_event():

    person_uuid = request.form["person_uuid"]

    cooldown = memcache.get(person_uuid)

    if cooldown is None:
        person = Person.query(Person.uuid == person_uuid).get()
        person.add_event(request.form["event_type"])
        memcache.add(person_uuid, "cooldown", 5)

    return redirect("/")


@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return 'Sorry, nothing at this URL.', 404
