# -*- coding: utf-8 -*-
"""
Created on Wed Apr 20 13:19:01 2022

@author: milth
"""
from time import monotonic, sleep
import sqlalchemy
import pandas as pd
from DeviceCreator import Device
from antares_http import antares
pd.set_option('display.max_columns', None)

if __name__ == '__main__' :
    
    ## Define Mysql Engine
    engine = sqlalchemy.create_engine('mysql+mysqlconnector://root:Ismilelabn209!!@172.23.142.168:3306/db_ismile', pool_pre_ping=True)
    ## Define antares accesskey to EnergyMonitoringSystem account
    antares.setAccessKey('c01538e56fc59f94:eff9cd5d2fee545c')
    ## Retrieve data from database 
    schedule_data_all = pd.read_sql_table("hasil_penjadwalan",engine)
    device_data = pd.read_sql_table("deviceinput",engine)
    device_number = device_data.shape[0]
    schedule_data = schedule_data_all.tail(device_number)
    key_value = device_data.loc[::, ['device_id', 'device_name', 'device_name_status', 'device_name_read', 'device_token']]
    device_name_dict = {}
    device_status_dict = {}
    device_read_dict = {}
    device_token_dict = {}
    for key, value in key_value.iterrows():
        device_name_dict.update({value['device_id']: value['device_name']})
        device_status_dict.update({value['device_id']: value['device_name_status']})
        device_read_dict.update({value['device_id']: value['device_name_read']})
        device_token_dict.update({value['device_id']: value['device_token']})
    print(device_name_dict)
    print(device_status_dict)
    print(device_read_dict)
    print(device_token_dict)
    	
    schedule_data['device_name'] = schedule_data['device_id'].map(device_name_dict)
    schedule_data['device_name_status'] = schedule_data['device_id'].map(device_status_dict)
    schedule_data['device_name_read'] = schedule_data['device_id'].map(device_read_dict)
    schedule_data['device_token'] = schedule_data['device_id'].map(device_token_dict)
    schedule_data.reset_index(drop=True)
    user_id = list(schedule_data['user_id'])
    device_name = list(schedule_data['device_name'])
    device_id = list(schedule_data['device_id'])
    device_schedule = list(schedule_data['durasi'])
    device_name_status = list(schedule_data['device_name_status'])
    device_name_read = list(schedule_data['device_name_read'])
    device_token = list(schedule_data['device_token'])
    
    """
    print(schedule_data)
    print("=======================================================")
    print(device_number)
    print("=======================================================")
     """
    
    #name = ['device_1', 'device_2', 'device_3', 'device_4', 'device_5', 'device_6', 'device_7', 'device_8', 'device_9', 'device_10', 'device_11']
    #schedule = [24, 23, 20, 16, 14, 12, 10, 9, 7, 5, 2]
    status = 0 # define status (mode) alat pertama kali menjadi 0 / "OFF"
    save_dev = []
    for i in range(len(device_schedule)):
        device = Device()
        device.EnterData(user_id[i], device_name[i], device_id[i], device_schedule[i], status, device_name_status[i], device_name_read[i], device_token[i])
        save_dev.append(device)
    
    print("SYSTEM ARE ON")
    print("========================================================================")
    for device in range(len(save_dev)):
        #latestData = antares.get('EnergyPowerMonitor', f'{save_dev[device].get_device_read}')
        #readStatus = latestData['content']['mode']
        save_dev[device].set_status_system(0)
        save_dev[device].get_time_scheduled_detail()
    for i in range(len(save_dev)):
        print("----------------------------")
        save_dev[i].Display()
        print("----------------------------")
    startSys = monotonic()
    counter = len(save_dev)
    timer_db = 0
    interval_timer_db = 10
    timer_antares = 0
    interval_timer_antares = 5
    timer_counter = 0
    flag = 0
    while counter != 0:
        endSys = monotonic()
        time_scheduled_all = []
        time_used_all = []
        time_left_all = []
        for device in range(len(save_dev)):
            if timer_counter == timer_antares + interval_timer_antares:
                flag += 1
                user_command = save_dev[device].get_status_user()
                if user_command != None and save_dev[device].hour_time_used() < save_dev[device].get_time_schedule_second():
                    save_dev[device].set_status_system(user_command)
                    if user_command == 1:
                        save_dev[device].timer_start()
                        print(save_dev[device].get_name(), " is ON")
                    elif user_command == 0:
                        print(save_dev[device].get_name(), " is OFF")
                        save_dev[device].set_status_system(0)
                        #save_dev[device].reset_status_user()
                
            if save_dev[device].hour_time_used() >= save_dev[device].get_time_schedule_second() and save_dev[device].get_status_system() != 0:
                save_dev[device].set_status_system(0)
                save_dev[device].get_time_used()
                save_dev[device].get_time_left()
                print(save_dev[device].get_name(), " is OFF")
                counter -= 1
                
            elif save_dev[device].get_status_system() != 0 :
                save_dev[device].set_time_used()
                save_dev[device].get_time_used()
                save_dev[device].get_time_left()
                
            time_scheduled_all.append(save_dev[device].time_scheduled_data())
            time_used_all.append(save_dev[device].time_used_data())
            time_left_all.append(save_dev[device].time_left_data())
            #print(time_scheduled_all)
            #print(time_used_all)
            #print(time_left_all)
            #print(f"timer count : {timer_counter}")
            print(save_dev[device].hour_time_used())
            #print(user_command)
        
        if flag == len(save_dev):
            timer_antares += interval_timer_antares
            flag = 0
        
        if timer_counter == timer_db + interval_timer_db:
            columns = ['user_id','device_id','device_name','duration_scheduled','duration_used','duration_left']
            index = range(len(device_id))
            df = pd.DataFrame(columns=columns, index=index)
            df['user_id'] = user_id
            df['device_id'] = device_id
            df['device_name'] = device_name
            df['duration_scheduled'] = time_scheduled_all
            df['duration_used'] = time_used_all
            df['duration_left'] = time_left_all
            
            df.to_sql(
                name='device_usage_duration', # database table name
                con=engine,
                if_exists='replace',
                index=False
            )
            timer_db += interval_timer_db
        timer_counter += 1
        sleep(1)
    
    print("========================================================================")
    print("ALl system has been shutdown")
    print(endSys - startSys)
    
    columns = ['user_id','device_id','device_name','duration_scheduled','duration_used','duration_left']
    index = range(len(device_id))
    df = pd.DataFrame(columns=columns, index=index)
    df['user_id'] = user_id
    df['device_id'] = device_id
    df['device_name'] = device_name
    df['duration_scheduled'] = time_scheduled_all
    df['duration_used'] = time_used_all
    df['duration_left'] = time_left_all
    
    df.to_sql(
        name='device_usage_duration', # database table name
        con=engine,
        if_exists='replace',
        index=False
    )
    
    for i in range(len(save_dev)):
        print("----------------------------")
        save_dev[i].Display()
        print("----------------------------")
    
    print(df)

    # Insert Scheduling Result into Each Instance
    

