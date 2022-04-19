clear all
close all
clc

m = modbus('tcpip', '10.2.0.100', 12345)

out1=0;
out2=0;


for i = 1:10000
    
    dadosEnviar = [out1 out2];
    write(m, 'holdingregs', 101, dadosEnviar)
    
    dadosRecebidos = read(m,'holdingregs', 201, 22);
    timeStampBytes=dadosRecebidos(1:8);
    timeStamp(i,1) = double(typecast(uint8(timeStampBytes),'uint64'))*10^-9;
    dadosRecebidos2 = read(m,'holdingregs', 301, 32);
%     disp(i)
    
end

%     t = datetime(timeStamp,'ConvertFrom','posixtime','TimeZone','America/Sao_Paulo');


t0=timeStamp(1);
TT0=ones(size(timeStamp))*t0;

tStart=timeStamp-TT0;
plot(tStart)

t1=tStart(1:end-1);
t2=tStart(2:end);
tt=t2-t1;

figure
plot(tt)
xlabel('Amostras')
ylabel('Tempo de aquisição (s)')
title('Tempo de aquisição Modbus')

figure
histogram(tt,25)
title('Tempo de aquisição Modbus')
xlabel('Tempo de aquisição (s)')
ylabel('Ocorrências')

