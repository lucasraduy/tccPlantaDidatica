# encoding: utf-8

# Importa as bibliotecas necessarias
import time
import Adafruit_ADS1x15
import RPi.GPIO as gpio
import threading
import signal
import socket
import struct
import decimal
from queue import Queue
from pyModbusTCP.server import ModbusServer, DataBank
from simple_pid import PID
import sys


# Configura os pinos de IO
gpio.setwarnings(False)
gpio.setmode(gpio.BOARD)

#*** Entradas e saídas do Raspberry ***
#Saída 1: pino 33
#Saída 2: pino 32
#Entrada 1: A0 do ADC
#Entrada 2: A1 do ADC
pino_saida1=33;
pino_saida2=32;
chave = 16

in1_offset_max=26544
in1_offset_min=8304

in2_offset_max=26224
in2_offset_min=7872

#offset 4mA IN1 = 8304
#offset 20mA IN1 = 26544

#offset 4mA IN2 = 7872
#offset 20mA IN2 = 26224

#Inicializa as duas saídas
gpio.setup(pino_saida1,gpio.OUT)
gpio.setup(pino_saida2,gpio.OUT)
gpio.setup(chave,gpio.IN)

saida1=gpio.PWM(pino_saida1,300)
saida2=gpio.PWM(pino_saida2,300)
statusChave = gpio.input(chave)

saida1.start(0)
saida2.start(0) 

# Cria uma instancia do ADCADS1115 ADC (16-bit).
adc = Adafruit_ADS1x15.ADS1115()
GAIN = 1
values = [0]*4
for i in range(4):
    values[i] = adc.read_adc(i, gain=GAIN)
#print('Entradas Analogicas: | {0:>6} | {1:>6} | {2:>6} | {3:>6} |'.format(*values))

# Inicializa as variaveis utilizadas
out1=0
out2=0
in1=0
in2=0
timestamp_thread=0

#Função que roda em um thread separado e realiza a
#leitura e escritas das entradas do raspberry
exit_event = False
def worker(comm_thread):
    #obtem o timestamp do inicio da aquisição
    #usado para calcular o timestamp das aquisições
    print("Thread iniciada\n")
    while True:
        th_in1=(((adc.read_adc(0, gain=GAIN))-in1_offset_min)/in1_offset_max)*100
        th_in2=(((adc.read_adc(1, gain=GAIN))-in2_offset_min)/in2_offset_max)*100
        comm_thread.put([time.time_ns(), th_in1, th_in2])
        
        
        #Desliga a thread
        if exit_event:
            break
#Fim da thread

        
def dword_to_float(word1, word2):
    float_out, = struct.unpack('>f',b''.join([word1.to_bytes(2,'big'),word2.to_bytes(2,'big')]))
    return float_out

