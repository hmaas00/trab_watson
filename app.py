from flask import Flask, escape, render_template
from dictation import start_stream
from reading import start_reading
import time

app = Flask(__name__)

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/resposta')
def resposta(blob):
    print(f"em resposta {type(blob)}")
    return 'hello !'

@app.route('/<name>')
def hello(name):
	return f'hello {escape(name)}!'

if __name__ == "__main__":
    app.run(host="127.0.0.1", port="5000", debug=True)