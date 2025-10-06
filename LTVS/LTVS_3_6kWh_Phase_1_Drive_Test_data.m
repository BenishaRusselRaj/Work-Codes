%% Cycle Test
f="D:\Benisha\LTVS\3.6kWh\Drive_Test\Phase_1\20230616 Battery driving analysis 3.6kWH GPSC Battery Pack.xlsx";
te='Field';
q='Test-1';
c=te+" "+q+"_"+"20230616 Battery driving analysis 3.6kWH GPSC Battery Pack_log";

%%
% f="D:\Benisha\Andaman\In-house_testing_data\Bank1\09_march_Dis Chag_ banks B1_parallel test\09_march_Dis Chag_ banks B1_parallel test_modified.xlsx";

f1="D:\Benisha\LTVS\3.6kWh\Final_Plots\"+c+"_details.png";
f2="D:\Benisha\LTVS\3.6kWh\Final_Plots\"+c+"_cv.png";
f3="D:\Benisha\LTVS\3.6kWh\Final_Plots\"+c+"_ca.png";
f4="D:\Benisha\LTVS\3.6kWh\Final_Plots\"+c+"_aft.png";

m1="D:\Benisha\LTVS\3.6kWh\Final_Plots\"+c+"_details.fig";
m2="D:\Benisha\LTVS\3.6kWh\Final_Plots\"+c+"_cv.fig";
m3="D:\Benisha\LTVS\3.6kWh\Final_Plots\"+c+"_ca.fig";
m4="D:\Benisha\LTVS\3.6kWh\Final_Plots\"+c+"_aft.fig";

%%
data=readtable(f,'Sheet','CV');
data_c=readtable(f,'Sheet','PC');
data_t=readtable(f,'Sheet','Cell temp');
data_a=readtable(f,'Sheet','Ambient Temp(In Pack)');

%%

% dt=data.ElapsedTime; %DT
dt=data.TimeInSecs;
% dt=(1:1:height(data));
delv=data.delV;
% delv=data.DelmV;
meanv=(data.Mean_V)*0.001;

packv=data_c.Pack_Voltage;
current=data_c.Pack_Current;
cap=data_c.Capacity_calculated;
engy=data_c.Energy_calculated;
% cap=str2double(data_c.Pack_Ah_BMS);
% cap=data_c.Pack_Ah_BMS;
% engy=str2double(data_c.Pack_Energy_BMS)*0.001;
% dt_c=data_c.ElapsedTime;

% packv=data_c.Voltage_V_;
% current=data_c.Current_A_;
% cap=data_c.Capacity_Ah_;
% engy=data_c.Energy_Wh_;
% dt_c=data_c.ElapsedTime; % DT
dt_c=data_c.TimeInSecs;
% dt_c=(1:1:height(data_c));

delt=data_t.delT;
% dt_t=data_t.ElapsedTime; %DT
dt_t=data_t.TimeInSecs;
% dt_t=(1:1:height(data_t));
mean_t=data_t.Mean_T;

dt_a=data_a.TimeInSecs;
amb_T=data_a.AMB;
chg_fet_T=data_a.CF;
dchg_fet_T=data_a.DF;
%% Common
figure;
subplot(3,1,1);

yyaxis left;
plot(dt_c, current, 'ro-', 'MarkerSize', 3, 'LineWidth', 1, 'DisplayName','Pack Current');
title('Pack Current and Voltage Data');
% xlabel('Time'); %DT
ylabel('Current (A)','Color','r');
ax=gca;
ax.YColor='r';
% xlim([0, endTimeLimit]);
ylim([-40,5]);
grid on;

% Plot Date vs Current on secondary axis
yyaxis right;
plot(dt_c, packv,'bo-', 'MarkerSize', 3, 'LineWidth', 1, 'DisplayName','Pack Voltage');
% xlabel('Time'); %DT
ylabel('Voltage (V)','Color','b');
ax=gca;
ax.YColor='b';

% ylim([-70,50]);
% ylim([-220,170]);       %Current limit to be changed based on the max and min limit

% Add legend
legend('Location', 'northwest');


subplot(3,1,2);
for j=2:17 % Test-1
% for j=19:34 %Test-2
    plot(dt_t, data_t.(j), 'LineWidth', 1, 'DisplayName',data_t.Properties.VariableNames{j});
    hold on;
