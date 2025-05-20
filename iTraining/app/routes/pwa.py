from flask import render_template
from flask_smorest import Blueprint

from iTraining.app.models import Event, Participant

blp = Blueprint('pwa','progressive_app', description='Progressive Web App for Training')

@blp.route('/events/view')
def view_events():
    events = Event.get_all()
    return render_template('events/view.html', events=events)

@blp.route('/participants/view')
def view_participants():
    participants = Participant.get_all()
    return render_template('view_participants.html', participants=participants)