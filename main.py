from flask import Flask, render_template, request
from dotenv import load_dotenv
import os
from googletrans import Translator

def word_translator(word):
    translator = Translator()
    translation = translator.translate(word, src='en', dest='de')
    return translation


def configure():
    load_dotenv()


api_key = os.getenv('api_key')

app = Flask(__name__)


@app.route("/")
def index():
    return render_template('index.html')


@app.route('/submit', methods=['POST'])
def submit():
    translated_words = []
    input_value = request.form['text'].lower().split()

    for word in input_value:
        translated_words.append(word_translator(word).text)

    combined_lists = dict(zip(input_value, translated_words))

    return render_template('index.html', words=combined_lists)


if __name__ == '__main__':
    app.run(port=1347, debug=True)
