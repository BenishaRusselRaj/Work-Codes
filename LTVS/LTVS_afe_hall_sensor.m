%% LTVS
f = "D:\Benisha\LTVS\10kWh\Re_In_house_testing\New_Cycles\Farhan_Testing\06-09-2024\LTVS_10kWh_pack_current_test_06-09-2024_BMS\LTVS_10kWh_pack_current_test_06-09-2024_BMS_modified_dlog_merged.xlsx";

data = readtable(f, 'Sheet', 'Hall Sensor data');

%%
date = "06_09_2024";
t_no = "AFE_test";

c = 'LTVS_'+t_no+"_"+date;
%%
% f1="D:\Benisha\LTVS\Mosfet_Test\Plot\"+c+"_dlog.png";
% f2="D:\Benisha\LTVS\Mosfet_Test\Plot\"+c+"_dlog_and_bms.png";
% 
% m1="D:\Benisha\LTVS\Mosfet_Test\Plot\"+c+"_dlog.fig";
% m2="D:\Benisha\LTVS\Mosfet_Test\Plot\"+c+"_dlog_and_bms.fig";

%% 

f1="D:\Benisha\LTVS\10kWh\Re_In_house_testing\New_Cycles\Farhan_Testing\Plots\"+c+"_dlog.png";
f2="D:\Benisha\LTVS\10kWh\Re_In_house_testing\New_Cycles\Farhan_Testing\Plots\"+c+"_dlog_and_bms.png";
f3="D:\Benisha\LTVS\10kWh\Re_In_house_testing\New_Cycles\Farhan_Testing\Plots\"+c+"_complete.png";

m1="D:\Benisha\LTVS\10kWh\Re_In_house_testing\New_Cycles\Farhan_Testing\Plots\"+c+"_dlog.fig";
m2="D:\Benisha\LTVS\10kWh\Re_In_house_testing\New_Cycles\Farhan_Testing\Plots\"+c+"_dlog_and_bms.fig";
m3="D:\Benisha\LTVS\10kWh\Re_In_house_testing\New_Cycles\Farhan_Testing\Plots\"+c+"_complete.fig";

%%
afe = data.AFE_GPIO_instant_value;
pack_hs = data.SS_1;
pack_hs_2 = data.SS_2;
ext_hs = data.External_Hall_Sensor;
ext_t = data.Temperature_on_External_Hall_Sensor;
amb_t = data.Ambient_Temperature;
rt = data.RT;
current = data.Approximated_Current;

dt = (1:1:height(data));

%%
figure;
subplot(2, 1, 1);

plot(dt,afe, 'LineWidth', 1, 'DisplayName','AFE GPIO instant value');
hold on;
plot(dt,pack_hs, 'LineWidth', 1, 'DisplayName','SS1');
plot(dt,pack_hs_2, 'LineWidth', 1, 'DisplayName','SS2');
title('Hall Sensor and AFE GPIO Data');
% xlabel('Time'); %DT
ylabel('Voltage (V)');
% ylim([-30,5])
grid on;
hold off;

% Add legend
legend('Location', 'northeast');

subplot(2, 1, 2);
plot(dt, ext_t, 'LineWidth', 1, 'DisplayName','External Hall Sensor Temperature');
hold on;
plot(dt, amb_t, 'LineWidth', 1, 'DisplayName','Ambient Temperature');
plot(dt, rt, 'LineWidth', 1, 'DisplayName','Relay Temperature');
title('Temperature');
% xlabel('Time'); %DT
ylabel('Temperature (degC)');
% ylim([-0.5, 1.5]);
grid on;
hold off;
legend('Location', 'northwest');


% t2=sgtitle('Hall Sensor Data');
% t2.FontWeight='bold';

linkaxes([subplot(2, 1, 1) subplot(2, 1, 2) ], 'x');


% l1=gcf;
% exportgraphics(l1,f1,'Resolution',600);
% savefig(m1);

%%
figure;
subplot(2, 1, 1);

plot(dt, ext_hs, 'LineWidth', 1, 'DisplayName','External Hall Sensor');
hold on;
plot(dt,pack_hs, 'LineWidth', 1, 'DisplayName','SS1');
plot(dt,pack_hs_2, 'LineWidth', 1, 'DisplayName','SS2');
title('Datalogger Hall Sensor Data');
% xlabel('Time'); %DT
ylabel('Voltage (V)');
% ylim([-0.5, 1.5]);
grid on;
hold off;
legend('Location', 'northeast');

subplot(2, 1, 2);
plot(dt, ext_t, 'LineWidth', 1, 'DisplayName','External Hall Sensor Temperature');
hold on;
plot(dt, amb_t, 'LineWidth', 1, 'DisplayName','Ambient Temperature');
plot(dt, rt, 'LineWidth', 1, 'DisplayName','Relay Temperature');
title('Temperature');
% xlabel('Time'); %DT
ylabel('Temperature (degC)');
% ylim([-0.5, 1.5]);
grid on;
hold off;
legend('Location', 'northwest');

linkaxes([subplot(2, 1, 1) subplot(2, 1, 2) ], 'x');

 
% t2=sgtitle('External Hall Sensor Data');
% t2.FontWeight='bold';

% l2=gcf;
% exportgraphics(l2,f2,'Resolution',600);
% savefig(m2);

%%
figure;
subplot(2, 1, 1);

yyaxis left;
plot(dt, ext_hs, 'LineWidth', 1, 'DisplayName','External Hall Sensor');
hold on;
plot(dt,afe, 'LineWidth', 1, 'DisplayName','AFE GPIO instant value');
plot(dt,pack_hs, 'LineWidth', 1, 'DisplayName','SS1');
plot(dt,pack_hs_2, 'LineWidth', 1, 'DisplayName','SS2');
title('Hall Sensor Data');
% xlabel('Time'); %DT
ylabel('Voltage (V)');
% ylim([-0.5, 1.5]);
xlim([0,height(afe)+2000])
colororder(["#0072BD";"#EDB120";"#D95319";"#77AC30"])
grid on;
hold off;

yyaxis right;
plot(dt, current, 'LineWidth', 1, 'DisplayName','Current');
ylabel('Current (A)');
ylim([-120,120]);
legend('Location', 'northeast');

subplot(2, 1, 2);
plot(dt, ext_t, 'LineWidth', 1, 'DisplayName','External Hall Sensor Temperature');
hold on;
plot(dt, amb_t, 'LineWidth', 1, 'DisplayName','Ambient Temperature');
plot(dt, rt, 'LineWidth', 1, 'DisplayName','Relay Temperature');
title('Temperature');
% xlabel('Time'); %DT
ylabel('Temperature (degC)');
% ylim([-0.5, 1.5]);
grid on;
hold off;
legend('Location', 'northwest');

linkaxes([subplot(2, 1, 1) subplot(2, 1, 2) ], 'x');


% l3=gcf;
% exportgraphics(l3,f3,'Resolution',600);
% savefig(m3);