#Comunicação UDP
def commUDP():
    print('UDP')
    servidorUDP = False

    #Define o IP e porta para a comunicação UDP
    localIP="10.2.0.100"
    localPort=20001

    #Define a quantidade de bytes que podem ser recebidos
    bufferSize=1024
    #Inicia a thread
 
    timestp=time.time_ns()
    statusChave_loc = gpio.input(16)
    print("inicio loop")
    while(statusChave_loc):
        try:
            # Define o protocolo a ser utilizado, no caso UDP
            #AF_INET = Internet
            #SOCK_DGRAM = UDP
            UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

            # Configura o IP e porta para a comunicacao
            UDPServerSocket.bind((localIP, localPort))
            print("Servidor UDP ligado\n")
            UDPServerSocket.settimeout(1)
            #Servidor UDP ligado
            servidorUDP = True
            contador=0

        
            while(True):
                print("Aguardando receber dados para iniciar o envio\n")
                fila_thread=q1.get()
                timestamp_thread = fila_thread[0]
                print(timestamp_thread)
                #Recebe pacotes via UDP
                bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
                #Dados recebidos via UDP
                message = bytesAddressPair[0]
                #Endereco IP que enviou dados para o raspberry
                address = bytesAddressPair[1]
                print(message)
                clientIP  = "Client IP Address:{}".format(address)
            #     print(clientIP)
            #     print(address)
                #Converte os bytes recebidos em um tuple de floats
                messageFloat=struct.unpack(">ff",message)
                print(messageFloat)
                #Arruma os valores recebidos para ter apenas 3 casas decimais
                out1_UDP_f=round(decimal.Decimal(messageFloat[0]),3)
                out2_UDP_f=round(decimal.Decimal(messageFloat[1]),3)
            #     address=('10.2.0.110', 53645)
                time1=time.time_ns()
                
                while True:            
                    statusChave_loc2 = gpio.input(chave)
                    #Termina a comunicacao
                    if statusChave_loc2 == False:
                        UDPServerSocket.close()
                        print('Servidor UDP desligado')
                        break
                   
                   #Tratamento dos dados recebidos
                    if (out1_UDP_f >= 100.0):
                        out1_UDP_f = 100.0
                        
                    if (out2_UDP_f >= 100.0):
                        out2_UDP_f = 100.0
                        
                    if (out1_UDP_f <= 0.0):
                        out1_UDP_f = 0.0
                        
                    if (out2_UDP_f <= 0.0):
                        out2_UDP_f = 0.0
                        
                    
                    #Valores para escrever na saida recebidos via UDP
                    out1=out1_UDP_f
                    out2=out2_UDP_f
                    
                    #Escreve na saida PWM os valores recebidos via UDP
                    saida1.ChangeDutyCycle(out1)
                    saida2.ChangeDutyCycle(out2)
                    
                    #Recebe os sinais dos sensores lidos pela thread
                    fila_thread=q1.get()
                    timestamp_thread = fila_thread[0]
                    in1 = fila_thread[1]
                    in2 = fila_thread[2]

                    #Vetor de variaveis a serem enviadas
                    dadosEnviaUDP=[timestamp_thread, in1, in2, out1, out2]
                    
                    #Converte as variaveis do tipo float para bytes
                    bytesToSend=bytearray(struct.pack("Qffff", dadosEnviaUDP[0], dadosEnviaUDP[1], dadosEnviaUDP[2], dadosEnviaUDP[3], dadosEnviaUDP[4]))

                    # Envia dados via UDP para o endereco que solicitou
                    UDPServerSocket.sendto(bytesToSend, address)
                    
                    #Recebe pacotes via UDP
                    bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
                    #Dados recebidos via UDP
                    message = bytesAddressPair[0]
                    #Endereco IP que enviou dados para o raspberry
                    address = bytesAddressPair[1]
                    #Converte os bytes recebidos em um tuple de floats
                    messageFloat=struct.unpack(">ff",message)
                    #Arruma os valores recebidos para ter apenas 3 casas decimais
                    out1_UDP_f=round(decimal.Decimal(messageFloat[0]),1)
                    out2_UDP_f=round(decimal.Decimal(messageFloat[1]),1)
                    
                    print(dadosEnviaUDP)
                    contador+=1

        except socket.timeout:
            print("UDP: Sem conexão")
            if(gpio.input(chave)):
                continue
            else:
                UDPServerSocket.close()
                break
        except:
            print("UDP: Erro")
            break
        
    print('UDP desligado')
    UDPServerSocket.close()
    #Desliga a thread
    exit_event=True
    #q1.join()
    #t.join()

                    
