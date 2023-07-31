from flask import Flask, render_template, request
from dotenv import load_dotenv
import os
from googletrans import Translator
import openai

def word_translator(word):
    translator = Translator()
    translation = translator.translate(word, src='en', dest='de')
    return translation
def sentence_creator(keyword):
    openai.api_key = api_key
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        temperature=0.8,
        max_tokens=2000,
        messages=[
            {"role": "system", "content": "You are a teacher who want to find the best example sentence for a word."},
            {"role": "user", "content": f"Write a short sentence for the word: '{keyword}'."}
        ]
    )
    return completion.choices[0].message.content

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
    example_sentence = []
    input_value = request.form['text'].lower().split()

    for word in input_value:
        translated_words.append(word_translator(word).text)
        try:
            example_sentence.append(sentence_creator(word))
        except:
            print("error motherfucker")

    combined_lists = dict(zip(input_value, translated_words))
    for index, key in enumerate(input_value):
        combined_lists[key] = combined_lists[key] + '   - ' + example_sentence[index]

    return render_template('translated.html', words=combined_lists)


if __name__ == '__main__':
    app.run(port=1347, debug=True)
