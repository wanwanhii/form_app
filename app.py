from flask import Flask, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Email(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), nullable=False)
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp(), nullable=False)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        email_address = request.form.get('email')
        if email_address and '@' in email_address:
            new_email = Email(email=email_address)
            try:
                db.session.add(new_email)
                db.session.commit()
                return redirect(url_for('success'))
            except Exception as e:
                db.session.rollback()
                print(f"Error: {e}")
        else:
            return render_template('index.html', error='Invalid email address. Please try again.', email=email_address)
    return render_template('index.html')

@app.route('/success')
def success():
    return "Data added successfully!"

if __name__ == '__main__':
    app.run(debug=True)