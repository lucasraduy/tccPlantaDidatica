import numpy as np
import csv
import time
import Adafruit_ADS1x15
import RPi.GPIO as gpio
import threading
import signal
from queue import Queue

gpio.setwarnings(False)
gpio.setmode(gpio.BOARD)

#*** Entradas e saídas do Raspberry ***
#Saída 1: pino 33
#Saída 2: pino 32
#Entrada 1: A0 do ADC
#Entrada 2: A1 do ADC
pino_saida1=33;
pino_saida2=32;

#offset 4mA IN1 = 8304
#offset 20mA IN1 = 26544

#offset 4mA IN2 = 7872
#offset 20mA IN2 = 26224

#Inicializa as duas saídas
gpio.setup(pino_saida1,gpio.OUT)
gpio.setup(pino_saida2,gpio.OUT)

saida1=gpio.PWM(pino_saida1,300)
saida2=gpio.PWM(pino_saida2,300)

saida1.start(0)
saida2.start(0)

# Ceia uma instancia do ADCADS1115 ADC (16-bit).
adc = Adafruit_ADS1x15.ADS1115()
GAIN = 1
values = [0]*4
for i in range(4):
    values[i] = adc.read_adc(i, gain=GAIN)
print('Entradas Analogicas: | {0:>6} | {1:>6} | {2:>6} | {3:>6} |'.format(*values))


#importa o sinal PRMLS
lista = np.genfromtxt("teste_3.csv",dtype="int", delimiter=",")

#Quantidade de amostras a serem realizadas
size_prmls=5
#Quantidade de amostrar por linhado PRMLS
n_repete=1000
#Quantidade total de linhas
linhas=size_prmls*n_repete
print('Quantidade de amostras:'+str(linhas))

#Cria um novo vetor para armazenar os dados coletados
lista2=np.zeros((linhas+1,5))
lista2[0,0]=time.time_ns()
s1=0
s2=0
out1=10
out2=10

exit_event = False
#Função que roda em um thread separado e realiza a
#leitura e escritas das entradas do raspberry
def worker(comm_thread):
    #obtem o timestamp do inicio da aquisição
    #usado para calcular o timestamp das aquisições
    print("Thread iniciada\n")
    while True:
        #Le os sinais do ADC
        th_in1=(adc.read_adc(0, gain=GAIN))
        th_in2=(adc.read_adc(1, gain=GAIN))
        
        #Envia para fora da thread os valores lidos
        comm_thread.put([time.time_ns(), th_in1, th_in2])
        
        #Desliga a thread
        if exit_event:
            break
#Fim da thread


#***** Programa princial *****
#Cria uma comunicação entre thread e programa principal
q1 = Queue()
#Cria um thread para realizar a leitura dos IOs
t = threading.Thread(target=worker, args=(q1, ))

#Inicia a thread
t.start()

#indice
k=1
#Realiza a aquisição
for i in range(0,size_prmls):
    print(lista[i,:])
    for j in range(0,n_repete):
#         print(k)
        
        #Recebe os sinais dos sensores lidos pela thread
        fila_thread=q1.get()
        timestamp_thread = fila_thread[0]
        in1 = fila_thread[1]
        in2 = fila_thread[2]
        
        #Timestamp
        lista2[k,0]=timestamp_thread
        
        #Entradas
        lista2[k,3]=in1
        lista2[k,4]=in2
        
        #escreve na saida 1
        s1=lista[i,0]
        lista2[k,1]=s1
        saida1.ChangeDutyCycle(s1)
        
        #escreve na saida 2
        s2=lista[i,1]
        lista2[k,2]=s2
        saida2.ChangeDutyCycle(s2)
            
        k=k+1
        
    print(lista2[k-1,:])
    print(k)

print("fim")
#Desliga a thread
exit_event=True
t.join()
print("Thread desligada")
# print(lista2)



#Salva os dados em um arquivo .csv para analise posterior
np.savetxt("aq3.csv",lista2,fmt="%d",delimiter=",")
