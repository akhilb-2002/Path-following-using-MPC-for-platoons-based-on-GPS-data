% Route plot

xhistory = readmatrix('xhistory.csv');
tabdata = readmatrix('tabdata.csv');
plotmap = readmatrix('Routenew.csv');

xlist= tabdata(1:101,1);
ylist = tabdata(1:101,2);

plot(plotmap(:,1),plotmap(:,2),'--');
t0=title('Hyderabad to Chennai plot');
x0=xlabel('$X (m)$');
y0=ylabel('$Y (m)$');
set(t0,'Interpreter','latex')
set(x0,'Interpreter','latex')
set(y0,'Interpreter','Latex')

figure;

subplot(4,1,1)
plot(xhistory(1,:), xhistory(2,:),'--');
hold on;
plot(xhistory(7,:), xhistory(8,:));
hold on;
plot(xhistory(13,:), xhistory(14,:),'--');
hold on;
plot(xhistory(19,:), xhistory(20,:));
hold on;
plot(xlist, ylist, '--');
hold on;
t1=title('(i)');
x1=xlabel('$X (m)$');
y1=ylabel('$Y (m)$');
leg1=legend('Vehicle 1', 'Vehicle 2', 'Vehicle 3', 'Vehicle 4', 'Reference trajectory');
set(t1,'Interpreter','latex')
set(x1,'Interpreter','latex')
set(y1,'Interpreter','Latex')
set(leg1,'Interpreter','latex');
set(leg1,'FontSize',5)
hold off;

t= 100;
subplot(4,1,2)
% 5. Plot of xdot vs time for all vehicles with legend 
plot(xhistory(3,1:t), '--');
hold on;
plot(xhistory(9, 1:t));
plot(xhistory(15,1:t), '--');
plot(xhistory(21, 1:t));
t2=title('(ii)');
x2=xlabel('$t (s)$');
y2=ylabel('$\dot x (m/s)$');
leg2=legend('Vehicle 1', 'Vehicle 2', 'Vehicle 3', 'Vehicle 4');
set(t2,'Interpreter','latex')
set(x2,'Interpreter','latex')
set(y2,'Interpreter','Latex')
set(leg2,'Interpreter','latex');
set(leg2,'FontSize',5)
hold off;

% 6. Plot of ydot vs time for all vehicles with legend
subplot(4, 1, 3);
plot(xhistory(4,1:t), '--');
hold on;
plot(xhistory(10, 1:t));
plot(xhistory(16, 1:t), '--');
plot(xhistory(22, 1:t));
t3=title('(iii)');
x3=xlabel('$t (s)$');
y3=ylabel('$\dot y (m/s)$');
leg3=legend('Vehicle 1', 'Vehicle 2', 'Vehicle 3', 'Vehicle 4');
set(t3,'Interpreter','latex')
set(x3,'Interpreter','latex')
set(y3,'Interpreter','Latex')
set(leg3,'Interpreter','latex');
set(leg3,'FontSize',5)
hold off;

subplot(4, 1, 4);
plot(xhistory(5,1:t), '--');
hold on;
plot(xhistory(11, 1:t));
plot(xhistory(17, 1:t), '--');
plot(xhistory(23, 1:t));
t4=title('(iv)');
x4=xlabel('$t (s)$');
y4=ylabel('$\psi (rad/s)$');
leg4=legend('Vehicle 1', 'Vehicle 2', 'Vehicle 3', 'Vehicle 4');
set(t4,'Interpreter','latex')
set(x4,'Interpreter','latex')
set(y4,'Interpreter','Latex')
set(leg4,'Interpreter','latex');
set(leg4,'FontSize',5)
hold off;