end
% plot(elapsedTime, T1, 'y-', 'LineWidth', 1, 'DisplayName','Cell tester thermocouple _ Cell Centre')
title('Cell Temperature');
% xlabel('Time'); %DT
ylabel('Temperature (deg C)');
% xlim([0, endTimeLimit]);
ylim([10,40]);
grid on;
hold off;

% Add legend
legend('Location', 'east','NumColumns',4,'FontSize',7);


subplot(3,1,3);
plot(dt_t,delt, 'LineWidth', 1, 'DisplayName','del T');
title('delT');
% xlabel('Time'); %DT
ylabel('Temperature (deg C)');
ylim([0,6]);
legend('Location', 'northwest');
grid on;

t1=sgtitle(string(te)+' '+string(q));
t1.FontWeight='bold';

linkaxes([subplot(3, 1, 1) subplot(3, 1, 2) subplot(3,1,3)], 'x');

% l1=gcf;
% exportgraphics(l1,f1,'Resolution',600);
% savefig(m1);

%% Cell Voltage Separate plot
figure;
subplot(3,1,1);

for i=2:17 
    plot(dt,(data.(i))*0.001, 'LineWidth', 1, 'DisplayName',data.Properties.VariableNames{i});
    hold on;
end

title('Cell Voltage');
% xlabel('Time'); %DT
ylabel('Voltage (V)');
% xlim([0, endTimeLimit]);
% ylim([23,60])
grid on;
hold off;

% Add legend
legend('Location', 'east','NumColumns',4,'FontSize',7);

subplot(3,1,2);
plot(dt,meanv,'LineWidth',1,'DisplayName','Average V');
title('Average Cell Voltage');
% xlabel('Time'); %DT
ylabel('Voltage (V)');
% ylim([2.5,7])
grid on;
legend('Location', 'northwest');

subplot(3,1,3);
plot(dt,delv, 'LineWidth', 1, 'DisplayName','del V');
title('delV');
% xlabel('Time'); %DT
ylabel('Voltage (mV)');
% ylim([0,350]);
grid on;
legend('Location', 'northwest');

t2=sgtitle(string(te)+' '+string(q)+' (Cell Voltage data)');
t2.FontWeight='bold';

linkaxes([subplot(3, 1, 1) subplot(3, 1, 2) subplot(3,1,3)], 'x');

% l2=gcf;
% exportgraphics(l2,f2,'Resolution',600);
% savefig(m2);

%% Capacity Separate plot
figure;
subplot(2,1,1);

plot(dt_c,cap,'LineWidth',1,'DisplayName','Capacity');
% title ('Pack Capacity');
title ('Pack Capacity (calculated)');
% xlabel('Time'); %DT
ylabel('Capacity (Ah)');
% ylim([0,4]);
grid on;
legend('Location', 'northwest');

subplot(2,1,2);
plot(dt_c,engy,'r-','LineWidth',1,'DisplayName','Energy');
% title('Pack Energy');
title('Pack Energy (calculated)');
% xlabel('Time'); %DT
ylabel('Energy (kWh)');
grid on;
legend('Location', 'northwest');

t3=sgtitle(string(te)+' '+string(q)+' (Capacity data)');
t3.FontWeight='bold';
linkaxes([subplot(2, 1, 1) subplot(2, 1, 2)], 'x');

% l3=gcf;
% exportgraphics(l3,f3,'Resolution',600);
% savefig(m3);

%% Amb and FET temp Separate plot
figure;
subplot(2,1,1);

plot(dt_a,amb_T,'r-','LineWidth',1,'DisplayName','Ambient T');
title('Ambient Temperature');
xlabel('Time'); %DT
ylabel('Temperature (deg C)');
grid on;
legend('Location', 'northwest');


subplot(2,1,2);
plot(dt_a,chg_fet_T, 'LineWidth', 1, 'DisplayName','Charge MOSFET');
hold on
plot(dt_a,dchg_fet_T, 'LineWidth', 1, 'DisplayName','Discharge MOSFET');
hold off
title('MOSFET Temperature');
xlabel('Time'); %DT
ylabel('Temperature (deg C)');
grid on;
legend('Location', 'northwest');
t1=sgtitle(string(te)+' '+string(q)+' (Ambient and FET Temperature data)');
t1.FontWeight='bold';

% l4=gcf;
% exportgraphics(l4,f4,'Resolution',600);
% savefig(m4);