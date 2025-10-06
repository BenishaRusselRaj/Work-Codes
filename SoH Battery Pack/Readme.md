# Estimating SOH for battery packs - I am updating feature branch

This code estimates the SOH and predicts the RUL of the 2 wheeler and 3 wheeler processed data.

## Sample Input files

Multiple .csv and .tsv (needs to be checked, even csv should work; better csv be default) files of below header will be processed

### 1. Combined_Summary_files
    The Combined summary files are present in a single folder in .csv format, each BIN having a file each.
   ```
  ,bin,session,start_Time,end_Time,start_V_Min,end_V_Min,start_V_Max,end_V_Max,start_Temp_Min,end_Temp_Min,start_Temp_Max,end_Temp_Max,I_Avg,I_Max,start_pack_vtg,end_pack_vtg,start_Avg_Vtg,end_Avg_Vtg,T_pack_Max,T_pack_Min,T_pack_Avg,dV_Max,dV_Min,dV_Avg,dT_fet_Max,dT_fet_Min,dT_fet_Avg,Vol_s0_mins,Vol_s1_mins,Vol_s2_mins,Vol_s3_mins,Vol_s4_mins,Vol_s5_mins,Vol_s6_mins,Vol_s7_mins,Vol_s8_mins,Temp_s0_mins,Temp_s1_mins,Temp_s2_mins,Temp_s3_mins,Temp_s4_mins,Temp_s5_mins,Temp_s6_mins,Time_Estimate,Time_in_session_mins,Remark,Session_Type,Cycle_No_Chg_DChg,Cycle_No_session

   ```
### 2. One Time Data file
    The One Time Data file(OTD file) is a .tsv file containing the charging session data of all the bins.
```
bin	vin	session	time	startSOC	endSOC	chargingEnergy	consumedEnergy	chargingDuration	SOH	lifeCycle
```


## Sample Output files

Generates 2 folders each with output files for each battery and a .csv file

### 1. OTD_Merged_Summary_files
   * Contains file with name OTD_Merged_Summary_file_BINxxxxxxx.csv for each battery
   * The OTD file and the combined summary files are merged according to the session ID
   
   ```
,Unnamed: 0,bin,session,start_Time,end_Time,start_V_Min,end_V_Min,start_V_Max,end_V_Max,start_Temp_Min,end_Temp_Min,start_Temp_Max,end_Temp_Max,start_current,end_current,start_pack_vtg,end_pack_vtg,start_Avg_Vtg,end_Avg_Vtg,start_Avg_Temp,end_Avg_Temp,Vol_s0_mins,Vol_s1_mins,Vol_s2_mins,Vol_s3_mins,Vol_s4_mins,Vol_s5_mins,Vol_s6_mins,Vol_s7_mins,Vol_s8_mins,Temp_s0_mins,Temp_s1_mins,Temp_s2_mins,Temp_s3_mins,Temp_s4_mins,Temp_s5_mins,Temp_s6_mins,Time_Estimate,Time_in_session_mins,Remark,Session_Type,Cycle_No_Chg_DChg,Cycle_No_session,bin_1,vin,session_1,time,startSOC,endSOC,chargingEnergy,consumedEnergy,chargingDuration,SOH,lifeCycle
0,0,INAMR0010102E3000909,00001.2018110316460301.002,2018-11-01 11:38:22,2018-11-01 11:38:22,,,,,,,,,,,,,,,,,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,First and last values were NAN;Taken the first valid data1 for summary,DChg,0.0,1.0,,,,,,,,,,,
1,1,INAMR0010102E3000909,00001.2018110316460301.002,2018-11-02 09:27:29,2018-11-02 17:41:42,,,,,,,,,,,,,,,,,0.0,0.0,20.85,24.75,17.016666666666666,32.33333333333333,73.6,17.016666666666666,308.65,0.0,0.0,179.16666666666663,126.73333333333332,0.0,188.31666666666663,0.0,494.21666666666664,494.2166666666666,First and last values were NAN;Taken the first valid data1 for summary,DChg,0.0,1.0,,,,,,,,,,,
2,2,INAMR0010102E3000909,00001.2018110316460301.002,2018-11-02 17:41:42,2018-11-02 18:03:07,,3.548,,3.5580000000000003,,0.0,,37.79,,,,,,3.5522307692307686,,0.0,,,,,,,,,,,,,,,,,21.416666666666668,21.416666666666668,Rest_included,Rest,0.0,1.0,,,,,,,,,,,
3,3,INAMR0010102E3000909,00001.2018110316460301.002,2018-11-02 18:03:07,2018-11-03 01:09:20,3.548,4.075,3.5580000000000003,4.082,0.0,0.0,37.79,35.45,,,,,3.5522307692307686,4.078615384615385,34.023529411764706,32.430588235294124,0.0,0.0,0.0,7.0166666666666675,21.0,20.016666666666666,30.016666666666666,48.01666666666666,300.15,0.0,0.0,0.0,417.2166666666667,9.0,0.0,0.0,426.2166666666666,426.2166666666666,---,Chg,1.0,1.0,INAMR0010102E3000909,MDCNJJKPBDP000363,00001.2018110316460301.002,2018-11-04 06:54:33,5.0,100.0,944.0,1018.0,17874.0,100.0,2.0
4,4,INAMR0010102E3000909,00001.2018110316460301.002,2018-11-03 11:15:52,2018-11-03 16:38:01,3.548,4.075,3.5580000000000003,4.082,0.0,0.0,37.79,35.45,,,,,3.5522307692307686,4.078615384615385,34.023529411764706,32.430588235294124,0.0,0.0,12.0,9.016666666666666,71.26666666666667,12.0,63.9,68.93333333333334,85.03333333333333,0.0,0.0,90.03333333333332,151.46666666666667,59.65000000000001,21.0,0.0,322.15,322.15,First and last values were NAN;Taken the first valid data1 for summary,DChg,1.0,1.0,,,,,,,,,,,
5,5,INAMR0010102E3000909,00001.2018110709130004.005,2018-11-05 10:19:14,2018-11-05 17:19:20,3.548,4.075,3.5580000000000003,4.082,0.0,0.0,37.79,35.45,,,,,3.5522307692307686,4.078615384615385,34.023529411764706,32.430588235294124,0.0,0.0,0.0,1.0166666666666666,35.16666666666667,94.91666666666666,134.36666666666665,106.46666666666668,48.16666666666666,0.0,0.0,0.0,0.0,0.0,420.1,0.0,420.1,420.1,First and last values were NAN;Taken the first valid data1 for summary,DChg,1.0,2.0,,,,,,,,,,,
   
   ```
   
