from flask import Flask
from flask_restful import Resource, Api, reqparse
from datetime import datetime

app = Flask(__name__)
api = Api(app)

DOCTORS = {
  '1': {'fname': 'Hippo', 'lname': 'Crates'},
  '2': {'fname': 'Alexander', 'lname': 'Fleming'},
  '3': {'fname': 'Helene', 'lname': 'Gayle'}
}

APPTS = {
  '1': {'doc_id':'2','patient_fn':'Mike', 'patient_ln':'Michaels','date':'2022-04-03','time':'13:00','appt_type':'New-Patient'},
  '2': {'doc_id':'3','patient_fn':'John', 'patient_ln':'Johnson','date':'2022-04-03','time':'14:00','appt_type':'Follow-up'},
  '3': {'doc_id':'3','patient_fn':'Sam', 'patient_ln':'Samuels','date':'2022-04-03','time':'14:00','appt_type':'Follow-up'},
  '4': {'doc_id':'3','patient_fn':'Dick', 'patient_ln':'Richards','date':'2022-04-03','time':'14:00','appt_type':'Follow-up'}
}

parser = reqparse.RequestParser()

class DoctorsList(Resource):
  def get(self):
    return DOCTORS

class AppointmentList(Resource):
  def get(self):
    return APPTS

  def post(self):
    parser.add_argument('doc_id')
    parser.add_argument('patient_fn')
    parser.add_argument('patient_ln')
    parser.add_argument('date')
    parser.add_argument('time')
    parser.add_argument('appt_type')
    args = parser.parse_args()
    appt_id = int(max(APPTS.keys())) + 1
    appt_id = '%i' % appt_id
    
    
    time_suffixes = ('00','15','30','45')
    checker = 0
    #Check if the time slot is an increment of 15 mins
    if args['time'].endswith(time_suffixes):
      
      #Check if the time+date combo exists more than 3 times in the appointments list
      for k in APPTS:
        if APPTS[k]['doc_id'] == args['doc_id'] and APPTS[k]['date'] == args['date'] and APPTS[k]['time'] == args['time']:
          checker += 1
          if checker == 3:
            return "Doctor is already fully booked for this time slot", 422
      
      APPTS[appt_id] = {
      'doc_id':args['doc_id'],
      'patient_fn':args['patient_fn'],
      'patient_ln':args['patient_ln'],
      'date':args['date'],
      'time':args['time'],
      'appt_type':args['appt_type']
      }
      return APPTS[appt_id], 201
        
    else:
      return "Time must be in increment of 15", 422



class Appointment(Resource):
  def delete(self, appt_id):
    if appt_id not in APPTS:
      return "Not found", 404
    else:
      del APPTS[appt_id]
      return '', 204


api.add_resource(DoctorsList, '/doctors/')
api.add_resource(AppointmentList, '/appointments/')
api.add_resource(Appointment, '/appointments/<appt_id>')


if __name__ == "__main__":
  app.run(debug=True)