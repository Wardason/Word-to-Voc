import csv
from flask import Flask, render_template, request, session
from dotenv import load_dotenv
import os
from googletrans import Translator
import openai


# region Functions
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

def save_data():
    combined_lists = session.get('combined_lists', {})
    with open('voc-data.csv', mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        for word, translation in combined_lists.items():
            writer.writerow([word + "   - " + translation])
    return combined_lists

def show_data():
    list_of_rows = []
    with open('voc-data.csv', newline='', encoding='utf-8') as file:
        csv_data = csv.reader(file, delimiter='/')
        list_of_rows = [row for row in csv_data]
        print(list_of_rows)
    return list_of_rows

def delete_data():
    with open('voc-data.csv', 'w') as file:
        pass

def sorting_translation(sort):
    translated_input = []
    input_value = request.form['text'].lower().split()
    creation = None

    for word in input_value:
        try:
            if sort == "word":
                creation = word_translator(word).text
            elif sort == "sentence":
                creation = sentence_creator(word)
            translated_input.append(creation)
        except Exception as e:
            print(f"Error Message in sorting word {e}")
            return render_template('error.html')
    return translated_input

def merge_translations_and_context(input_value, translated_words, example_sentence):
    combined_lists = dict(zip(input_value, translated_words))
    for index, key in enumerate(input_value):
        combined_lists[key] = combined_lists[key] + '   - ' + example_sentence[index]
    return combined_lists
# endregion





api_key = os.getenv('api_key')
app_secret = os.getenv('app_secret')

app = Flask(__name__)
app.secret_key = app_secret

@app.route("/")
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    input_value = request.form['text'].lower().split()
    translated_words = sorting_translation("word")
    example_sentence = sorting_translation("sentence")

    combined_lists = merge_translations_and_context(input_value, translated_words, example_sentence)
    session['combined_lists'] = combined_lists

    return render_template('translated.html', words=combined_lists)

@app.route('/save', methods=['POST'])
def save_data_website():
    combined_lists = save_data()
    return render_template('translated.html', words=combined_lists)

@app.route('/show', methods=['POST'])
def show_data_website():
    list_of_rows = show_data()
    return render_template('show-data.html', data=list_of_rows)

@app.route('/clear', methods=['POST'])
def clear_data_website():
    delete_data()
    return render_template('index.html')



if __name__ == '__main__':
    app.run(port=1347, debug=True)
