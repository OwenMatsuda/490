from flask import Flask, render_template, redirect, url_for, request
import subprocess
from digital_nurse import DigitalNurse

app = Flask(__name__)

user = None
digital_nurse = DigitalNurse()
print(digital_nurse)

@app.route('/')
def index():
    if (user != "doctor"):
        return redirect('/login')
    return render_template('index.html')
Ad

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

if __name__ == "__main__":
    app.run(port=8000, debug=True)