### 2. SOH_Capacity_Graphs_all_bins_code_merged_otd
   * Contains separate folders for each BIN, containing various SOH graphs

### 3. Final_Cycle_Nos_and SOH_time_included
   * This is a .csv file containing the Cycle numbers and SOH values

   ```
,bin,nc_bms,SOH_BMS,nc_otd,SOH_otd,nc_cell_testing,SOH_cell_testing,start_Time,end_Time,Total_Time_spent,Time_in_days
0,INAMR0010102E3000909,0.0,99.95,33.0,99.56930509104423,38.0,99.964,2018-11-05 17:46:40,2019-02-07 20:41:39,94 days 02:54:59.000000000,94.1215162037037
1,INAMR0010102E3002009,0.0,99.96,5.0,99.04386276203995,8.0,89.636,2018-11-12 15:20:49,2019-10-18 17:40:33,340 days 02:19:44.000000000,340.097037037037
2,INAMR0010103I2500109,0.0,99.98,1.0,99.7737556561086,3.0,99.999,2019-10-16 20:29:53,2019-10-16 21:37:55,0 days 01:08:02.000000000,0.04724537037037037
3,INAMR0010103I2500209,0.0,99.93,3.0,99.87234042553192,5.0,99.99,2019-10-15 13:16:50,2019-10-24 10:12:57,8 days 20:56:07.000000000,8.872303240740742
4,INAMR0010103I2500309,0.0,99.92,5.0,94.02455322455322,7.0,100.0,2019-10-10 17:14:20,2019-10-16 21:24:47,6 days 04:10:27.000000000,6.173923611111111
5,INAMR0010103I2500409,0.0,99.93,2.0,99.3556131758379,4.0,99.997,2019-10-16 22:37:02,2019-10-23 22:20:38,6 days 23:43:36.000000000,6.988611111111111

   ```

## How to use
* Insert files inside Sample Input files folder into Data folder.


## Built With

* Python

## Versioning - see how do we do.

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/your/project/tags). 

## Authors

* Benisha
* Sushant M M
