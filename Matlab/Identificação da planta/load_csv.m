

%% Aquisição 1 - Válvula da malha de vazão variando e válvula da malha de nível fixa em 100%

clear
close all
clc
Ts=0.0391; %s
x_0=load('AQ1.csv');
timestamp_aq0=x_0(:,1)*10^-9;


out1_aq0=x_0(:,3);
out2_aq0=x_0(:,2);
in1_aq0=x_0(:,4).*100;
in2_aq0=x_0(:,5).*100;

data1_aq0=iddata([in1_aq0(1:10000) in2_aq0(1:10000)],[out1_aq0(1:10000) out2_aq0(1:10000)],Ts);
data2_aq0=iddata([in1_aq0(10000:end) in2_aq0(10000:end)],[out1_aq0(10000:end) out2_aq0(10000:end)],Ts);

teste1_aq0=iddata([in1_aq0(1:10000)],[out1_aq0(1:10000)],Ts);
teste2_aq0=iddata([in1_aq0(10000:end)],[out1_aq0(10000:end)],Ts);

figure
subplot(211)
plot(out1_aq0)
hold on
plot(in1_aq0)
axis([0 20000 -5 105])
hold off
legend('Válvula','Vazão')
title('Malha de vazão')

subplot(212)
plot(out2_aq0)
hold on
plot(in2_aq0)
axis([0 20000 -5 105])
hold off
legend('Válvula','Nível')
title('Malha de nível')
%% 
Ts=0.0391;
x_1=load('aq1_out2_100.csv');

timestamp_aq1=(x_1(2:end,1)-x_1(1:end-1,1)).*10^-9;

out1_aq1=x_1(2:end,2);
out2_aq1=x_1(2:end,3);
in1_aq1=x_1(2:end,4);
in2_aq1=x_1(2:end,5);

data_1=iddata([in1_aq1 in2_aq1],[out1_aq1 out2_aq1],Ts);


x_2=load('aq2_out2_50.csv');

timestamp_aq2=(x_2(2:end,1)-x_2(1:end-1,1)).*10^-9;

out1_aq2=x_2(2:end,2);
out2_aq2=x_2(2:end,3);
in1_aq2=x_2(2:end,4);
in2_aq2=x_2(2:end,5);

data_2=iddata([in1_aq2 in2_aq2],[out1_aq2 out2_aq2],Ts);

% figure
% subplot(211)
% plot(out1_aq1)
% hold on
% plot(in1_aq1)
% axis([0 5000 -5 105])
% hold off
% legend('Válvula','Vazão')
% title('Malha de vazão')
% 
% subplot(212)
% plot(out2_aq1)
% hold on
% plot(in2_aq1)
% axis([0 5000 -5 105])
% hold off
% legend('Válvula','Nível')
% title('Malha de nível')
% sgtitle('Variação na saída 1, saída 2 fixa em 100%')
% saveas(gcf,'Aquisição 1.svg')


% figure
% plot(data)

% ARX: A(q)y(t)=B(q)u(t?nk)+e(t)

% na=[3, 3;
%     3, 3];
% 
% nb=[2, 2;
%     2, 2];
% 
% nk=[1, 0;
%     0, 1];
% 
% sys=arx(data, [na nb nk])
% 
% figure
% compare(data,sys)



% %% Aquisição 2 - Válvula da malha de vazão variando e válvula da malha de nível fixa em 50%
% x=load('aq2_out2_50.csv');
% 
% timestamp_aq2=(x(2:end,1)-x(1:end-1,1)).*10^-9;
% 
% % hist(timestamp)
% 
% out1_aq2=x(2:end,2);
% out2_aq2=x(2:end,3);
% in1_aq2=x(2:end,4);
% in2_aq2=x(2:end,5);
% 
% figure
% subplot(211)
% plot(out1_aq2)
% hold on
% plot(in1_aq2)
% axis([0 5000 -5 105])
% hold off
% legend('Válvula','Vazão')
% title('Malha de vazão')
% 
% subplot(212)
% plot(out2_aq2)
% hold on
% plot(in2_aq2)
% axis([0 5000 -5 105])
% hold off
% legend('Válvula','Nível')
% title('Malha de nível')
% sgtitle('Variação na saída 1, saída 2 fixa em 50%')
% 
% saveas(gcf,'Aquisição 2.svg')
% %% Aquisição 3 - Válvula da malha de vazão fixa em 50% e válvula da malha de nível variando
% x=load('aq3_out1_50.csv');
% 
% timestamp_aq3=(x(2:end,1)-x(1:end-1,1)).*10^-9;
% 
% % hist(timestamp)
% 
% out1_aq3=x(2:end,2);
% out2_aq3=x(2:end,3);
% in1_aq3=x(2:end,4);
% in2_aq3=x(2:end,5);
% 
% figure
% subplot(211)
% plot(out1_aq3)
% hold on
% plot(in1_aq3)
% axis([0 5000 -5 105])
% hold off
% legend('Válvula','Vazão')
% title('Malha de vazão')
% 
% subplot(212)
% plot(out2_aq3)
% hold on
% plot(in2_aq3)
% axis([0 5000 -5 105])
% hold off
% legend('Válvula','Nível')
% title('Malha de nível')
% sgtitle('Variação na saída 2, saída 1 fixa em 50%')
% saveas(gcf,'Aquisição 3.svg')
% 
% %% Aquisição 4 - Válvula da malha de vazão fixa em 80% e válvula da malha de nível variando
% x=load('aq4_out1_80.csv');
% 
% timestamp_aq4=(x(2:end,1)-x(1:end-1,1)).*10^-9;
% 
% % hist(timestamp)
% 
% out1_aq4=x(2:end,2);
% out2_aq4=x(2:end,3);
% in1_aq4=x(2:end,4);
% in2_aq4=x(2:end,5);
% 
% figure
% subplot(211)
% plot(out1_aq4)
% hold on
% plot(in1_aq4)
% axis([0 5000 -5 105])
% hold off
% legend('Válvula','Vazão')
% title('Malha de vazão')
% 
% subplot(212)
% plot(out2_aq4)
% hold on
% plot(in2_aq4)
% axis([0 5000 -5 105])
% hold off
% legend('Válvula','Nível')
% title('Malha de nível')
% sgtitle('Variação na saída 2, saída 1 fixa em 80%')
% saveas(gcf,'Aquisição 4.svg')
