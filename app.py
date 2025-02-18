from flask import Flask, request, render_template, redirect, url_for, session
import os
import json
import resend
import base64

app = Flask(__name__)
app.secret_key = os.urandom(24)
PASSWORD = os.getenv('SITE_PASSWORD')
resend.api_key = os.getenv('RESEND_API_KEY')

# 加载翻译文件
translations = {}
translations_dir = os.path.join(app.root_path, 'translations')
for filename in os.listdir(translations_dir):
    if filename.endswith('.json'):
        lang_code = filename.split('.')[0]
        with open(os.path.join(translations_dir, filename), 'r', encoding='utf-8') as f:
            translations[lang_code] = json.load(f)

@app.context_processor
def inject_translations():
    lang = session.get('language', 'zh')
    return {
        'all_translations': translations,
        'translations': translations.get(lang, translations['zh']),
        'current_lang': lang
    }

@app.route('/')
def home():
    if 'authenticated' in session:
        return render_template('index.html')
    return redirect(url_for('login'))

@app.route('/setlang', methods=['POST'])
def set_language():
    session['language'] = request.form['language']
    return redirect(request.referrer or url_for('home'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['password'] == PASSWORD:
            session['authenticated'] = True
            return redirect(url_for('home'))
        return render_template('error.html', error=translations[session.get('language', 'zh')]['error_password']), 401
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('authenticated', None)
    return redirect(url_for('login'))

@app.route('/send-email', methods=['POST'])
def send_email():
    if 'authenticated' not in session:
        return redirect(url_for('login'))

    try:
        from_email = request.form['from']
        to_email = request.form['to']
        subject = request.form['subject']
        html = request.form['html']
        attachments = request.files.getlist('attachments')

        params = {
            'from': from_email,
            'to': [to_email],
            'subject': subject,
            'html': html
        }

        if attachments:
            attachment_data = [
                {
                    'filename': attachment.filename,
                    'content': base64.b64encode(attachment.read()).decode('utf-8')
                }
                for attachment in attachments
            ]
            params['attachments'] = attachment_data

        email_response = resend.Emails.send(params)
        return f"Email sent successfully: {email_response['id']}"
    except Exception as e:
        return str(e), 500

if __name__ == '__main__':
    app.run(debug=True)
