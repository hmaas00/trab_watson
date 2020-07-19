from flask import Flask, escape, render_template, request, url_for
import requests
from requests.auth import HTTPBasicAuth
import time
import configparser
from ibm_watson import SpeechToTextV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import json
import re

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
	return render_template('ouvir.html')

@app.route('/interpretar', methods= ['GET','POST'])
def interpretar():
    data = request.data
    
    auth_var = HTTPBasicAuth('apikey', config['SPEECH2TEXT']['API_KEY'])

    x = requests.post( 
        (config['SPEECH2TEXT']['URL'] + '/v1/recognize?model=pt-BR_NarrowbandModel'), 
        auth=auth_var,
        data = data, 
        headers = {"Content-Type": "audio/ogg; codecs=opus"})

    json_resposta = x.text
    
    interpretacao = json.loads(json_resposta, encoding='utf-8')['results'][0 ]['alternatives'][0]['transcript']
    print('interpretacao: ', interpretacao)
    texto = re.sub(r'[^ a-zA-ZãÃáÁàÀâÂçÇéÉêÊíÍõÕóÓôÔúÚ]', "", interpretacao)
    comAcentos = "ÄÅÁÂÀÃäáâàãÉÊËÈéêëèÍÎÏÌíîïìÖÓÔÒÕöóôòõÜÚÛüúûùÇç"
    semAcentos = "AAAAAAaaaaaEEEEeeeeIIIIiiiiOOOOOoooooUUUuuuuCc"
    
    print('velho: ', texto)
    for i, l in enumerate(texto):
        if l in comAcentos:
            x = comAcentos.index(l)
            y = semAcentos[x]
            texto = texto.replace(texto[i], y)

    print('novo: ', texto)
    auth_var = HTTPBasicAuth('apikey', config['TEXT2SPEECH']['API_KEY'])

    print("{\"text\":\"" + texto + "\"}")
    fala = requests.post( 
        (config['TEXT2SPEECH']['URL'] + '/v1/synthesize?voice=pt-BR_IsabelaV3Voice'),
        auth=auth_var,
        data = "{\"text\":\"" + texto + "\"}",
        headers = {"Content-Type": "application/json", "Accept":"audio/ogg; codecs=opus"})
    
    with open("static/fala_watson.ogg", "wb") as f:
        f.write(fala.content)

    return fala.content

if __name__ == "__main__":
    app.run(host="127.0.0.1", port="5000", debug=True)