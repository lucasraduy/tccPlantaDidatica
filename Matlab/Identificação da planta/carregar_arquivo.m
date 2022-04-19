function [data, timeStamp, dados] = carregar_arquivo(arquivo,Ts, plotar, titulo)
x_0=load(arquivo);
timestamp_ref=x_0(1,1);
timestamp_aq0=(x_0(2:end,1)-timestamp_ref).*10^-9;
time_period_aq0=(x_0(2:end,1)-x_0(1:end-1,1)).*10^-9;


in1_offset_max=26544;
in2_offset_max=26224;

in1_offset_min=8304;
in2_offset_min=7872;

out1=x_0(2:end,2);  %Válvula 1
out2=x_0(2:end,3);  %Válvula 2
out2_complementar=100-out2;
in1=(((x_0(2:end,4)-in1_offset_min)./in1_offset_max).*100); %Sensor 1
in2=(((x_0(2:end,5)-in2_offset_min)./in2_offset_max).*100); %Sensor 2

t_max=length(in1)*Ts;
t_s=(0:Ts:(t_max-Ts))';   %Vetor de tempo para o grafico

data=iddata([in1 in2],[out1 out2],Ts);
eixo=[0 300 -5 105];
if plotar
    figure
    subplot(211)
    sgtitle(titulo)
    plot(t_s',out1)
    hold on
    plot(t_s',in1)
    axis(eixo)
    hold off
    legend('Válvula','Vazão')
    ylabel('[%]')
    xlabel('Tempo [s]')
    title('Malha de vazão')
    
    subplot(212)
    plot(t_s',out2)
    hold on
    plot(t_s',in2)
    axis(eixo)
    hold off
    ylabel('[%]')
    xlabel('Tempo [s]')
    legend('Válvula','Nível')
    title('Malha de nível')
    
    saveas(gcf,strcat(titulo,'.svg'))
    
end
timeStamp=timestamp_aq0;

%       t    u1     u2   y1   y2
dados=[t_s, out1, out2, in1, in2];
end
