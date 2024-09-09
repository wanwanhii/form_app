from flask import Flask, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import datetime
import os

app = Flask(__name__)

# 環境変数からデータベースのURLを取得する
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///data.db')  # ローカルではSQLiteを使用
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# データベースのテーブル定義
class EmailEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def __init__(self, email):
        self.email = email

# データベースの初期化
@app.before_first_request
def create_tables():
    try:
        db.create_all()
    except Exception as e:
        print(f"Error creating tables: {e}")

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        email = request.form.get('email')
        if not email:
            return render_template('index.html', error="Email address is required.")
        if validate_email(email):
            try:
                new_entry = EmailEntry(email=email)
                db.session.add(new_entry)
                db.session.commit()
                return redirect(url_for('success'))
            except Exception as e:
                db.session.rollback()
                return render_template('index.html', error=f"Failed to save to database: {e}")
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

if __name__ == '__main__':
    app.run(debug=True)
