# -*- coding: utf-8 -*-
"""
Created on Wed Apr 20 13:19:01 2022

@author: milth
"""
from time import monotonic, sleep

class Device():
    
    def __init__(self):
        self.name = ""
        # self.clock = clock*3600 #convert time in hours to seconds
        self.time_scheduled = 0
        self.time_used = 0
        self.status = 0
    
    def EnterData(self, name, time_scheduled, status):
        self.name = name
        self.time_scheduled = time_scheduled
        self.status = status
        
    def get_name(self):
        return self.name
    
    def get_time_scheduled(self):
        return self.time_scheduled
    
    def get_time_used(self):
        return self.time_used
    
    def set_time_used(self):
        self.time_used += 1
    
    def get_status(self):
        return self.status
    
    def set_status(self, status):
        self.status = status
        
    def Display(self):
        print(f"Device Name               : {self.name}")
        print(f"Time Scehduled for Device : {self.time_scheduled}")
        print(f"Time Used by Device       : {self.time_used}")
        print(f"Device State              : {self.status}")

if __name__ == '__main__' :
    
    name = ['device_1', 'device_2', 'device_3', 'device_4', 'device_5', 'device_6', 'device_7', 'device_8', 'device_9', 'device_10', 'device_11']
    schedule = [24, 23, 20, 16, 14, 12, 10, 9, 7, 5, 2]
    status = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    save_dev = []
    for i in range(len(schedule)):
        device = Device()
        device.EnterData(name[i], schedule[i], status[i])
        save_dev.append(device)
    
    for i in range(len(save_dev)):
        print("----------------------------")
        save_dev[i].Display()
        print("----------------------------")
        
    print("SYSTEM ARE ON")
    print("========================================================================")
    for device in range(len(save_dev)):
        save_dev[device].set_status(1)
    startSys = monotonic()
    counter = len(save_dev)
    
    while counter != 0:
        endSys = monotonic()
        
        for device in range(len(save_dev)):
            if round(endSys - startSys) == 8 and device == 6:
                save_dev[device].set_status(0)
                print(save_dev[device].get_name(), "is OFF")
                counter -= 1
                
            elif save_dev[device].get_time_used() == save_dev[device].get_time_scheduled() and save_dev[device].get_status() != 0:
                save_dev[device].set_status(0)
                print(save_dev[device].get_name(), "is OFF")
                counter -= 1
                
            elif save_dev[device].get_status() != 0 :
                save_dev[device].set_time_used()
        
        sleep(1)
    
    print("========================================================================")
    print("ALl system has been shutdown")
    print(endSys - startSys)
    
    for i in range(len(save_dev)):
        print("----------------------------")
        save_dev[i].Display()
        print("----------------------------")
