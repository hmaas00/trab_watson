from flask import Flask, escape, render_template, request

import requests
from requests.auth import HTTPBasicAuth
import time

import configparser
from ibm_watson import SpeechToTextV1
from ibm_watson.websocket import RecognizeCallback, AudioSource
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

import json

#carrega configuracoes
config = configparser.ConfigParser()
config.read('config.ini')
print('configurações:/n')
print(config['SPEECH2TEXT'])


#configura o speech2text
authenticator = IAMAuthenticator(config['SPEECH2TEXT']['API_KEY'])
speech_to_text = SpeechToTextV1(
   authenticator=authenticator)
speech_to_text.set_service_url(config['SPEECH2TEXT']['URL'])



app = Flask(__name__)

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/apresentar')
def resposta():
    iteracoes = request.args['iteracoes']
    print(f"em resposta {type(iteracoes)}")
    iter = int(iteracoes)
    return render_template('apresentacao.html', iter=iter)

@app.route('/ouvir')
def ouvir():

    print('chegou em ouvir')
    return render_template('ouvir.html')


@app.route('/interpretar', methods= ['GET','POST'])
def interpretar():

    print('chegou em interpretar')
    data = request.data
    print(type(data))
    
    """curl -X POST -u "apikey:{apikey}"
    --header "Content-Type: audio/flac"
    --data-binary @{path}audio-file.flac
    "{url}/v1/recognize"
    """

    " WATSON_STT_APIKEY=YOUR_API_KEY"

    #auth_var = HTTPBasicAuth('WATSON_STT_APIKEY', config['SPEECH2TEXT']['API_KEY'])
    auth_var = HTTPBasicAuth('apikey', config['SPEECH2TEXT']['API_KEY'])

    #?model=en-US_NarrowbandModel pt-BR_NarrowbandModel

    x = requests.post( 
        (config['SPEECH2TEXT']['URL'] + '/v1/recognize?model=pt-BR_NarrowbandModel'), 
        auth=auth_var,
        data = data, 
        headers = {"Content-Type": "audio/ogg; codecs=opus"})

    print('texto:')
    json_resposta = x.text
    print(json_resposta)
    print('interpretacao')

    interpretacao = json.loads(json_resposta, encoding='utf-8')['results'][0 ]['alternatives'][0]['transcript']
    print(interpretacao)

    '''curl -X POST -u "apikey:{apikey}" 
    --header "Content-Type: application/json" 
    --header "Accept: audio/wav" 
    --data "{\"text\":\"Hello world\"}" 
    --output hello_world.wav "{url}/v1/synthesize?voice=en-US_AllisonV3Voice"'''


    #auth_var = HTTPBasicAuth('WATSON_STT_APIKEY', config['SPEECH2TEXT']['API_KEY'])
    auth_var = HTTPBasicAuth('apikey', config['TEXT2SPEECH']['API_KEY'])

    #?model=en-US_NarrowbandModel pt-BR_NarrowbandModel

    fala = requests.post( 
        (config['TEXT2SPEECH']['URL'] + '/v1/synthesize?voice=pt-BR_IsabelaVoice'), 
        auth=auth_var,
        data = interpretacao, 
        headers = {"Content-Type": "application/json", "Accept":"audio/ogg; codecs=opus"})
        #headers = {"Content-Type": "audio/ogg; codecs=opus"})
    print("resposta do text2speech - tipo: ")
    print(type(fala.content))




    
    return 'interpretado!!!!'


@app.route('/<name>')
def hello(name):
	return f'hello {escape(name)}!'

if __name__ == "__main__":
    app.run(host="127.0.0.1", port="5000", debug=True)