from flask import Flask, render_template, request
from dotenv import load_dotenv
import os
from googletrans import Translator

def word_translator(word):
    translator = Translator()
    translation = translator.translate(word, src='en', dest='de')
    print(translation.text)


def configure():
    load_dotenv()


api_key = os.getenv('api_key')



app = Flask(__name__)


@app.route("/")
def index():
    return render_template('index.html')


@app.route('/submit', methods=['POST'])
def submit():
    input_value = request.form['text'].lower().split()
    print(input_value)

    for word in input_value:
        word_translator(word)

    return render_template('index.html')


if __name__ == '__main__':
    app.run(port=1347, debug=True)
