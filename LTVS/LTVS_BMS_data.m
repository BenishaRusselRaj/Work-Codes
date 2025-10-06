%% BMS Data

f="D:\Benisha\LTVS\Final_Report\Drive Test data\Prev\Test_1\Drive data analysis_10Kwh.xlsx";
c="Actual_Drive_Test_Log_1";
q='Test-1';

% f="D:\Benisha\LTVS\Final_Report\Drive Test data\Prev\Test_2\10kwh Drive Testing 2 2.xlsx";
% c="Actual_Drive_Test_Log_2";
% q='Test-2';

% sheet='Testing-10kwh';
sheet='Analysis data';

te='Field';
%%
% f="D:\Benisha\LTVS\Final_Report\Capacity Test data\pack testing with BMS for calibration-- Tester and BMS_09_12_2023_modified.xlsx";

f1="D:\Benisha\LTVS\Final_Report\Final_Plots\"+c+"_details.png";
f2="D:\Benisha\LTVS\Final_Report\Final_Plots\"+c+"_cv.png";
f3="D:\Benisha\LTVS\Final_Report\Final_Plots\"+c+"_ct.png";

m1="D:\Benisha\LTVS\Final_Report\Final_Plots\"+c+"_details.fig";
m2="D:\Benisha\LTVS\Final_Report\Final_Plots\"+c+"_cv.fig";
m3="D:\Benisha\LTVS\Final_Report\Final_Plots\"+c+"_ct.fig";


%% 
% data=readtable(f,'Sheet','Cell Voltage');
% data_c=readtable(f,'Sheet','Pack Details');
% data_t=readtable(f,'Sheet','Cell Temperature');
data=readtable(f,'Sheet',sheet);
% %%
% data.Date=datetime(data.DateTime);
% data.Start_Time=data.DateTime;
% x=data.DateTime(1);
% data.Start_Time(:)=x;
% data.ElapsedTime=zeros(height(data),1);
% data.ElapsedTime=duration(data.DateTime(:)-data.Start_Time(:));
% 
% %%
% data_c.Date=datetime(data_c.Date);
% data_c.Start_Time=data_c.Date;
% x=data_c.Date(1);
% data_c.Start_Time(:)=x;
% data_c.ElapsedTime=zeros(height(data_c),1);
% data_c.ElapsedTime=duration(data_c.Date(:)-data_c.Start_Time(:));
% 
% %%
% data_t.Date=datetime(data_t.DateTime);
% data_t.Start_Time=data_t.DateTime;
% x=data_t.DateTime(1);
% data_t.Start_Time(:)=x;
% data_t.ElapsedTime=zeros(height(data_t),1);
% data_t.ElapsedTime=duration(data_t.DateTime(:)-data_t.Start_Time(:));
%%

% dt=data.ElapsedTime;
dt=data.TimeInSecs;
% delv=data.delV;
delv=data.DelmV;
meanv=data.Mean_V;

packv=(data.PV)*0.001;
current=data.PC;
% cap=data_c.Capacity_calculated;
% engy=data_c.Energy_calculated;
cap=data.Pack_Ah;
engy=data.Pack_Energy;
% dt_c=data_c.ElapsedTime;

% packv=data_c.Voltage_V_;
% current=data_c.Current_A_;
% cap=data_c.Capacity_Ah_;
% engy=data_c.Energy_Wh_;
% dt_c=data_c.ElapsedTime;
dt_c=data.TimeInSecs;

delt=data.delT;
% dt_t=data_t.ElapsedTime;
dt_t=data.TimeInSecs;
mean_t=data.Mean_T;
%% Common
figure;
tiledlayout(3,2,'TileSpacing','compact');
nexttile([1 2]); %making 3 sections of the figure, putting graph in the 1 section
yyaxis left;
plot(dt_c, packv,'bo-', 'MarkerSize', 3, 'LineWidth', 1, 'DisplayName','Pack Voltage');
% xlabel('Time');
ylabel('Voltage (V)');

% xlim([0, endTimeLimit]);
% ylim([2.38,3.85]);
grid on;

% Plot Date vs Current on secondary axis
yyaxis right;
plot(dt_c, current, 'ro-', 'MarkerSize', 3, 'LineWidth', 1, 'DisplayName','Pack Current');
title('Pack Current and Voltage Data');
% xlabel('Time');
ylabel('Current (A)');
% ylim([-70,50]);
% ylim([-220,170]);       %Current limit to be changed based on the max and min limit


% Add legend
legend('Location', 'northwest');

nexttile;
plot(dt_c,cap,'LineWidth',1,'DisplayName','Capacity');
% title ('Pack Capacity');
title ('Pack Capacity(BMS)');
% xlabel('Time');
ylabel('Capacity (Ah)');
% ylim([0,4]);
grid on;
legend('Location', 'northwest');

nexttile;
plot(dt_c,engy*0.001,'r-','LineWidth',1,'DisplayName','Energy');
% title('Pack Energy');
title('Pack Energy(BMS)');
% xlabel('Time');
ylabel('Energy (kWh)');
grid on;
legend('Location', 'northwest');

nexttile;
plot(dt,meanv*0.001,'LineWidth',1,'DisplayName','Average V');
title('Average Cell Voltage');
% xlabel('Time');
ylabel('Voltage (V)');
% ylim([2.5,7])
grid on;
legend('Location', 'northwest');

nexttile;
plot(dt_t,mean_t,'r-','LineWidth',1,'DisplayName','Average T');
title('Average Cell Temperature');
% xlabel('Time');
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
for i=3:18 % Test-1
% for i=2:17 % Test-2
    plot(dt,(data.(i))*0.001, 'LineWidth', 1, 'DisplayName',data.Properties.VariableNames{i});
    hold on;
end
% plot(elapsedTime, T1, 'y-', 'LineWidth', 1, 'DisplayName','Cell tester thermocouple _ Cell Centre')
title('Cell Voltage');
% xlabel('Time');
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
% xlabel('Time');
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

for j=25:32 % Test-1
% for j=19:34 %Test-2
    plot(dt_t, data.(j), 'LineWidth', 1, 'DisplayName',data.Properties.VariableNames{j});
    hold on;
end
% plot(elapsedTime, T1, 'y-', 'LineWidth', 1, 'DisplayName','Cell tester thermocouple _ Cell Centre')
title('Cell Temperature');
% xlabel('Time');
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
% xlabel('Time');
ylabel('Temperature (deg C)');
ylim([0,4]);
legend('Location', 'northwest');
grid on;

t3=sgtitle(string(te)+' '+string(q)+' (Cell Temperature data)');
t3.FontWeight='bold';
linkaxes([subplot(2, 1, 1) subplot(2, 1, 2)], 'x');

% l3=gcf;
% exportgraphics(l3,f3,'Resolution',600);
% savefig(m3);