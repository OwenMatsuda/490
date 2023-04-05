from flask import Flask, render_template, redirect, request, jsonify
from digital_nurse import DigitalNurse
import json
 

app = Flask(__name__)

user = None
digital_nurse = DigitalNurse()
print(digital_nurse)

@app.route('/')
def index():
    if (user != "doctor"):
        return redirect('/login')
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'doctor' or request.form['password'] != 'doctor':
            error = 'Invalid Credentials. Please try again.'
        else:
            global user
            user = "doctor"
            return redirect('/')
    return render_template('login.html', error=error)

@app.route('/set_patient')
def set_patient():
    print("Running digital nurse!") 
    digital_nurse.set_patient()
    return ""

@app.route('/get_patient')
def get_patient():
    print("Running digital nurse!") 
    patient_data = digital_nurse.get_patient()
    return patient_data

@app.route('/nurse')
def nurse():
    # digital_nurse.set_patient()
    text = digital_nurse.audio_loop()
    print(3)
    print(text)
    response = app.response_class(
        response=json.dumps(text),
        status=200,
        mimetype='application/json'
    )
    return response

if __name__ == "__main__":
    app.run(port=8000, debug=True)
