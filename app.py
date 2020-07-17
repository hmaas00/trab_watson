from flask import Flask, escape, render_template, request
from dictation import start_stream
from reading import start_reading
import time

app = Flask(__name__)

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/resposta')
def resposta():
    iteracoes = request.args['iteracoes']
    print(f"em resposta {type(iteracoes)}")
    iter = int(iteracoes)
    return render_template('resposta.html', iter=iter)

@app.route('/<name>')
def hello(name):
	return f'hello {escape(name)}!'

if __name__ == "__main__":
    app.run(host="127.0.0.1", port="5000", debug=True)