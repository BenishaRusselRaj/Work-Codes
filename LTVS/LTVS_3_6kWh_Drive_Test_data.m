%% Cycle Test

% f="D:\Benisha\LTVS\3.6kWh\Drive_Test\Phase_2\18-10-2023\18-10-2023_observations.xlsx";
% te='Field';
% q='Test-2';
% c=te+" "+q+"_"+"18-10-2023_log";

% f="D:\Benisha\LTVS\3.6kWh\Drive_Test\Phase_2\19-10-2023\19-10-2023_observations.xlsx";
% te='Field';
% q='Test-3';
% c=te+" "+q+"_"+"19-10-2023_log";

f="D:\Benisha\LTVS\3.6kWh\Drive_Test\Phase_2\30-10-2023\30-10-2023_observations.xlsx";
te='Field';
q='Test-4';
c=te+" "+q+"_"+"30-10-2023_log";
%%
% f="D:\Benisha\Andaman\In-house_testing_data\Bank1\09_march_Dis Chag_ banks B1_parallel test\09_march_Dis Chag_ banks B1_parallel test_modified.xlsx";

f1="D:\Benisha\LTVS\3.6kWh\Final_Plots\"+c+"_details.png";
f2="D:\Benisha\LTVS\3.6kWh\Final_Plots\"+c+"_cv.png";
f3="D:\Benisha\LTVS\3.6kWh\Final_Plots\"+c+"_ca.png";

m1="D:\Benisha\LTVS\3.6kWh\Final_Plots\"+c+"_details.fig";
m2="D:\Benisha\LTVS\3.6kWh\Final_Plots\"+c+"_cv.fig";
m3="D:\Benisha\LTVS\3.6kWh\Final_Plots\"+c+"_ca.fig";

%%
data=readtable(f);
%%
data.Date=datetime(data.DateTime); % Comment for 18/10/2023 data
data.Start_Time=data.DateTime;
x=data.DateTime(1);
data.Start_Time(:)=x;
data.ElapsedTime=zeros(height(data),1);
data.ElapsedTime=duration(data.DateTime(:)-data.Start_Time(:));
dt=data.ElapsedTime;

% dt=duration(0,0,data.ElapsedTime);
% dt=(1:1:height(data));
 
delv=data.delV;
meanv=(data.Mean_V)*0.001;

packv=data.Pack_Voltage;
current=data.Pack_Current;
cap=data.Capacity_calculated;
engy=(data.Energy_calculated)*0.001;


%% Common
figure;
subplot(3,1,1);

yyaxis left;
plot(dt, current, 'ro-', 'MarkerSize', 3, 'LineWidth', 1, 'DisplayName','Pack Current');
title('Pack Current and Voltage Data');
xlabel('Time'); %DT
ylabel('Current (A)','Color','r');
ax=gca;
ax.YColor='r';
% xlim([0, endTimeLimit]);
ylim([-40,5]);
grid on;

% Plot Date vs Current on secondary axis
yyaxis right;
plot(dt, packv,'bo-', 'MarkerSize', 3, 'LineWidth', 1, 'DisplayName','Pack Voltage');
xlabel('Time'); %DT
ylabel('Voltage (V)','Color','b');
ax=gca;
ax.YColor='b';

% ylim([-70,50]);
% ylim([-220,170]);       %Current limit to be changed based on the max and min limit

% Add legend
legend('Location', 'northwest');


subplot(3,1,2);
plot(dt,amb_T,'r-','LineWidth',1,'DisplayName','Ambient T');
title('Ambient Temperature');
xlabel('Time'); %DT
ylabel('Temperature (deg C)');
grid on;
legend('Location', 'northwest');


subplot(3,1,3);
plot(dt,chg_fet_T, 'LineWidth', 1, 'DisplayName','Charge MOSFET');
hold on
plot(dt,dchg_fet_T, 'LineWidth', 1, 'DisplayName','Discharge MOSFET');
hold off
title('MOSFET Temperature');
xlabel('Time'); %DT
ylabel('Temperature (deg C)');
grid on;
legend('Location', 'northwest');
t1=sgtitle(string(te)+' '+string(q));
t1.FontWeight='bold';

linkaxes([subplot(3, 1, 1) subplot(3, 1, 2) subplot(3,1,3)], 'x');

% l1=gcf;
% exportgraphics(l1,f1,'Resolution',600);
% savefig(m1);

%% Cell Voltage Separate plot
figure;
subplot(3,1,1);

for i=5:20 
    plot(dt,(data.(i))*0.001, 'LineWidth', 1, 'DisplayName',data.Properties.VariableNames{i});
    hold on;
end

title('Cell Voltage');
xlabel('Time'); %DT
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
xlabel('Time'); %DT
ylabel('Voltage (V)');
% ylim([2.5,7])
grid on;
legend('Location', 'northwest');

subplot(3,1,3);
plot(dt,delv, 'LineWidth', 1, 'DisplayName','del V');
title('delV');
xlabel('Time'); %DT
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

plot(dt,cap,'LineWidth',1,'DisplayName','Capacity');
% title ('Pack Capacity');
title ('Pack Capacity (calculated)');
xlabel('Time'); %DT
ylabel('Capacity (Ah)');
% ylim([0,4]);
grid on;
legend('Location', 'northwest');

subplot(2,1,2);
plot(dt,engy,'r-','LineWidth',1,'DisplayName','Energy');
% title('Pack Energy');
title('Pack Energy (calculated)');
xlabel('Time'); %DT
ylabel('Energy (kWh)');
grid on;
legend('Location', 'northwest');

t3=sgtitle(string(te)+' '+string(q)+' (Capacity data)');
t3.FontWeight='bold';
linkaxes([subplot(2, 1, 1) subplot(2, 1, 2)], 'x');

% l3=gcf;
% exportgraphics(l3,f3,'Resolution',600);
% savefig(m3);