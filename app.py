from flask import Flask, render_template, request, redirect, url_for, jsonify
from models import db, Complaint
import os
import openai
from translate import Translator

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///falpha1.db'

db.init_app(app)

# Flask Migrate
from flask_migrate import Migrate

migrate = Migrate(app, db)

openai.api_key = os.environ['OPENAI_API_KEY']

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit_complaint():
    name = request.form['name']
    phone = request.form['phone']
    locality = request.form['locality']
    problem = request.form['problem']

    complaint = Complaint(name=name, phone=phone, locality=locality, problem=problem)
    db.session.add(complaint)
    db.session.commit()

    return redirect(url_for('home'))

@app.route('/chatbot')
def chatbot():
    return render_template('chatbot.html')

@app.route('/gpt', methods=['POST'])
def gpt():
    try:
        message = request.form['message']
        language = request.form['language']
        response = call_gpt_api(message, language)
        return jsonify(response=response)
    except Exception as e:
        print("Error in GPT API call:", e)
        return jsonify(error=str(e))


def translate_text(text, target_language):
    translator = Translator(to_lang=target_language)
    translation = translator.translate(text)
    return translation



def call_gpt_api(message, language):
    # Translate the message to English if it's in Hindi or Telugu
    if language == 'hi' or language == 'te':
        message = translate_text(message, 'en')

    messages = [{"role": "system", "content": "You are a Legal GPT for Law relating to Women in India. Based on the problem of the user, you will check the relavant laws and provide the user with the sections under which they can file a case. \nYou will also give the mention of reporting authority and the procedure to file a case in an empathetic tone"}]
    messages.append({"role": "user", "content": message})
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        max_tokens=1000,
        n=1,
        stop=None,
        temperature=0.5,
        messages=messages
    )
    response_text = response.choices[0].message["content"].strip()

    # Translate the response back to the selected language if it's Hindi or Telugu
    if language == 'hi' or language == 'te':
        response_text = translate_text(response_text, language)

    return response_text


if __name__ == '__main__':
    ports = [8080, 8000, 5000]
    for port in ports:
        try:
            app.run(debug=True, port=port)
            break
        except OSError as e:
            print(f"Port {port} is in use, trying the next one...")

