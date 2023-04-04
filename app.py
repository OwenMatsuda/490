from flask import Flask, render_template, redirect, url_for, request
import subprocess

app = Flask(__name__)

user = None

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

@app.route('/digital_nurse')
def digital_nurse():
    print("Running digital nurse!")
    subprocess.run(["python3", "./digital_nurse.py"])
    return ""

if __name__ == "__main__":
    app.run(port=8000, debug=True)
