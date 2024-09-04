from flask import Flask, render_template, request, redirect, url_for, session
import csv
import re
from datetime import datetime, timedelta, timezone

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # セッションの暗号化に必要なキー

# メールアドレスの正規表現パターン
EMAIL_REGEX = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'

@app.route('/', methods=['GET', 'POST'])
def index():
    # セッションからメッセージを取得して初期化
    message = session.pop('message', '')
    user_input = ''
    
    if request.method == 'POST':
        user_input = request.form['user_input']
        
        # バリデーション: メールアドレスの形式をチェック
        if not re.match(EMAIL_REGEX, user_input):
            message = 'Invalid email address. Please try again.'
        else:
            try:
                # 現在の日本時間を取得
                jst = timezone(timedelta(hours=9))  # 日本標準時 (UTC+9)
                now = datetime.now(jst)
                timestamp = now.strftime('%Y-%m-%d %H:%M:%S')

                # メールアドレスと登録日時を保存
                with open('data.csv', 'a', newline='') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow([user_input, timestamp])
                
                # メッセージをセッションに保存してリダイレクト
                session['message'] = 'Your email has been recorded!'
                return redirect(url_for('index'))
            except PermissionError:
                message = 'There was a problem saving your data. Please check file permissions.'
            except Exception as e:
                message = f'An unexpected error occurred: {e}'
    
    return render_template('index.html', user_input=user_input, message=message)

if __name__ == '__main__':
    app.run(debug=True)
