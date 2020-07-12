from flask import Flask, escape
from dictation import start_stream
from reading import start_reading
import time

app = Flask(__name__)

@app.route('/')
def index():
	return '''<h1 style="text-align: center;">Brincando de telefone sem fio com o IBM Watson</h1>
		<form action="/action_page.php">
		<p style="text-align: center;"><label for="size">Escolha o n&uacute;mero de rodadas:</label></p>
		<select id="size" name="size">
		<option selected="selected" value="2">2</option>
		<option value="4">4</option>
		<option value="6">6</option>
		<option value="8">8</option>
		<option value="10">10</option>
		</select>
		<p style="text-align: center;"><input type="submit" value="GRAVAR!" /></p>
		</form>'''

@app.route('/<name>')
def hello(name):
	return f'hello {escape(name)}!'

if __name__ == "__main__":
    app.run(host="127.0.0.1", port="5000", debug=True)