def commModbus():
    print('funcao Modbus')
    
    #Cria uma instancia do ModbusServer
    server=ModbusServer("10.2.0.100",port=12345,no_block=True,ipv6=False )

    try:
        
        pid1 = PID(1, 0.1, 0.05, setpoint=1)
        pid2 = PID(1, 0.1, 0.05, setpoint=1)
        
        pid1.output_limits = (0, 100)
        pid2.output_limits = (0, 100)
        
        pid1.sample_time = 0.01
        pid2.sample_time = 0.01
        
        print("Iniciando servidor Modbus")
        server.start()
        print("Servidor Modbus iniciado")

        while (gpio.input(chave) == False):
            
            #Recebe os dados via Modbus
            dadosRecebidos = DataBank.get_words(100,16)
            modoOperacao = DataBank.get_words(500,1)
            
            #Organiza os dados recebidos
            setpoint1 = int(dword_to_float(dadosRecebidos[0],dadosRecebidos[1]))
            setpoint2 = int(dword_to_float(dadosRecebidos[2],dadosRecebidos[3]))    
            
            Kp1=dword_to_float(dadosRecebidos[4], dadosRecebidos[5])    
            Ti1=dword_to_float(dadosRecebidos[6], dadosRecebidos[7])
            Td1=dword_to_float(dadosRecebidos[8], dadosRecebidos[9])
            
            Kp2=dword_to_float(dadosRecebidos[10], dadosRecebidos[11])
            Ti2=dword_to_float(dadosRecebidos[12], dadosRecebidos[13])
            Td2=dword_to_float(dadosRecebidos[14], dadosRecebidos[15])
             
            #Recebe os sinais dos sensores lidos pela thread
            fila_thread=q1.get()
            timestamp_thread = int(fila_thread[0])
            in1 = int(fila_thread[1])
            in2 = int(fila_thread[2])
            
            #in1=setpoint1
            #in2=setpoint2
            
            if modoOperacao[0]==1:
                pid1.auto_mode = True
                pid1.tunings = (Kp1,Ti1,Td1)
                pid2.tunings = (Kp2,Ti2,Td2)
                
                pid1.setpoint = setpoint1
                pid2.setpoint = setpoint2
                
                out1=pid1(in1)
                out2=pid2(in2)
                s1=[Kp2,Ti2,Td2, in2, setpoint2,out2]
#                 print(s1)
            else:
                out1=setpoint1
                out2=setpoint2
            #Tratamento dos dados recebidos
            if (out1 >= 100.0):
                out1 = 100.0
                
            if (out2 >= 100.0):
                out2 = 100.0
                
            if (out1 <= 0.0):
                out1 = 0.0
                
            if (out2 <= 0.0):
                out2 = 0.0
                
            #Escreve na saida PWM os valores recebidos via UDP
            saida1.ChangeDutyCycle(out1)
            saida2.ChangeDutyCycle(out2)
            
            #Prepara o vetor de dados a serem enviados
            itimestamp_thread= int(timestamp_thread)
            x=itimestamp_thread.to_bytes(22, byteorder='little')        
           
            #Envia os dados via modbus
            DataBank.set_words(200,x)
            DataBank.set_words(300,[in1])
            DataBank.set_words(301,[in2])
            DataBank.set_words(302,[out1])
            DataBank.set_words(303,[out2])

    except:
        
        print("Desligando servidor Modbus")
        server.stop()
        print("Servidor Modbus Desligado")
    
    print("Desligando servidor Modbus")
    server.stop()
    print("Servidor Modbus Desligado")

#***** Programa princial *****
udpAtivo = False
modbusAtivo = False
#Cria uma comunicação entre thread e programa principal
q1 = Queue()
#Cria um thread para realizar a leitura dos IOs
t = threading.Thread(target=worker, args=(q1, ))

t.start()

print('inicia o monitoramento da chave')
#Cria um thread para realizar a leitura dos IOs
#gpio.add_event_detect(chave,gpio.BOTH , callback=monitoraChave, bouncetime=300)

while True:
    #le o sinal da chave de seleção
    statusChave = gpio.input(16)

    if(statusChave):
        #Chave ligada: modo UDP
        if(udpAtivo == False):
            print('UDP selecionado')
            commUDP()
            udpAtivo = True
        else:
            print('UDP ja selecionado')
        
    else:
        #Chave desligada: modo Modbus
        if(udpAtivo):
                                
            print('Modbus')
            commModbus()
            udpAtivo = False
        else:
            if(modbusAtivo):
                print('Modbus ativo')
            else:
                commModbus()
                print('Modbus Iniciado')
