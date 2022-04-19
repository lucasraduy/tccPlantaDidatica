function [] = plotarMimo(t_s,u,y)

 figure
    subplot(211)
%     sgtitle(titulo)
    plot(t_s,u(:,1))
    hold on
    plot(t_s,y(:,1))
    
    hold off
    legend('V�lvula','Vaz�o')
    ylabel('[%]')
    xlabel('Tempo [s]')
    title('Malha de vaz�o')
    
    subplot(212)
    plot(t_s,u(:,2))
    hold on
    plot(t_s,y(:,2))
    
    hold off
    ylabel('[%]')
    xlabel('Tempo [s]')
    legend('V�lvula','N�vel')
    title('Malha de n�vel')


end