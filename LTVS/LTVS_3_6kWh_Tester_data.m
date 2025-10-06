%% Tester Data
te='Capacity';
%With BMS
% f="D:\Benisha\LTVS\3.6kWh\Capacity_Test\With_BMS\28_04_2023\Discharge_1C & Charge_24A.xlsx";
% sheet_name="record";
% q='Test-1';
% c=te+" "+q+"_"+"Capacity test after welding issue- 0.25C";
% 
% f="D:\Benisha\LTVS\3.6kWh\Capacity_Test\Without_BMS\Capacity test after welding issue- 0.25C.xlsx";
% sheet_name="record";
% q='Test-2';
% c=te+" "+q+"_"+"Capacity test after welding issue- 0.25C";


% Without BMS
f="D:\Benisha\LTVS\3.6kWh\Capacity_Test\Without_BMS\Capacity test after welding issue- 0.25C.xlsx";
sheet_name="record";
q='Test-2';
c=te+" "+q+"_"+"Capacity test after welding issue- 0.25C";

%%
% f="D:\Benisha\Andaman\In-house_testing_data\Bank1\09_march_Dis Chag_ banks B1_parallel test\09_march_Dis Chag_ banks B1_parallel test_modified.xlsx";

f1="D:\Benisha\LTVS\3.6kWh\Final_Plots\"+c+"_details.png";
f2="D:\Benisha\LTVS\3.6kWh\Final_Plots\"+c+"_cv.png";
f3="D:\Benisha\LTVS\3.6kWh\Final_Plots\"+c+"_ct.png";

m1="D:\Benisha\LTVS\3.6kWh\Final_Plots\"+c+"_details.fig";
m2="D:\Benisha\LTVS\3.6kWh\Final_Plots\"+c+"_cv.fig";
m3="D:\Benisha\LTVS\3.6kWh\Final_Plots\"+c+"_ct.fig";

%% 
data=readtable(f,'Sheet',sheet_name);
% data=readtable(f);
%%
data.Date=datetime(data.Date);
data.Start_Time=data.Date;
x=data.Date(1);
data.Start_Time(:)=x;
data.ElapsedTime=zeros(height(data),1);
data.ElapsedTime=duration(data.Date(:)-data.Start_Time(:));
%%
% dt=data.ElapsedTime;
dt=duration(data.TotalTime,'Format','hh:mm:ss');
packv=data.Voltage_V_;
% dt=duration(data.ElapsedTime,'Format','hh:mm:ss');
current=data.Current_A_;
% cap=data.Capacity_calculated;
% engy=data.Energy_calculated;
cap=data.Capacity_Ah_;
engy=(data.Energy_Wh_)*0.001;


delv=data.delV;
meanv=data.Mean_V;


% delt=data.delT;
% mean_t=data.Mean_T;
%% Common
figure;
tiledlayout(3,2,'TileSpacing','compact');
nexttile([1 2]); %making 3 sections of the figure, putting graph in the 1 section
yyaxis left;
plot(dt, packv,'bo-', 'MarkerSize', 3, 'LineWidth', 1, 'DisplayName','Pack Voltage');
xlabel('Time');
ylabel('Voltage (V)');

% xlim([0, endTimeLimit]);
% ylim([2.38,3.85]);
grid on;

% Plot Date vs Current on secondary axis
yyaxis right;
plot(dt, current, 'ro-', 'MarkerSize', 3, 'LineWidth', 1, 'DisplayName','Pack Current');
title('Pack Current and Voltage Data');
xlabel('Time');
ylabel('Current (A)');
% ylim([-70,50]);
% ylim([-220,170]);       %Current limit to be changed based on the max and min limit


% Add legend
legend('Location', 'northwest');

nexttile;
plot(dt,cap,'LineWidth',1,'DisplayName','Capacity');
title ('Time Vs. Capacity');
xlabel('Time');
ylabel('Capacity (Ah)');
grid on;
legend('Location', 'northwest');

nexttile;
plot(dt,engy,'r-','LineWidth',1,'DisplayName','Energy');
title('Time Vs. Energy');
xlabel('Time');
ylabel('Energy (kWh)');
grid on;
legend('Location', 'northwest');

% nexttile;
nexttile([1 2]);
plot(dt,meanv,'LineWidth',1,'DisplayName','Average V');
title('Time Vs. Average Cell Voltage');
xlabel('Time');
ylabel('Voltage (V)');
% ylim([2.5,7])
grid on;
legend('Location', 'northwest');

% nexttile;
% plot(dt,mean_t,'r-','LineWidth',1,'DisplayName','Average T');
% title('Time Vs. Average Cell Temperature');
% xlabel('Time');
% ylabel('Temperature (deg C)');
% grid on;
% legend('Location', 'northwest');

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
for i=25:40 % Cap test 1
    plot(dt,(data.(i)), 'LineWidth', 1, 'DisplayName',data.Properties.VariableNames{i});
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
legend('Location', 'east','NumColumns',4,'FontSize',7);

subplot(2,1,2);
plot(dt,delv, 'LineWidth', 1, 'DisplayName','del V');
title('Time Vs. delV');
xlabel('Time');
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
% figure;
% subplot(2,1,1);
% 
% for j=28:43 % Cap test 1
%     plot(dt, data.(j), 'LineWidth', 1, 'DisplayName',data.Properties.VariableNames{j});
%     hold on;
% end
% % plot(elapsedTime, T1, 'y-', 'LineWidth', 1, 'DisplayName','Cell tester thermocouple _ Cell Centre')
% title('Time vs Cell Temperature');
% xlabel('Time');
% ylabel('Temperature (deg C)');
% % xlim([0, endTimeLimit]);
% % ylim([10,40]);
% grid on;
% hold off;
% 
% % Add legend
% legend('Location', 'east','NumColumns',4,'FontSize',7);
% 
% subplot(2,1,2);
% plot(dt,delt, 'LineWidth', 1, 'DisplayName','del T');
% title('Time Vs. delT');
% xlabel('Time');
% ylabel('Temperature (deg C)');
% % ylim([5,10]);
% legend('Location', 'northwest');
% grid on;
% 
% t3=sgtitle(string(te)+' '+string(q)+' (Cell Temperature data)');
% t3.FontWeight='bold';
% linkaxes([subplot(2, 1, 1) subplot(2, 1, 2)], 'x');
% 
% % l3=gcf;
% % exportgraphics(l3,f3,'Resolution',600);
% % savefig(m3);