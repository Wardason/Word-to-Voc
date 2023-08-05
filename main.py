import csv
from flask import Flask, render_template, request, session
from dotenv import load_dotenv
import os
from googletrans import Translator
import openai

# This function takes an English word as input and translates it to German and retruns it
def word_translator(word):
    translator = Translator()
    translation = translator.translate(word, src='en', dest='de')
    return translation


# This function uses the ChatGPT API to generate a random sentence, incorporating the provided English Keyword.
# The generated sentence is returned as the output.
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

# This function loads the env file, in which the api key and the session key is stored
def configure():
    load_dotenv()


api_key = os.getenv('api_key')
app_secret = os.getenv('app_secret')

app = Flask(__name__)
app.secret_key = app_secret

# Main website
@app.route("/")
def index():
    return render_template('index.html')

# Submit website
# The function performs the following steps:
#   - It retrieves the form input data as a list of words
#   - For each word in the input list, it translates the word and creates an example sentence
#   - If there's an exception during sentence creation, it renders the error website
#   - The translated words and example sentences are combined into a dictionary and stored in the session variable.
@app.route('/submit', methods=['POST'])
def submit():
    translated_words = []
    example_sentence = []
    input_value = request.form['text'].lower().split()

    for word in input_value:
        translated_words.append(word_translator(word).text)
        try:
            example_sentence.append(sentence_creator(word))
        except Exception as e:
            print(e)
            return render_template('error.html')

    combined_lists = dict(zip(input_value, translated_words))
    for index, key in enumerate(input_value):
        combined_lists[key] = combined_lists[key] + '   - ' + example_sentence[index]

    session['combined_lists'] = combined_lists

    return render_template('translated.html', words=combined_lists)

# This function is triggered when the user pushes the save button to store the data in a CSV file (database). It
# retrieves the combined list data from the session, which contains word-translation pairs, and appends the data to a
# CSV file named "voc-data.csv"
@app.route('/save', methods=['POST'])
def save_data():
    combined_lists = session.get('combined_lists', {})
    with open('voc-data.csv', mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        for word, translation in combined_lists.items():
            writer.writerow([word + "   - " + translation])
    return render_template('translated.html', words=combined_lists)

# This function shows the saved vocs history
# It reads the data from the CSV file and stores the rows in a list
@app.route('/show', methods=['POST'])
def show_data():
    list_of_rows = []
    with open('voc-data.csv', newline='', encoding='utf-8') as csv_file:
        csv_data = csv.reader(csv_file, delimiter='/')
        list_of_rows = [row for row in csv_data]
        print(list_of_rows)
    return render_template('show-data.html', data=list_of_rows)


if __name__ == '__main__':
    app.run(port=1347, debug=True)
