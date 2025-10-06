%% LTVS mogambo board

f = "D:\Benisha\LTVS\Mosfet_Test\mosfet_test\mosfet_test_modified.xlsx";

d_current = readtable(f, 'Sheet', 'Pack Details');
d_fet = readtable(f,'Sheet', 'Relay Status');
d_c_current = readtable(f, 'Sheet', 'Compensated Current');

%%
date = "02_09_2024";
t_no = "";

c = 'LTVS_'+t_no+"_"+date;
%%
f1="D:\Benisha\LTVS\Mosfet_Test\Plot\"+c+"_discharge_fet.png";
f2="D:\Benisha\LTVS\Mosfet_Test\Plot\"+c+"_charge_fet.png";

m1="D:\Benisha\LTVS\Mosfet_Test\Plot\"+c+"_discharge_fet.fig";
m2="D:\Benisha\LTVS\Mosfet_Test\Plot\"+c+"_charge_fet.fig";

%%
% pc = (d_c_current.CompensatedCurrent_mA_)*0.001;
pc = (d_current.Pack_Current)*0.001;
dchg_fet = d_fet.Discharge_Relay;
dchg_pre_fet = str2double(d_fet.Pre_discharge);
chg_fet = d_fet.Charge_Relay;
chg_pre_fet = str2double(d_fet.Precharge);

dt = (1:1:height(d_current));
% dt = (1:1:height(d_c_current));
dt_f = (1:1:height(d_fet));

%%
figure;
subplot(3, 1, 1);

plot(dt,pc, 'LineWidth', 1, 'DisplayName','Pack Current');
% plot(elapsedTime, T1, 'y-', 'LineWidth', 1, 'DisplayName','Cell tester thermocouple _ Cell Centre')
title('Pack Current');
% xlabel('Time'); %DT
ylabel('Current (A)');

ylim([-30,5])
grid on;
hold off;

% Add legend
legend('Location', 'east','NumColumns',4,'FontSize',7);

subplot(3, 1, 2);
plot(dt_f, dchg_pre_fet, 'LineWidth', 1, 'DisplayName','Pre-discharge Relay');
title('Pre-discharge Relay');
% xlabel('Time'); %DT
% ylabel('Voltage (mV)');
ylim([-0.5, 1.5]);
grid on;
legend('Location', 'northwest');

subplot(3, 1, 3);
plot(dt_f, dchg_fet, 'LineWidth', 1, 'DisplayName','Discharge Relay');
title('Discharge Relay');
% xlabel('Time'); %DT
% ylabel('Voltage (mV)');
ylim([-0.5, 1.5]);
grid on;
legend('Location', 'northwest');


t2=sgtitle('Pack Current and Discharge Relay');
t2.FontWeight='bold';

linkaxes([subplot(3, 1, 1) subplot(3, 1, 2) subplot(3, 1, 3)], 'x');


% l1=gcf;
% exportgraphics(l1,f1,'Resolution',600);
% savefig(m1);

%%
figure;
subplot(3, 1, 1);

plot(dt,pc, 'LineWidth', 1, 'DisplayName','Pack Current');
% plot(elapsedTime, T1, 'y-', 'LineWidth', 1, 'DisplayName','Cell tester thermocouple _ Cell Centre')
title('Pack Current');
% xlabel('Time'); %DT
ylabel('Current (A)');

ylim([-30,5])
grid on;
hold off;

% Add legend
legend('Location', 'east','NumColumns',4,'FontSize',7);

subplot(3, 1, 2);
plot(dt_f, chg_pre_fet, 'LineWidth', 1, 'DisplayName','Pre-charge Relay');
title('Pre-charge Relay');
% xlabel('Time'); %DT
% ylabel('Voltage (mV)');
ylim([-0.5, 1.5]);
grid on;
legend('Location', 'northwest');

subplot(3, 1, 3);
plot(dt_f, chg_fet, 'LineWidth', 1, 'DisplayName','Charge Relay');
title('Charge Relay');
% xlabel('Time'); %DT
% ylabel('Voltage (mV)');
ylim([-0.5, 1.5]);
grid on;
legend('Location', 'northwest');


t2=sgtitle('Pack Current and Charge Relay');
t2.FontWeight='bold';

linkaxes([subplot(3, 1, 1) subplot(3, 1, 2) subplot(3, 1, 3)], 'x');

% l2=gcf;
% exportgraphics(l2,f2,'Resolution',600);
% savefig(m2);