from flask import Flask, request, render_template, redirect, url_for
import csv
import datetime
import os

app = Flask(__name__)

# CSVファイルのパス
CSV_FILE = 'data.csv'

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        email = request.form['email']
        if validate_email(email):
            now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            write_to_csv(email, now)
            return redirect(url_for('success'))
        else:
            return render_template('index.html', error="Invalid email address. Please try again.", email=email)
    return render_template('index.html')

@app.route('/success')
def success():
    return render_template('success.html')

def validate_email(email):
    import re
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email) is not None

def write_to_csv(email, timestamp):
    file_exists = os.path.isfile(CSV_FILE)
    with open(CSV_FILE, mode='a', newline='') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(['Email', 'Timestamp'])
        writer.writerow([email, timestamp])

if __name__ == '__main__':
    app.run(debug=True)
