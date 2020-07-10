from __future__ import print_function
import pyaudio
from ibm_watson import SpeechToTextV1
from ibm_watson.websocket import RecognizeCallback, AudioSource
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from threading import Thread, Timer
import configparser
import time

try:
    from Queue import Queue, Full
except ImportError:
    from queue import Queue, Full

#carrega configuracoes
config = configparser.ConfigParser()
config.read('config.ini')
print(config['SPEECH2TEXT'])

###############################################
#### inicia fila para gravar as gravacoes do microfone ##
###############################################
CHUNK = 1024
# Nota: gravacoes sao descartadas caso o websocket nao consuma rapido o suficiente
# Caso precise, aumente o max size conforme necessario
BUF_MAX_SIZE = CHUNK * 10
# Buffer para guardar o audio
q = Queue(maxsize=int(round(BUF_MAX_SIZE / CHUNK)))

# Cria o audio source com a fila
audio_source = AudioSource(q, True, True)

#configura o speech2text
authenticator = IAMAuthenticator(config['SPEECH2TEXT']['API_KEY'])
speech_to_text = SpeechToTextV1(
   authenticator=authenticator)
speech_to_text.set_service_url(config['SPEECH2TEXT']['URL'])

resultado = ''

# classe de callback para o servico de reconhecimento de voz
class MyRecognizeCallback(RecognizeCallback):
    
    def __init__(self):
        RecognizeCallback.__init__(self)

    def on_transcription(self, transcript):
        pass

    def on_connected(self):
        print('Conexão OK')

    def on_error(self, error):
        print('Erro recebido: {}'.format(error))

    def on_inactivity_timeout(self, error):
        print('Timeout de inatividade: {}'.format(error))

    def on_listening(self):
        print('Serviço está ouvindo, aperte q + Enter para finalizar')

    def on_hypothesis(self, hypothesis):
        pass

    def on_data(self, data):
        global resultado
        print('Texto detectado: ')
        for result in data['results']:
            resultado = (result['alternatives'][0]['transcript']) #Como gravar essa saída para uso na função start_reading em tsf.py?
        

    def on_close(self):
        print("Conexão fechada")

# inicia o reconhecimento usando o audio_source
def recognize_using_websocket(*args):
    mycallback = MyRecognizeCallback()
    speech_to_text.recognize_using_websocket(audio=audio_source,
                                             content_type='audio/l16; rate=44100',
                                             recognize_callback=mycallback,
                                             model='pt-BR_NarrowbandModel',
                                             interim_results=False)

###############################################
#### Prepara gravacao usando pyaudio ##
###############################################

# Config do pyaudio para as gravacoes
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100

# define callback para gravar o audio na fila
def pyaudio_callback(in_data, frame_count, time_info, status):
    try:
        q.put(in_data)
    except Full:
        pass # discard
    return (None, pyaudio.paContinue)

def start_stream():
    global resultado
    # instancia pyaudio
    audio = pyaudio.PyAudio()

    # abre stream
    stream = audio.open(
        format=FORMAT,
        channels=CHANNELS,
        rate=RATE,
        input=True,
        frames_per_buffer=CHUNK,
        stream_callback=pyaudio_callback,
        start=False
    )

    #########################################################################
    #### Start the recording and start service to recognize the stream ######
    #########################################################################

    stream.start_stream()

    try:
        recognize_thread = Thread(target=recognize_using_websocket, args=())
        recognize_thread.start()

        command = ''
        while command != 'q':
            command = input()

        # para gravacao
        audio_source.completed_recording()
        stream.stop_stream()
        stream.close()
        audio.terminate()
        recognize_thread.join()
        return resultado

    except KeyboardInterrupt:
        # para gravacao
        audio_source.completed_recording()
        stream.stop_stream()
        stream.close()
        audio.terminate()