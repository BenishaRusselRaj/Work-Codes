%% In-house data

% f="D:\Benisha\Andaman\In-house_testing_data\Bank1\09_march_Dis Chag_ banks B1_parallel test\09_march_Dis Chag_ banks B1_parallel test_modified.xlsx";
% c="In_house_09_march_Dis Chag_ banks B1_parallel test";
f="D:\Benisha\Andaman\In-house_testing_data\Bank1\19_April_Bank1_series with deltal Discharge\19_April_Bank1_series with deltal Discharge_modified.xlsx";
c="In_house_19_April_Bank1_series with deltal Discharge";
% 

% f="D:\Benisha\Andaman\In-house_testing_data\Bank2\09_march_Dis Chag_ banks B2_parallel test\09_march_Dis Chag_ banks B2_parallel test_modified.xlsx";
% c="In_house_09_march_Dis Chag_ banks B2_parallel test";
% f="D:\Benisha\Andaman\In-house_testing_data\Bank2\19_April_Bank2_series with deltal Discharge\19_April_Bank2_series with deltal Discharge_modified.xlsx";
% c="In_house_19_April_Bank2_series with deltal Discharge";

%% Field data

% f="D:\Benisha\Andaman\Andaman Battery Data_February\B1_014_02_24_log\B1_014_02_24_log_modified.xlsx";
% c="Field_B1_014_02_24_log";
% f="D:\Benisha\Andaman\Andaman Battery Data_February\B2_014_02_24_log\B2_014_02_24_log_modified.xlsx";
% c="Field_B2_014_02_24_log";
%%
% f="D:\Benisha\Andaman\In-house_testing_data\Bank1\09_march_Dis Chag_ banks B1_parallel test\09_march_Dis Chag_ banks B1_parallel test_modified.xlsx";

f1="D:\Benisha\Andaman\Final_Plots\"+c+"_details.png";
f2="D:\Benisha\Andaman\Final_Plots\"+c+"_cv.png";
f3="D:\Benisha\Andaman\Final_Plots\"+c+"_ct.png";

m1="D:\Benisha\Andaman\Final_Plots\"+c+"_details.fig";
m2="D:\Benisha\Andaman\Final_Plots\"+c+"_cv.fig";
m3="D:\Benisha\Andaman\Final_Plots\"+c+"_ct.fig";

b='Bank 1';
q='Test-2';
te='In-house';


%% In-house data
data=readtable(f,'Sheet','Cell Voltage');
data_t=readtable(f,'Sheet','Cell Temperature');
packv=data.PackVoltage;


dt=duration(data.ElapsedTime,'Format','hh:mm:ss');

dt_c=duration(data.ElapsedTime,'Format','hh:mm:ss');
current=data.PackCurrent;
cap=data.Capacity_calculated;
engy=data.Energy_calculated;
delv=data.delV;
meanv=data.Mean_V;

delt=data_t.delT;
dt_t=duration(data_t.ElapsedTime,'Format','hh:mm:ss');
mean_t=data_t.Mean_T;

%% For Field data

% data=readtable(f,'Sheet','Cell Voltage');
% data_t=readtable(f,'Sheet','Cell Temperature');
% data_c=readtable(f,'Sheet','Pack Details');
% 
% packv=data_c.PackVoltage;
% dt=duration(data.ElapsedTime,'Format','hh:mm:ss');
% current=data_c.PackCurrent;
% cap=data_c.Capacity_calculated;
% engy=data_c.Energy_calculated;
% dt_c=duration(data_c.ElapsedTime,'Format','hh:mm:ss');
% delv=data.delV;
% meanv=data.Mean_V;
% 
% 
% delt=data_t.delT;
% dt_t=duration(data_t.ElapsedTime,'Format','hh:mm:ss');
% mean_t=data_t.Mean_T;
%% Common
figure;
tiledlayout(3,2,'TileSpacing','compact');
nexttile([1 2]); %making 3 sections of the figure, putting graph in the 1 section
yyaxis left;
plot(dt_c, packv,'bo-', 'MarkerSize', 3, 'LineWidth', 1, 'DisplayName','Pack Voltage');
xlabel('Time');
ylabel('Voltage (V)');

% xlim([0, endTimeLimit]);
% ylim([2.38,3.85]);
grid on;

