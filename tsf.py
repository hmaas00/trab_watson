from dictation import start_stream
from reading import start_reading
import time

i = int(input('Escolha a quantidade de iterações entre 2 e 10: '))
while i < 2 or i > 10:
    i = int(input('Escolha a quantidade de iterações entre 2 e 10: '))

s = int(input('Defina a duração do áudio entre 3 e 7 segundos: '))
while s < 3 or s > 7:
    s = int(input('Defina a duração do áudio entre 3 e 7 segundos: '))

while i >= 0:
    print('Fale...')
    start_stream(s)
    print('Ouça...')
    start_reading()
    
    i -= 1
