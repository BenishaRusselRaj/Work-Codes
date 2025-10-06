"""
DESCRIPTION:
[STEP ZERO.1]
The input to this code is the text file from the cell testers (6A and 100A)
Code to arrange the txt file in a way that can be processed
Misaligned data are straightened out
The output(a txt file) gets saved automatically
The output is the file with the same name, with a "_modified_arranged.txt" added at the end

THINGS TO NOTE:
Change the variable "csv_header" according to the tester configuration
"""
import fileinput
import glob
import os
import re
path="D:\\Benisha\\SoH_NN\\Data\\PHY\\PHY_21.1\\21.1\\*.txt"
files=glob.glob(path)

for file in files:
    inputFileName1 = file
    # inputFileName1 = "D:\Benisha\SoH_NN\Data\Variable Temperature\Extracted files_PHY13\PHY13_CYC_33.1_100%_25 Deg_RPT+Imp_183Cycles.txt"
    # inputFileName1 = inputFileName1.replace("\\",'\\\\')
    inputFileName =  os.path.splitext(inputFileName1)[0] + "_remove.txt" #change input file name for data already having the headers
    # outputFileName = os.path.splitext(inputFileName1)[0] + "_modified_arranged.txt"
    
    fin_path=inputFileName1.rsplit('\\',1)[0]+'\\Modified_Files'
    if not os.path.exists(fin_path):
        os.makedirs(fin_path)
    outputFileName = fin_path+'\\'+inputFileName1.rsplit('\\',1)[1].rsplit('.',1)[0]+ "_modified_arranged.txt"
    
    count=1; result=''
    #%%
    # csv_header='Cycle_No,Step_No,Record_ID,Step_Type,Time_Elapsed,Time_Spent_in_Step,Voltage,Q_in_Step,Current,Q_in_and_out_Step,Temperature,Energy_in_out,Q_in_out,Energy_in_out,Q_in_Step(mAh/g),Super Capacitace,Energy(mWh),Start_Voltage,Energy_in_out(mWh/g),End_Voltage,Power,Start Temperature,DCIR(mO),End Temperature,RTC,Q_End,ShowAuxVolt,Chg_Mid_Vtg,ShowAuxTemp,DChg_Mid_Vtg,DCIR(mO),a1,Q_Chg,a2,Q_Dchg,a3,Energy_Chg,a4,Energy_DChg,a5,Q_Net_DChg,a6,Energy_Net_DChg,a7,OriStepID,y,Chg_IR(mO),,DChg_IR(mO),,End_Temp,,Q_Net_DChg(mAh),,Net_Engy_DChg(mWh),,' # 6Amp Tester
    # csv_header='Cycle_No,Step_No,Record_ID,Step_Type,Time_Elapsed,Time_Spent_in_Step,Voltage,Q_in_Step,Current,Q_in_and_out_Step,Temperature,Energy_in_out,Q_in_out,Energy_in_out,Q_in_Step(mAh/g),Capacitance,Energy(mWh),Start_Voltage,Energy_in_out(mWh/g),End_Voltage,RTC,Start_Temperature,Plat_Cap(mAh),End_Temperature,Plat_Cap_Density(mAh/g),Q_End(mWh),Plat_Cap_Eff(%),Chg_Mid_Vtg,Plat_Time,DChg_Mid_Vtg,Chg_Capacitance,DCIR,DChg_Capacitance,Q_Chg(mAh),Engy_Chg(mWh),Q_DChg(mAh),Engy_DChg(mWh),Engy_Chg(mWh),dQ/dV(mAh/V),Engy_DChg(mWh),dQm/dV(mAh/V.g),Q_Net_DChg(mAh),Auxiliary_ChannelTU4,Raw_Step_ID,a1,U4_Start,a2,U4_End,a3,T4_Start_Temp,a4,T1_EndTemp,a5,,,,,,,' #6Amp Tester
    # csv_header='Cycle_No,Step_No,Record_ID,Step_Type,Time_Elapsed,Time_Spent_in_Step,Voltage,Q_in_Step,Current,Q_in_and_out_Step,Temperature,Energy_in_out,Q_in_out,Energy_in_and_out_Step,Q_in_Step,Capacitance,Energy(mWh),Start_Voltage,Energy_in_out(mWh/g),End_Voltage,RTC,Start_Temperature,Min-T,End_Temperature,Max-T,Q_End(mAh),Chg_Mid_Vtg,Power,DChg_Mid_Vtg,Capacitance_Chg(mAh),DCIR,Capacitance_DChg(mAh),Q_Chg(mAh),Engy_Chg(mWh),Q_DChg(mAh),Engy_DChg(mWh),Engy_Chg(mWh),dQ/dV(mAh/V),Engy_DChg(mWh),dQm/dV(mAh/V.g),Q_Net_DChg(mAh),Auxiliary_Channel_TU4 U(V),Net Engy_DChg(mWh),Auxiliary_Channel_TU4 T,Raw Step ID,Charge IR(O),U4 Start(V),Discharge IR(O),U4 End(V),End Temp,T4 StartTemp,Net Cap_DChg(mAh),T1 EndTemp,Net Engy_DChg(mWh),a1,Energy Efficiency,,,,,,,,,,'
    csv_header='Cycle_No,Step_No,Record_ID,Step_Type,Time_Elapsed,Time_Spent_in_Step,Voltage,Q_in_Step,Current,Q_in_and_out_Step,Temperature,Energy_in_out,Q_in_out,Energy_in_and_out_Step,Q_in_Step,Capacitance,Energy(mWh),Start_Voltage,Energy_in_out(mWh/g),End_Voltage,Power,Start Temperature,DCIR,End Temperature,RTC,End Cap,ShowAuxVolt,Chg_Mid_Vtg,ShowAuxTemp,DChg_Mid_Vtg,Platform_Time,DCIR_Step(mO),Capacitance_Chg(F),ChgCap(mAh),Capacitance_DChg(F),DChgCap(mAh),rd(mO),ChgEng(mWh),Mid_value Voltage(V),DChgEng(mWh),Discharge Fading Ratio(%),NetDChgCap(mAh),Charge Time,NetDChgEng(mWh),Discharge Time,OriStepID,Charge IR(mO),a1,Discharge IR(mO),y,End Temp(),,Net_Cap_DChg(mAh),,Net_Engy_DChg(mWh)'
    
    '''
    CycleID 	Cap_Chg(mAh) 	Cap_DChg(mAh) 	RCap_Chg(mAh/g) 	RCap_DChg(mAh/g) 	Cycle_Efficiency(%) 	Engy_Chg(mWh) 	Engy_DChg(mWh) 	REngy_Chg(mWh/g) 	REngy_Dchg(mWh/g) 	CC_Chg_Ratio(%) 	CC_Chg_Cap(mAh) 	Platform_Cap(mAh) 	Platform_RCap(mAh) 	Platfrom_Efficiency(%) 	Platform_Time(h:m:s:ms) 	Capacitance_Chg(F) 	Capacitance_DChg(F) 	rd(mO) 	Mid_value Voltage(V) 	Discharge Fading Ratio(%) 	Charge Time(h:m:s:ms) 	Discharge Time(h:m:s:ms) 	Charge IR(mO) 	Discharge IR(mO) 	End Temp(?) 	Net_Cap_DChg(mAh) 	Net_Engy_DChg(mWh) 	
    		Step ID 	Step Type 	Step Time(h:m:s:ms:us) 	Cap(mAh) 	CmpCap(mAh/g) 	Energy(mWh) 	CmpEngergy(mWh/g) 	Super Capacitace(F) 	Start Vol(V) 	End Vol(V) 	Start Temperature 	End Temperature 	End Cap 	Charge Mid-Vol(V) 	Discharge Mid-Vol(V) 	DCIR(mO) 	ChgCap(mAh) 	DChgCap(mAh) 	ChgEng(mWh) 	DChgEng(mWh) 	NetDChgCap(mAh) 	NetDChgEng(mWh) 	OriStepID 	
    				Record ID 	Time(h:m:s:ms:us) 	Voltage(V) 	Current(mA) 	Temperature(?) 	Cap(mAh) 	CmpCap(mAh/g) 	Energy(mWh) 	CmpEng(mWh/g) 	Power(mW) 	DCIR(mO) 	Realtime 	ShowAuxVolt 	ShowAuxTemp 	
    '''
    
    '''
    'Cycle_No,Step_No,Record_ID,Step_Type,Time_Elapsed,Time_Spent_in_Step,Voltage,Q_in_Step,Current,Q_in_and_out_Step,Temperature,Energy_in_out,Q_in_out,Energy_in_and_out_Step,Q_in_Step,Capacitance,Energy(mWh),Energy_in_out(mWh/g),End_Voltage,Power(mW),Start Temperature,DCIR,End Temperature,RTC,End Cap,ShowAuxVolt,Charge Mid-Vol(V),ShowAuxTemp,Discharge Mid-Vol(V),Platform_Time(h:m:s:ms),DCIR_Step(mO),Capacitance_Chg(F),ChgCap(mAh),Capacitance_DChg(F),DChgCap(mAh),rd(mO),ChgEng(mWh),Mid_value Voltage(V),DChgEng(mWh),Discharge Fading Ratio(%),NetDChgCap(mAh),Charge Time(h:m:s:ms),NetDChgEng(mWh),Discharge Time(h:m:s:ms),OriStepID,Charge IR(mO),a1,Discharge IR(mO),,End Temp(?),,Net_Cap_DChg(mAh),,Net_Engy_DChg(mWh)'
    '''
    
    '''
    'CycleID','Step ID','Record ID','Cap_Chg(mAh)','Step Type','Time(h:m:s:ms:us)','Cap_DChg(mAh)','Step Time(h:m:s:ms:us)','Voltage(V)','RCap_Chg(mAh/g)','Cap(mAh)','Current(mA)','
    RCap_DChg(mAh/g)','CmpCap(mAh/g)','Temperature(?)','Cycle_Efficiency(%)','Energy(mWh)','Cap(mAh)','Cycle_Efficiency(%)','CmpEngergy(mWh/g)','CmpCap(mAh/g)','
    Engy_Chg(mWh)','Super Capacitace(F)','Energy(mWh)','Engy_DChg(mWh)','Start Vol(V)','CmpEng(mWh/g)','REngy_Chg(mWh/g)','End Vol(V)','Power(mW)','
    REngy_Dchg(mWh/g)','Start Temperature','DCIR(mO)','CC_Chg_Ratio(%)','End Temperature','Realtime','CC_Chg_Cap(mAh)','End Cap','ShowAuxVolt','
    Platform_Cap(mAh)','Charge Mid-Vol(V)','ShowAuxTemp','Platform_RCap(mAh)','Discharge Mid-Vol(V)','xx','Platfrom_Efficiency(%)','DCIR(mO)','xx','
    Platform_Time(h:m:s:ms)','ChgCap(mAh)','xx','Capacitance_Chg(F)','DChgCap(mAh)','xx','Capacitance_DChg(F)','ChgEng(mWh)','xx','rd(mO)','DChgEng(mWh)','xx','
    Mid_value Voltage(V)','NetDChgCap(mAh)','xx','Discharge Fading Ratio(%)','NetDChgEng(mWh)','xx','Charge Time(h:m:s:ms)','OriStepID','xx','
    Discharge Time(h:m:s:ms)','xx','xx','Charge IR(mO)','xx','xx','Discharge IR(mO)','xx','xx','End Temp(?)','xx','xx','Net_Cap_DChg(mAh)','xx','xx','Net_Engy_DChg(mWh)'
    
    '''
    
    with open (inputFileName, "w") as f:
        for line in fileinput.input([inputFileName1],inplace=False):
            if  fileinput.isfirstline():
                line=csv_header + '\n'
                f.write(line)
            elif (fileinput.filelineno()==2) or (fileinput.filelineno()==3):
                f.write('\n')
            else:
                f.write(line)
        f.close()
    
    #%%
    with open(outputFileName, "w") as f:
        for line in fileinput.input([inputFileName],inplace=False):
                   line = line.replace('\t\t', '\t\t\t')
                   if fileinput.lineno()<3:                             #these represent headers
                         value_list = line.split('\t\t\t')
                         line = "\t".join(map(str, value_list)).lstrip()#separations between the entries are made to one tab space
                         result = line + '\n'
                         f.write(result)
                         
                   else:
                         try :
                             value_list = line.split('\t\t\t')
                             if (value_list[0]!=''):
                                line = '\t\t\t'.join(map(str, value_list)).lstrip()
                                line = re.sub("[\t ]+", "\t\t\t", line)
                                value_list = line.split('\t\t\t')
                                line = '\t\t'.join(map(str, value_list)).lstrip() ##
                                line = line.replace('\t\t\t', '\t\t')
                                result = line + '\n'
                                f.write(result)
                             elif (value_list[1]!=''):
                                line = '\t\t\t'.join(map(str, value_list)).lstrip()
                                line = line.replace(' ', '\t\t\t')
                                value_list = line.split('\t\t\t')
                                line = '\t\t'.join(map(str, value_list)).lstrip() ##
                                line = line.replace('\t\t\t', '\t\t')
                                result = '\t' + line + '\n'
                                f.write(result)
                                continue
                             else:
                                value_list[3]=count  #continuous record Ids
    #                            value_list = value_list[:2] + value_list[3:]
                                line = '\t\t'.join(map(str, value_list)).lstrip() ##
                                line = line.replace('\t\t\t', '\t\t')
                                result ='\t\t'+line + '\n'#different tab spacing to arrange them in a way processable by the given (Step 1)code
                                f.write(result)
                                count= count+1
                                continue
                         except IndexError:
                             continue
                         
                        
    os.remove(inputFileName)