
clear all
close all
clc

inputArray=(load('inputSignal.csv'));
% plot(inputArray)
nAmostras=500;
indexSaida=1;
lastIndex=1;
%Cria um cliente udp e inicia a comunicação enviando os primeiros valores
u = udp('10.2.0.100',20001);
fopen(u);
fwrite(u,inputArray(1,:),'float32')


% fwrite(u,x,'float32')

i=1;
contador_Erro=0;
pause(2)
while true
    
    %Le os dados enviados via UDP
    A = fread(u,16,'uint8');
    
    %Se o vetor lido esta vazio, gera um erro
    if isempty(A)
        fprintf('Erro\n')
        contador_Erro=contador_Erro+1;
    else
        
        %Trata os dados lidos;
        C=uint8(A);
        if length(C)<24
            C=[C;zeros(24-length(C),1)]
            
        end
        dataBytes=C(9:end);
        
        %Timestamp o momento da aquisição
        timeStampBytes=C(1:8);
        timeStamp(i)=double(typecast(timeStampBytes,'int64'))*10^-9;
        t = datetime(timeStamp,'ConvertFrom','posixtime','TimeZone','America/Sao_Paulo');
        
        y_rec(i,:) = typecast(dataBytes, 'single');
        
             
        
        
        fwrite(u,inputArray(indexSaida,:),'float32');
        
        fprintf('\nTimestamp: %s\n Setpoint: %f; Vazão: %f\n Setpoint: %f; Nivel: %f\n', t(i),y_rec(i,3),y_rec(i,1),y_rec(i,4),y_rec(i,2))
        
        inputVector(i,:)=inputArray(indexSaida,:);
        
        
        %Incrementa a quantidade de pontos lidos
        i=i+1;
        
        
        
        if indexSaida<length(inputArray)
            indexSaida=fix(i/nAmostras)+1;
        else
            break
        end
    end
    
    if contador_Erro > 10
        disp('10 erros, cancelando comunicação')
        break
    end
end
disp("Fim")
fwrite(u,[999,999],'float32');
% tmstp=(timeStamp-timeStamp(1)).*(10^9);
tmstp=(timeStamp-timeStamp(1));
stem(tmstp)
%
% 
% Ts(1)=0;
% for j=2:length(tmstp)
%     Ts(j)=tmstp(j)-tmstp(j-1);
%     
% end
% figure
% plot(Ts)

y=double(y_rec(:,1:2));
plotarMimo(tmstp',inputVector,y(:,1:2))
