# -*- coding: utf-8 -*-
"""
Created on Thu Jun 30 12:44:46 2022

@author: milth
"""
from antares_http import antares
from time import monotonic

class Device():
    
    def __init__(self):
        self.name = ""
        # self.clock = clock*3600 #convert time in hours to seconds
        self.time_scheduled = 0
        self.time_used = 0
        self.time_left = 0
        self.second_scheduled = 0
        self.minute_scheduled = 0
        self.hour_scheduled = 0
        self.second_used = 0
        self.minute_used = 0
        self.hour_used = 0
        self.second_left = 0
        self.minute_left = 0
        self.hour_left = 0
        self.status_sys = 0
        self.status_user = None
        self.counter_get_data = 0
        self.counter_flag = 2
        self.time_start = 0
        self.time_now = 0
        self.id = 0
    
    def EnterData(self, user_id, name, device_id, time_scheduled, status_sys, device_status, device_read, device_token):
        self.user_id = user_id
        self.name = name
        self.id = device_id
        self.time_scheduled = time_scheduled*3600 
        self.status_sys = status_sys
        self.device_status = device_status
        self.device_read = device_read
        self.device_token = device_token
        
    def get_name(self):
        return self.name
    
    def get_device_read(self):
        return self.device_read
    
    def get_time_schedule_second(self):
        return self.time_scheduled # nanti sebelum percobaan asli, ganti bagian ini supaya yg dibaca beneran detik, krn ini masih jam
    
    def get_time_scheduled_detail(self):
        self.minute_scheduled, self.second_scheduled = divmod(self.time_scheduled, 60)
        self.hour_scheduled, self.minute_scheduled = divmod(self.minute_scheduled, 60)
        return self.hour_scheduled, self.minute_scheduled, self.second_scheduled
    
    def get_time_used(self):
        self.minute_used, self.second_used = divmod(self.time_used, 60)
        self.hour_used, self.minute_used = divmod(self.minute_used, 60)
        return self.hour_used, self.minute_used, self.second_used
    
    def get_time_left(self):
        self.time_left = self.time_scheduled - self.time_used
        self.minute_left, self.second_left = divmod(self.time_left, 60)
        self.hour_left, self.minute_left = divmod(self.minute_left, 60)
        return self.hour_left, self.minute_left, self.second_left
    
    def hour_time_used(self):
        return self.time_used
    
    def timer_start(self):
        self.time_start = monotonic()
    
    def set_time_used(self):
        self.time_now = monotonic()
        self.time_used = round(self.time_now - self.time_start)
    
    def time_scheduled_data(self):
        self.scheduled_data = f"{self.hour_scheduled} jam, {self.minute_scheduled} menit, {self.second_scheduled} detik"
        #self.scheduled_data = time.strptime(self.scheduled_data, '%H:%M:%S')
        return self.scheduled_data
    
    def time_used_data(self):
        self.used_data = f"{self.hour_used} jam, {self.minute_used} menit, {self.second_used} detik"
        #self.scheduled_data = time.strptime(self.scheduled_data, '%H:%M:%S')
        return self.used_data
    
    def time_left_data(self):
        self.left_data = f"{self.hour_left} jam, {self.minute_left} menit, {self.second_left} detik"
        #self.left_data = time.strptime(self.left_data, '%H:%M:%S')
        return self.left_data
    
    def get_status_user(self):
        antares.setAccessKey('c01538e56fc59f94:eff9cd5d2fee545c')
        self.latestData = antares.getAll('EnergyPowerMonitor', f'{self.device_read}', limit=2)
        self.readStatus = self.latestData[0]['content']['mode']
        self.readStatusBefore = self.latestData[1]['content']['mode']
        self.created_time =self.latestData[0]['created_time']
        self.created_time_before =self.latestData[1]['created_time']
        if self.created_time != self.created_time_before and self.readStatus != self.readStatusBefore:
            if self.readStatus == "ON":
                self.status_user = 1
                return self.status_user
            if self.readStatus == "OFF":
                self.status_user = 0
                return self.status_user
    
    def reset_status_user(self):
        self.status_user = None
        
    def get_status_system(self):
        return self.status_sys
    
    def set_status_system(self, status):
        antares.setAccessKey('c01538e56fc59f94:eff9cd5d2fee545c')
        if status == 0:
            self.status_sys = 0
            data = {
            'device_token' : f'{self.device_token}',
            'mode' : 'OFF'
            }
            antares.send(data, 'EnergyPowerMonitor', f'{self.device_read}')
            
        elif status == 1:
            self.status_sys = 1
            data = {
            'device_token' : f'{self.device_token}',
            'mode' : 'ON'
            }
            antares.send(data, 'EnergyPowerMonitor', f'{self.device_read}')
        
    def Display(self):
        print(f"Device Name               : {self.name}")
        print(f"Time Scehduled for Device : {self.hour_scheduled} jam, {self.minute_scheduled} menit, {self.second_scheduled} detik")
        print(f"Time Used by Device       : {self.hour_used} jam, {self.minute_used} menit, {self.second_used} detik")
        print(f"Time left by Device       : {self.hour_left} jam, {self.minute_left} menit, {self.second_left} detik")
        print(f"Device State              : {self.status_sys}")