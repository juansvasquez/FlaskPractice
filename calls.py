import requests

#Get list of doctors
response = requests.get("http://127.0.0.1:5000/doctors")
print(response.json())

#Get list of appointments
response = requests.get("http://127.0.0.1:5000/appointments")
print(response.json())

#Delete appointment from doctor's calendar
response = requests.delete("http://127.0.0.1:5000/appointments/1")

#Add appointment for doctor #1 (no appointments)
response = requests.post("http://127.0.0.1:5000/appointments/", json = {'doc_id':'1','patient_fn':'Jake', 'patient_ln':'Jacobs','date':'2022-04-03','time':'15:00','appt_type':'New Patient'})
print(response.json())

#Add appointment for doctor #3 (3 concurrent appointments already scheduled)
response = requests.post("http://127.0.0.1:5000/appointments/", json = {'doc_id':'3','patient_fn':'Jane', 'patient_ln':'Janets','date':'2022-04-03','time':'14:00','appt_type':'New Patient'})
print(response.json())

#Final Appointments list
response = requests.get("http://127.0.0.1:5000/appointments")
print(response.json())