from dictation import start_stream
from reading import start_reading
import time

i = int(input('Escolha a quantidade de iterações entre 2 e 10: '))
while i < 2 or i > 10:
    i = int(input('Escolha a quantidade de iterações entre 2 e 10: '))

while i >= 0:
    print('Fale...')
    texto = start_stream()
    print('Ouça...')
    start_reading(texto)
    
    i -= 1
