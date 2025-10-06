%% Graph plots
% Add path to file here:
f = "C:\Users\IITM\Downloads\Sample Data for code generation.xlsx";

%% Read file
data = readtable(f);

%% Figure locations

splitFileName = strsplit(f,'\\');
splitName = strsplit(splitFileName(end), '.');
name = splitName(1);

%% Separating the needed values/columns
% When saving the excel file, always save using the names given in the
% sample files.
% !!! Do not use different column names for every file!!!
packVoltage = data.Voltage;
current = data.Current;
delV = data.DelMV;
delT = data.DelT;

% cellV_pattern = 'Cell ' + digitsPattern(1, 2);
cellV_pattern = 'Cell'+ digitsPattern(1, 2);
cell_voltages = data(:, matches(data.Properties.VariableNames, cellV_pattern));
% cell_voltages = data(:, regexp(data.Properties.VariableNames, cellV_pattern, 'match'));
cellT_pattern = 'Cell' + digitsPattern(1, 2)  + 'Temp';
cell_temperatures = data(:, matches(data.Properties.VariableNames, cellT_pattern));

%% Extracting date and time as datetime (since a single test could techically take place at different dates)

data.Time = datetime(data.Time, 'ConvertFrom','excel', 'Format','HH:mm:ss');
data.DateTime = strcat(string(data.Date),{' '}, string(data.Time));
data.DateTime = datetime(data.DateTime);
time = data.DateTime;

%% Pack Voltage Vs. Time

t = 'Pack Voltage Vs. Time';
figure('units','normalized','outerposition',[0 0 1 1]);

plot(time, packVoltage, 'LineWidth', 1, 'DisplayName','Pack Voltage');
title(t,'fontweight','bold');
xlabel('Time','fontweight','bold'); %DT
ylabel('Voltage (V)','fontweight','bold');
grid on;
legend('Location', 'northeast');

f1 = strjoin(splitFileName(1:end-1), '\\') + '\\' + name + '_' + t + '.png';
l1=gcf;
exportgraphics(l1,f1,'Resolution',600);

%% Pack Voltage and Current Vs. Time

t = 'Pack Current and Voltage Data';
figure('units','normalized','outerposition',[0 0 1 1]);

yyaxis left;
plot(time, packVoltage, 'LineWidth', 1, 'DisplayName','Pack Voltage');
ylabel('Voltage (V)','fontweight','bold');
grid on;

yyaxis right;
plot(time, current,'LineWidth', 1, 'DisplayName','Pack Current');
ylabel('Current(A)','fontweight','bold');
xlabel('Time','fontweight','bold');
title (t,'fontweight','bold');
legend('Location', 'northeast');

f1 = strjoin(splitFileName(1:end-1), '\\') + '\\' + name + '_' + t + '.png';
l1=gcf;
exportgraphics(l1,f1,'Resolution',600);

%% Cell Voltages Vs. Time

t = 'Cell Voltages Vs. Time';
figure('Units','normalized', 'OuterPosition', [0 0 1 1]);

for k = 1: length(cell_voltages.Properties.VariableNames)
    plot(time, cell_voltages.(k),'LineWidth', 1, 'DisplayName', cell_voltages.Properties.VariableNames{k});
    hold on;
end

hold off;
title (t,'fontweight','bold');
ylabel('Voltage (V)','fontweight','bold');
xlabel('Time','fontweight','bold');
grid on;
legend('Location','northeast');

f1 = strjoin(splitFileName(1:end-1), '\\') + '\\' + name + '_' + t + '.png';
l1=gcf;
exportgraphics(l1,f1,'Resolution',600);

%% delV Vs. Time

t = 'DelV Vs. Time';
figure('units','normalized','outerposition',[0 0 1 1]);

plot(time, delV, 'LineWidth', 1, 'DisplayName','DelV');
title(t,'fontweight','bold');
xlabel('Time','fontweight','bold'); %DT
ylabel('Voltage (mV)','fontweight','bold');
grid on;
legend('Location', 'northeast');

f1 = strjoin(splitFileName(1:end-1), '\\') + '\\' + name + '_' + t + '.png';
l1=gcf;
exportgraphics(l1,f1,'Resolution',600);


%% Cell Temperatures Vs. Time

t = 'Cell Temperatures Vs. Time';
figure('Units','normalized', 'OuterPosition', [0 0 1 1]);

for k = 1: length(cell_temperatures.Properties.VariableNames)
    plot(time, cell_temperatures.(k),'LineWidth', 1, 'DisplayName', cell_temperatures.Properties.VariableNames{k});
    hold on;
end

hold off;
title (t,'fontweight','bold');
ylabel('Temperature (degC)','fontweight','bold');
xlabel('Time','fontweight','bold');
grid on;
legend('Location','northeast');

f1 = strjoin(splitFileName(1:end-1), '\\') + '\\' + name + '_' + t + '.png';
l1=gcf;
exportgraphics(l1,f1,'Resolution',600);


%% delT Vs. Time

t = 'DelT Vs. Time';
figure('units','normalized','outerposition',[0 0 1 1]);

plot(time, delT, 'LineWidth', 1, 'DisplayName','DelT');
title(t,'fontweight','bold');
xlabel('Time','fontweight','bold'); %DT
ylabel('Temperature (degC)','fontweight','bold');
grid on;
legend('Location', 'northeast');

f1 = strjoin(splitFileName(1:end-1), '\\') + '\\' + name + '_' + t + '.png';
l1=gcf;
exportgraphics(l1,f1,'Resolution',600);

%%
% If the code throws an error, check the original excel file if the names
% of the columns are as follows:

% Pack Voltage: 'Voltage'
% Pack Current: 'Current'
% Cell Voltages: 'Cell 1', 'Cell 2', ...
% Cell Temperature:'Cell 1 Temp'or'Cell 01 Temp','Cell2Temp'or 'Cell02Temp',...
% delV: 'DelMV'
% delT: 'DelT'