% Plot Date vs Current on secondary axis
yyaxis right;
plot(dt_c, current, 'ro-', 'MarkerSize', 3, 'LineWidth', 1, 'DisplayName','Pack Current');
title('Pack Current and Voltage Data');
xlabel('Time');
ylabel('Current (A)');
% ylim([-70,50]);
% ylim([-220,170]);       %Current limit to be changed based on the max and min limit


% Add legend
legend('Location', 'northwest');

nexttile;
plot(dt_c,cap,'LineWidth',1,'DisplayName','Capacity');
title ('Time Vs. Capacity');
xlabel('Time');
ylabel('Capacity (Ah)');
grid on;
legend('Location', 'northwest');

nexttile;
plot(dt_c,engy*0.001,'r-','LineWidth',1,'DisplayName','Energy');
title('Time Vs. Energy');
xlabel('Time');
ylabel('Energy (kWh)');
grid on;
legend('Location', 'northwest');

nexttile;
plot(dt,meanv*0.0001,'LineWidth',1,'DisplayName','Average V');
title('Time Vs. Average Cell Voltage');
xlabel('Time');
ylabel('Voltage (V)');
% ylim([2.5,7])
grid on;
legend('Location', 'northwest');

nexttile;
plot(dt_t,mean_t,'r-','LineWidth',1,'DisplayName','Average T');
title('Time Vs. Average Cell Temperature');
xlabel('Time');
ylabel('Temperature (deg C)');
grid on;
legend('Location', 'northwest');

t1=sgtitle(string(te)+' '+string(q)+' ('+string(b)+')');
t1.FontWeight='bold';
% l1=gcf;
% exportgraphics(l1,f1,'Resolution',600);
% savefig(m1);

%% Cell Voltage Separate plot
figure;
subplot(2,1,1);
% plot(dt, (data.MV_1)*0.0001, 'LineWidth', 1, 'DisplayName','MV_1');
% hold on;
for i=4:105
    plot(dt,(data.(i))*0.0001, 'LineWidth', 1, 'DisplayName',data.Properties.VariableNames{i});
    hold on;
end
% plot(elapsedTime, T1, 'y-', 'LineWidth', 1, 'DisplayName','Cell tester thermocouple _ Cell Centre')
title('Time vs Cell Voltage');
xlabel('Time');
ylabel('Voltage (V)');
% xlim([0, endTimeLimit]);
% ylim([23,60])
grid on;
hold off;

% Add legend
legend('Location', 'eastoutside','NumColumns',6,'FontSize',5);

subplot(2,1,2);
plot(dt,delv*0.1, 'LineWidth', 1, 'DisplayName','del V');
title('Time Vs. delV');
xlabel('Time');
ylabel('Voltage (mV)');
grid on;
legend('Location', 'northwest');
t2=sgtitle(string(te)+' '+string(q)+' (Cell Voltage data) ('+string(b)+')');
t2.FontWeight='bold';

linkaxes([subplot(2, 1, 1) subplot(2, 1, 2)], 'x');

% l2=gcf;
% exportgraphics(l2,f2,'Resolution',600);
% savefig(m2);
%% Cell Temperature Separate plot
figure;
subplot(2,1,1);

for j=4:71
    plot(dt_t, data_t.(j), 'LineWidth', 1, 'DisplayName',data_t.Properties.VariableNames{j});
    hold on;
end
% plot(elapsedTime, T1, 'y-', 'LineWidth', 1, 'DisplayName','Cell tester thermocouple _ Cell Centre')
title('Time vs Cell Temperature');
xlabel('Time');
ylabel('Temperature (deg C)');
% xlim([0, endTimeLimit]);
ylim([10,40]);
grid on;
hold off;

% Add legend
legend('Location', 'eastoutside','NumColumns',6,'FontSize',5);

subplot(2,1,2);
plot(dt_t,delt, 'LineWidth', 1, 'DisplayName','del T');
title('Time Vs. delT');
xlabel('Time');
ylabel('Temperature (deg C)');
% ylim([5,10]);
legend('Location', 'northwest');
grid on;

t3=sgtitle(string(te)+' '+string(q)+' (Cell Temperature data) ('+string(b)+')');
t3.FontWeight='bold';
linkaxes([subplot(2, 1, 1) subplot(2, 1, 2)], 'x');

% l3=gcf;
% exportgraphics(l3,f3,'Resolution',600);
% savefig(m3);