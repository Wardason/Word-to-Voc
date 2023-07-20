from flask import Flask, render_template, request

api_key = "apy_key"
print(api_key)

app = Flask(__name__)

@app.route("/")
def index():
        return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    input_value = request.form['text'].lower().split()
    print(input_value)
    return render_template('index.html')


if __name__ == '__main__':
    app.run(port=1347, debug=True)
