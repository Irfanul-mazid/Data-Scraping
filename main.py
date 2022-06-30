# importing modules
import requests #for fetching the url
import os #saving the file in the current directory
import re #extracting data using regex
import pandas as pd #for dataframe
import time #for running loop after specific time
from datetime import datetime # saving the file using todays date

#Saving the file using current time
now = datetime.now()
dt_string = now.strftime(" %d-%m-%y %H-%M-%S")

#Running the loop for set time
for i in range(48):

# fetching data from aemo
        URL = "https://visualisations.aemo.com.au/aemo/apps/api/report/ELEC_NEM_SUMMARY"
        res = requests.get(URL)

        # extracting required data from the response object
        data = res.text

        # Extracting data from the link using regex
        date = re.findall(r'{"SETTLEMENTDATE":"([0-9]{4}-[0-9]{2}-[0-9T:]{11})', data)
        regionid = re.findall(r',"REGIONID":"([A-Z0-9]{3,4})', data)
        price = re.findall(r',"PRICE":(-{0,1}[0-9]{1,6}[.][0-9]{5})', data)
        t_demand = re.findall(r',"TOTALDEMAND":([0-9]{1,6}[.][0-9]{5})', data)
        netinterchange = re.findall(r',"NETINTERCHANGE":(-{0,1}[0-9]{1,6}[.][0-9]{5})', data)
        scheduled_gen = re.findall(r',"SCHEDULEDGENERATION":([0-9]{1,6}[.][0-9]{5})', data)
        semischedule_gen = re.findall(r',"SEMISCHEDULEDGENERATION":([0-9]{1,6}[.][0-9]{5})', data)


        #print(data) #for testing
        #print(len(date),len(regionid),len(price),len(t_demand),len(netinterchange),len(scheduled_gen),len(semischedule_gen)) #for testing

        dict = {'Date': date, 'State': regionid, 'Price': price, 'Total Demand': t_demand, 'Net Inter Change': netinterchange,
                'Scheduled Generation':scheduled_gen, 'Semi-Scheduled Generation':semischedule_gen}

        if i ==0: #frist intance to create the dataframe
                energy_price_pd = pd.DataFrame(dict)

        else: #from the second step appending the new dictionary to the new dataframe
                energy_price = pd.DataFrame(dict)
                energy_price_pd = pd.concat([energy_price_pd,energy_price],ignore_index=True)

        print(energy_price_pd) #test check the current dataframe
        print(i) #test check the current number of iteration

        #saving in the current path
        csv_path = os.path.abspath(__file__)
        csv_path = f'{os.sep.join(csv_path.split(os.sep)[:-1])}{os.sep}aemo file{dt_string}.csv' #saving the file in the specific name

        #print(csv_path) #test

        energy_price_pd.to_csv(csv_path) #saving the file as csv file
        time.sleep(300) #waiting for 5 minutes to rerun the loop

print(energy_price_pd) # Test viewing the current dataframe

energy_price_pd.to_csv(csv_path) #saving the file to csv

