
from models import Person

from flask import Flask, render_template, request, redirect
app = Flask(__name__)
app.config['DEBUG'] = True


@app.route('/api/event', methods=["POST"])
def event():

    params = request.get_json(force=True)
    if params["event_type"] != "1234567":
        return (401, "Unauthorized")

    person = Person.query().filter(uuid=params["person_uuid"]).get()
    person.add_event(params["event_type"])

    return (200, "ok")

