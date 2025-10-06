%% Cycle Test
f="D:\Benisha\LTVS\3.6kWh\Cycle_Test\BMS_log\3_2P16S lucas tvs _CYC_7_6_23 (1).log\Cycle_Test_05.06_06.06_07.06_Complete_log_modified.xlsx";
te='Cycle';
q='Test';
c=te+" "+q+"_"+"Cycle_Test_05.06_06.06_07.06_Complete_log";

% f="D:\Benisha\LTVS\3.6kWh\Cycle_Test\BMS_log\2P16S lucas tvs _CYC_6_6_23 (1).log\2P16S lucas tvs _CYC_6_6_23 (1).log_modified.xlsx";
% te='Cycle';
% q='Test-2';
% c=te+" "+q+"_"+"2P16S lucas tvs _CYC_6_6_23 (1)";

% f="D:\Benisha\LTVS\3.6kWh\Cycle_Test\BMS_log\2P16S lucas tvs _CYC_7_6_23 (1).log\2P16S lucas tvs _CYC_7_6_23 (1).log_modified.xlsx";
% te='Cycle';
% q='Test-3';
% c=te+" "+q+"_"+"2P16S lucas tvs _CYC_7_6_23 (1)";

% f="D:\Benisha\LTVS\3.6kWh\Capacity_Test\With_BMS\28_04_2023\Test_1\Discharge_1C & Charge_24A\Discharge_1C & Charge_24A_modified.xlsx";
% te='Capacity';
% q='Test-1';
% c=te+" "+q+"_"+"Discharge_1C & Charge_24A";

% f="D:\Benisha\LTVS\3.6kWh\Capacity_Test\With_BMS\30_05_2023\BMS_data_mogambo_31st_may\BMS_data_mogambo_31st_may_modified.xlsx";
% te='Capacity';
% q='Test-2';
% c=te+" "+q+"_"+"BMS_data_mogambo_31st_may";
%%
% f="D:\Benisha\Andaman\In-house_testing_data\Bank1\09_march_Dis Chag_ banks B1_parallel test\09_march_Dis Chag_ banks B1_parallel test_modified.xlsx";

f1="D:\Benisha\LTVS\3.6kWh\Final_Plots\"+c+"_details.png";
f2="D:\Benisha\LTVS\3.6kWh\Final_Plots\"+c+"_cv.png";
f3="D:\Benisha\LTVS\3.6kWh\Final_Plots\"+c+"_ct.png";

m1="D:\Benisha\LTVS\3.6kWh\Final_Plots\"+c+"_details.fig";
m2="D:\Benisha\LTVS\3.6kWh\Final_Plots\"+c+"_cv.fig";
m3="D:\Benisha\LTVS\3.6kWh\Final_Plots\"+c+"_ct.fig";

%%
data=readtable(f,'Sheet','Cell Voltage');
data_c=readtable(f,'Sheet','Pack Details');
data_t=readtable(f,'Sheet','Cell Temperature');
% data=readtable(f,'Sheet',sheet);
%% DT
data.Date=datetime(data.DateTime);
data.Start_Time=data.DateTime;
x=data.DateTime(1);
data.Start_Time(:)=x;
data.ElapsedTime=zeros(height(data),1);
data.ElapsedTime=duration(data.DateTime(:)-data.Start_Time(:));

%%
data_c.Date=datetime(data_c.DateTime);
data_c.Start_Time=data_c.DateTime;
x=data_c.DateTime(1);
data_c.Start_Time(:)=x;
data_c.ElapsedTime=zeros(height(data_c),1);
data_c.ElapsedTime=duration(data_c.DateTime(:)-data_c.Start_Time(:));

%%
data_t.Date=datetime(data_t.DateTime);
data_t.Start_Time=data_t.DateTime;
x=data_t.DateTime(1);
data_t.Start_Time(:)=x;
data_t.ElapsedTime=zeros(height(data_t),1);
data_t.ElapsedTime=duration(data_t.DateTime(:)-data_t.Start_Time(:));
%%

% dt=data.ElapsedTime; %DT
% dt=data.TimeInSecs;
dt=(1:1:height(data));
delv=data.delV;
% delv=data.DelmV;
meanv=(data.Mean_V)*0.001;

packv=data_c.Pack_Voltage;
current=data_c.Pack_Current;
% cap=data_c.Capacity_calculated;
% engy=data_c.Energy_calculated;
cap=str2double(data_c.Pack_Ah_BMS);
% cap=data_c.Pack_Ah_BMS;
engy=str2double(data_c.Pack_Energy_BMS)*0.001;
% dt_c=data_c.ElapsedTime;

