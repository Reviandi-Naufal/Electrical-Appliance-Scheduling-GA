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
        self.clock = 0
        self.state = 0
    
    def EnterData(self, name, clock, state):
        self.name = name
        self.clock = clock
        self.state = state
        
    def get_name(self):
        return self.name
    
    def get_time(self):
        return self.clock
    
    def get_state(self):
        return self.state
    
    def set_state(self, state):
        self.state = state
        
    def Display(self):
        print(f"Device Name  : {self.name}")
        print(f"Device Clock : {self.clock}")
        print(f"Device State : {self.state}")

if __name__ == '__main__' :
    
    name = ['device_1', 'device_2', 'device_3', 'device_4', 'device_5', 'device_6', 'device_7', 'device_8', 'device_9', 'device_10', 'device_11']
    schedule = [24, 23, 20, 16, 14, 12, 10, 9, 7, 5, 2]
    state = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    save_dev = []
    for i in range(len(schedule)):
        device = Device()
        device.EnterData(name[i], schedule[i], state[i])
        save_dev.append(device)
    """
    for i in range(len(save_dev)):
        print("----------------------------")
        save_dev[i].Display()
        print("----------------------------")
        """
    print("SYSTEM ARE ON")
    print("========================================================================")
    startSys = monotonic()
    counter = len(save_dev)
    
    while counter != 0:
        endSys = monotonic()
        
        for i in range(len(save_dev)):
            if round(endSys - startSys) == save_dev[i].get_time():
                save_dev[i].set_state(1)
                print(save_dev[i].get_name(), "is OFF")
                counter -= 1
        
        sleep(1)
    
    print("========================================================================")
    print("ALl system has been shutdown")
    print(endSys - startSys)