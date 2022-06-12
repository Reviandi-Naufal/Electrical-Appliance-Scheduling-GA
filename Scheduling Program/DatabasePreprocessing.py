# -*- coding: utf-8 -*-
"""
Created on Mon Jun  6 14:39:46 2022

@author: milth
"""

import sqlalchemy
import pandas as pd

class schedule_data_processing():
    
    def __init__(self):
        self.user_id = 0
        self.device_id = []
        self.Tagihan = 0
        self.Tarif = 0
        self.daya_total = 0
        self.daya_listrik = ""
        self.tingkat_prioritas = ""
        self.ranges = []
        self.value = []
        self.Power = []
        self.scheduled = []
        self.energy_usage = 0
        self.energy_threshold = 0
        self.scheduled_date = ""
        self.scheduled_time = ""
    
    def get_data(self, billing_data, device_data, index):
        #device_data_copy = device_data.copy()
        #device_data_copy.sort_values(by='user_id')
        self.user_id = index
        self.instance_device_data = device_data[device_data['user_id'] == index]
        self.instance_billing_data = billing_data[billing_data['user_id_bill'] == index]
        self.device_id = list(self.instance_device_data['device_id'])
        self.Tagihan = self.instance_billing_data.iloc[0,3]
        self.daya_listrik = self.instance_billing_data.iloc[0,2]
        #self.tingkat_prioritas = self.instance_device_data['tingkat_prioritas']
        self.daya_total = self.instance_device_data['total_daya']
    
    def preprocessing(self):    
        ## Preprocessing Data
        # Define Data Tarif Listrik
        if self.daya_listrik == "900":
            self.Tarif = 1352
        else:
            self.Tarif = 1444.7
        
        # Collect Time Ranges and Value Data
        title_mapping = {"Very High":1, "High":2, "Medium":3, "Low":4, "Very Low":5}
        self.instance_device_data['tingkat_prioritas'] = self.instance_device_data['tingkat_prioritas'].map(title_mapping)
        #for dataset in self.instance_device_data:
         #   dataset[-1] = dataset[-1].map(title_mapping)
        #instance_device_data_copy = self.instance_device_data.sort()
        for prioritas in self.instance_device_data['tingkat_prioritas']:
            if prioritas == 1:
                self.ranges.append([20,25])
                self.value.append(500) 
            elif prioritas == 2:
                self.ranges.append([15,20])
                self.value.append(400)
            elif prioritas == 3:
                self.ranges.append([10,15])
                self.value.append(300)
            elif prioritas == 4:
                self.ranges.append([5,10])
                self.value.append(200)
            elif prioritas == 5:
                self.ranges.append([1,5])
                self.value.append(100)
        
        # Collect Power Data
        for daya in self.daya_total:
           self.Power.append(daya)
    
    def retrieve_data(self, scheduled, energy_usage, energy_threshold, scheduled_date, scheduled_time):
        self.scheduled = scheduled
        self.energy_usage = energy_usage
        self.energy_threshold = energy_threshold
        self.scheduled_date = scheduled_date
        self.scheduled_time = scheduled_time
        
    def database_df(self):
        columns = ['user_id', 'device_id', 'durasi', 'tanggal', 'waktu']
        index = range(len(self.device_id))
        self.df = pd.DataFrame(columns=columns, index=index)
        self.df['user_id'] = self.user_id
        self.df['device_id'] = self.device_id
        self.df['durasi'] = self.scheduled
        self.df['tanggal'] = self.scheduled_date
        self.df['waktu'] = self.scheduled_time
    
    def Display(self):
        print("==================================================")
        print(self.instance_device_data)
        print(self.instance_billing_data)
        print(f"Device ID              : {self.device_id}")
        print(f"Ranges waktu Scheduling: {self.ranges}")
        print(f"Value device           : {self.value}")
        print(f"Taris Listrik          : {self.Tarif}")
        print(f"Tagihan Listrik        : {self.Tagihan}")
        print(f"Daya Tiap Device       : {self.Power}")
        print(f"Hasil Penjadwalan      : {self.scheduled}")
        print(f"Total Energi           : {self.energy_usage}")
        print(f"Batas Energi           : {self.energy_threshold}")
        print(f"Tanggal Penjadwalan    : {self.scheduled_date}")
        print(f"Waktu Penjadwalan      : {self.scheduled_time}")
        print("==================================================")

if __name__ == '__main__':
    
    ## Define Mysql Engine
    engine = sqlalchemy.create_engine('mysql+mysqldb://root:MilitenSire360@localhost:3306/appliance_db', pool_pre_ping=True)
    
    # Retrieve data from database 
    billing_data = pd.read_sql_table("billinginput",engine)
    device_data = pd.read_sql_table("deviceinput", engine)
    indexes = list(device_data['user_id'].unique())
    indexes.sort(reverse=False)
    user_data = []
    for index in indexes:
        User = schedule_data_processing()
        User.get_data(billing_data=billing_data, device_data=device_data, index=index)
        User.preprocessing()
        user_data.append(User)

    
    for i in range(len(user_data)):
        print("----------------------------")
        user_data[i].Display()
        print("----------------------------")