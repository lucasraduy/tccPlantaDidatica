function [] = plotarMimo(t_s,u,y)

 figure
    subplot(211)
%     sgtitle(titulo)
    plot(t_s,u(:,1))
    hold on
    plot(t_s,y(:,1))
    
    hold off
    legend('Válvula','Vazão')
    ylabel('[%]')
    xlabel('Tempo [s]')
    title('Malha de vazão')
    
    subplot(212)
    plot(t_s,u(:,2))
    hold on
    plot(t_s,y(:,2))
    
    hold off
    ylabel('[%]')
    xlabel('Tempo [s]')
    legend('Válvula','Nível')
    title('Malha de nível')


end