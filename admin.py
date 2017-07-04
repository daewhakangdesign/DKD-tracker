import os
import uuid
from models import Person

from flask import Flask, request, redirect
app = Flask(__name__)
app.config['DEBUG'] = True

from shared import render_login_template

@app.route('/admin/people')
def get_people():
    people = Person.query().fetch()
    return render_login_template("admin-people.html", people=people)


@app.route('/admin/new-person', methods=["POST", "GET"])
def new_person():

    if request.method == 'POST':
        person = Person(name=request.form["name"], uuid=str(uuid.uuid4()))
        person.put()
        return redirect("/admin/people")

    return render_login_template("new-person.html")


@app.route('/admin/person/<person_uuid>/reset', methods=["POST"])
def reset_person(person_uuid):

    person = Person.query(Person.uuid == person_uuid).get()

    if person is not None:
        person.reset()

    return redirect("/admin/people")


@app.route('/admin/person/<person_uuid>/delete', methods=["POST"])
def delete_person(person_uuid):

        person = Person.query(Person.uuid == person_uuid).get()

        if person is not None:
            person.key.delete()

        return redirect("/admin/people")

