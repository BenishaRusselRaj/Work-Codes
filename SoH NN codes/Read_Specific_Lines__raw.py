# -*- coding: utf-8 -*-
"""
Created on Tue Sep 27 11:27:12 2022

@author: IITM
"""

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
import os
import re
inputFileName1 = "E:\\BRD\\Sample 3.1\\BRD_3.1_25Deg_AllCycles.txt"
inputFileName =  os.path.splitext(inputFileName1)[0] + "_1.txt" #change input file name for data already having the headers
outputFileName = os.path.splitext(inputFileName1)[0] + "_modified_arranged.txt"
count=1; result=''
#%%
# csv_header='Cycle_No,Step_No,Record_ID,Step_Type,Time_Elapsed,Time_Spent_in_Step,Voltage,Q_in_Step,Current,Q_in_and_out_Step,Temperature,Energy_in_out,Q_in_out,Energy_in_out,Q_in_Step(mAh/g),Super Capacitace,Energy(mWh),Start_Voltage,Energy_in_out(mWh/g),End_Voltage,Power,Start Temperature,DCIR(mO),End Temperature,RTC,Q_End,ShowAuxVolt,Chg_Mid_Vtg,ShowAuxTemp,DChg_Mid_Vtg,DCIR(mO),a1,Q_Chg,a2,Q_Dchg,a3,Energy_Chg,a4,Energy_DChg,a5,Q_Net_DChg,a6,Energy_Net_DChg,a7,OriStepID,y,Chg_IR(mO),,DChg_IR(mO),,End_Temp,,Q_Net_DChg(mAh),,Net_Engy_DChg(mWh),,' # 6Amp Tester
# csv_header='Cycle_No,Step_No,Record_ID,Step_Type,Time_Elapsed,Time_Spent_in_Step,Voltage,Q_in_Step,Current,Q_in_and_out_Step,Temperature,Energy_in_out,Q_in_out,Energy_in_out,Q_in_Step(mAh/g),Capacitance,Energy(mWh),Start_Voltage,Energy_in_out(mWh/g),End_Voltage,RTC,Start_Temperature,Plat_Cap(mAh),End_Temperature,Plat_Cap_Density(mAh/g),Q_End(mWh),Plat_Cap_Eff(%),Chg_Mid_Vtg,Plat_Time,DChg_Mid_Vtg,Chg_Capacitance,DCIR,DChg_Capacitance,Q_Chg(mAh),Engy_Chg(mWh),Q_DChg(mAh),Engy_DChg(mWh),Engy_Chg(mWh),dQ/dV(mAh/V),Engy_DChg(mWh),dQm/dV(mAh/V.g),Q_Net_DChg(mAh),Auxiliary_ChannelTU4,Raw_Step_ID,a1,U4_Start,a2,U4_End,a3,T4_Start_Temp,a4,T1_EndTemp,a5,,,,,,,' #6Amp Tester
# csv_header='Cycle_No,Step_No,Record_ID,Step_Type,Time_Elapsed,Time_Spent_in_Step,Voltage,Q_in_Step,Current,Q_in_and_out_Step,Q_in_out,Start_Voltage,Energy_in_out,End_Voltage,Power,y,Chg_Mid_Vtg,DCIR,RTC,a1,a2,a3,,,DChg_Mid_Vtg,,,,,'
csv_header='Cycle_No,Step_No,Record_ID,Energy_in_cycle,Step_Type,Time_Elapsed,Charge_in_Cycle,Time_Spent_in_Step,Voltage,Q_in_and_out_Step,Q_in_Step,Current,Energy_out_cycle,Energy_in_out_Step,Q_in_out,Power,Start_Voltage,Energy_in_Step,y,End_Voltage,Energy_in_out,a1,Chg_Mid_Vtg,a2,DCIR,DChg_Mid_Vtg,RTC,,,'
with open (inputFileName, "w") as f:
    for line in fileinput.input([inputFileName1],inplace=False):
        if  fileinput.isfirstline():
            line=csv_header + '\n'
            f.write(line)
        elif (fileinput.filelineno()==2):   ## or (fileinput.filelineno()==3)
            f.write('\n')
        else:
            f.write(line)
    f.close()

#%%
with open(outputFileName, "w") as f:
    for line in fileinput.input([inputFileName],inplace=False):
               # line = line.replace('\t\t', '\t\t\t')
               if fileinput.lineno()<3:                             #these represent headers
                     value_list = line.split('\t\t') ##3t
                     line = "\t".join(map(str, value_list)).lstrip()#separations between the entries are made to one tab space
                     result = line + '\n'
                     f.write(result)
               else:
                     try :
                         value_list = line.split('\t\t') ##3t
                         if (value_list[0]!=''):
                            if len(value_list)==7:
                                line = '\t\t'.join(map(str, value_list)).lstrip() ##3t
                                # line = re.sub("[\t ]+", "\t\t\t", line)
                                value_list = line.split('\t\t') ##3t
                                line = '\t\t\t'.join(map(str, value_list)).lstrip()
                                # line = line.replace('\t\t\t', '\t\t')
                                result = line + '\n'
                                f.write(result)
                            elif len(value_list)==10:
                                line = '\t\t'.join(map(str, value_list)).lstrip() ##3t
                                # line = re.sub("[\t ]+", "\t\t\t", line)
                                value_list = line.split('\t\t') ##3t
                                line = '\t\t\t'.join(map(str, value_list)).lstrip()
                                # line = line.replace('\t\t\t', '\t\t')
                                result = '\t'+line +'\n'
                                f.write(result)                               
                         elif (value_list[1]!=''):
                            line = '\t\t'.join(map(str, value_list)).lstrip() ##3t
                            ## line = line.replace(' ', '\t\t\t')
                            value_list = line.split('\t\t') ##3t
                            line = '\t\t\t'.join(map(str, value_list)).lstrip()
                            # line = line.replace('\t\t\t', '\t\t')
                            result = '\t\t' + line + '\n'
                            f.write(result)
                            continue
                         else:
                            value_list[3]=count  #continuous record Ids
#                            value_list = value_list[:2] + value_list[3:]
                            line = '\t\t\t'.join(map(str, value_list)).lstrip()
                            line = line.replace('\t\t\t', '\t\t')
                            result ='\t\t'+line + '\n'#different tab spacing to arrange them in a way processable by the given (Step 1)code
                            f.write(result)
                            count= count+1
                            continue
                     except IndexError:
                         continue
                     
                    