% packv=data_c.Voltage_V_;
% current=data_c.Current_A_;
% cap=data_c.Capacity_Ah_;
% engy=data_c.Energy_Wh_;
% dt_c=data_c.ElapsedTime; % DT
% dt_c=data.TimeInSecs;
dt_c=(1:1:height(data_c));

delt=data_t.delT;
% dt_t=data_t.ElapsedTime; %DT
% dt_t=data.TimeInSecs;
dt_t=(1:1:height(data_t));
mean_t=data_t.Mean_T;
%% Common
figure;
tiledlayout(3,2,'TileSpacing','compact');
nexttile([1 2]); %making 3 sections of the figure, putting graph in the 1 section
yyaxis left;
plot(dt_c, packv,'bo-', 'MarkerSize', 3, 'LineWidth', 1, 'DisplayName','Pack Voltage');
% xlabel('Time'); %DT
ylabel('Voltage (V)');

% xlim([0, endTimeLimit]);
% ylim([2.38,3.85]);
grid on;

% Plot Date vs Current on secondary axis
yyaxis right;
plot(dt_c, current, 'ro-', 'MarkerSize', 3, 'LineWidth', 1, 'DisplayName','Pack Current');
title('Pack Current and Voltage Data');
% xlabel('Time'); %DT
ylabel('Current (A)');
% ylim([-70,50]);
% ylim([-220,170]);       %Current limit to be changed based on the max and min limit


% Add legend
legend('Location', 'northwest');

nexttile;
plot(dt_c,cap,'LineWidth',1,'DisplayName','Capacity');
% title ('Pack Capacity');
title ('Pack Capacity(BMS)');
% xlabel('Time'); %DT
ylabel('Capacity (Ah)');
% ylim([0,4]);
grid on;
legend('Location', 'northwest');

nexttile;
plot(dt_c,engy,'r-','LineWidth',1,'DisplayName','Energy');
% title('Pack Energy');
title('Pack Energy(BMS)');
% xlabel('Time'); %DT
ylabel('Energy (kWh)');
grid on;
legend('Location', 'northwest');

nexttile;
plot(dt,meanv,'LineWidth',1,'DisplayName','Average V');
title('Average Cell Voltage');
% xlabel('Time'); %DT
ylabel('Voltage (V)');
% ylim([2.5,7])
grid on;
legend('Location', 'northwest');

nexttile;
plot(dt_t,mean_t,'r-','LineWidth',1,'DisplayName','Average T');
title('Average Cell Temperature');
% xlabel('Time'); %DT
ylabel('Temperature (deg C)');
grid on;
legend('Location', 'northwest');

t1=sgtitle(string(te)+' '+string(q));
t1.FontWeight='bold';
% l1=gcf;
% exportgraphics(l1,f1,'Resolution',600);
% savefig(m1);

%% Cell Voltage Separate plot
figure;
subplot(2,1,1);
% plot(dt, (data.MV_1)*0.0001, 'LineWidth', 1, 'DisplayName','MV_1');
% hold on;
for i=1:16 % Test-1
% for i=2:17 % Test-2
    plot(dt,(data.(i))*0.001, 'LineWidth', 1, 'DisplayName',data.Properties.VariableNames{i});
    hold on;
end
% plot(elapsedTime, T1, 'y-', 'LineWidth', 1, 'DisplayName','Cell tester thermocouple _ Cell Centre')
title('Cell Voltage');
% xlabel('Time'); %DT
ylabel('Voltage (V)');
% xlim([0, endTimeLimit]);
% ylim([23,60])
grid on;
hold off;

% Add legend
legend('Location', 'east','NumColumns',4,'FontSize',7);

subplot(2,1,2);
plot(dt,delv, 'LineWidth', 1, 'DisplayName','del V');
title('delV');
% xlabel('Time'); %DT
ylabel('Voltage (mV)');
grid on;
legend('Location', 'northwest');
t2=sgtitle(string(te)+' '+string(q)+' (Cell Voltage data)');
t2.FontWeight='bold';

linkaxes([subplot(2, 1, 1) subplot(2, 1, 2)], 'x');

% l2=gcf;
% exportgraphics(l2,f2,'Resolution',600);
% savefig(m2);
%% Cell Temperature Separate plot
figure;
subplot(2,1,1);

for j=1:16 % Test-1
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

subplot(2,1,2);
plot(dt_t,delt, 'LineWidth', 1, 'DisplayName','del T');
title('delT');
% xlabel('Time'); %DT
ylabel('Temperature (deg C)');
ylim([0,6]);
legend('Location', 'northwest');
grid on;

t3=sgtitle(string(te)+' '+string(q)+' (Cell Temperature data)');
t3.FontWeight='bold';
linkaxes([subplot(2, 1, 1) subplot(2, 1, 2)], 'x');

% l3=gcf;
% exportgraphics(l3,f3,'Resolution',600);
% savefig(m3);