import luigi
import os
from os import listdir
from os.path import isfile, join
import glob
import requests
import csv
import pandas as pd
import json
import datetime
import socket
import boto3
import logging
from logging import Logger
import io
import re
import numpy as np
from boto3.s3.transfer import S3Transfer


class CleanIllinoisDataSet(luigi.Task):

	def run(self):
		
		homedir = os.path.expanduser("~")
		data_path = homedir + "\\Team6_ADS_Assignment1\\Luigi\\Data"
		if not os.path.exists(data_path):
			os.makedirs(data_path)
			
		log_time = datetime.datetime.now().strftime("%d%m%Y_%M%S")

		logging.basicConfig(filename = log_time+'.txt',
							filemode='a',
							format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
							datefmt='%H:%M:%S',
							level=logging.DEBUG)

		current_date = datetime.datetime.now().strftime("%d%m%Y")
		#current_date = '20062017'

		with open('configWrangle.json') as json_file:
			json_txt =json.load(json_file)
		AWS_ACCESS_KEY = json_txt["AWSAccess"]
		AWS_SECRET_KEY = json_txt["AWSSecret"]
		State=json_txt["state"]
		St_Id = json_txt["Station_Id"]

		conn = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY, aws_secret_access_key=AWS_SECRET_KEY)
		transfer = S3Transfer(conn)

		filenames = []

		for key in conn.list_objects(Bucket='Team6ILAssignment01')['Contents']:
			filenames.append(key['Key'])
        
		datelist = [filedate[3:11] for filedate in filenames]

		actual_file = State + '_' + current_date + '_' + St_Id + '.csv'
		actual_file_clean = State + '_' + current_date + '_' + St_Id + '_clean' + '.csv'
		target_directory = data_path
		
		if current_date in datelist:
			if actual_file_clean not in filenames:
				print("File is present for today on s3. Downloading today's file!!!!!")
				logging.warning("File is present for today on s3. Downloading today's file!!!!!")
				
				transfer.download_file('Team6ILAssignment01', actual_file, os.path.join(target_directory, actual_file))
				print('File downloaded successfully!!!!!')
				logging.warning("File downloaded successfully!!!!!")
				
				print('Starting Data Wrangling process!!!!!')
				logging.warning("Starting Data Wrangling process!!!!!")
				
				csv_data_df =pd.read_csv(actual_file,encoding='ISO-8859-1',
										usecols=[0, 1,5,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25],low_memory=False)
				
				cols = ['HOURLYVISIBILITY','HOURLYDRYBULBTEMPF','HOURLYWETBULBTEMPF','HOURLYDewPointTempF','HOURLYWindDirection',
						'HOURLYStationPressure','HOURLYPressureChange','HOURLYSeaLevelPressure','HOURLYPrecip','HOURLYAltimeterSetting'
						,'HOURLYDRYBULBTEMPC','HOURLYWETBULBTEMPC','HOURLYWindSpeed','HOURLYRelativeHumidity','HOURLYDewPointTempC']
				
				csv_data_df[cols]=csv_data_df[cols].astype(str)
				csv_data_df[cols]=csv_data_df[cols].applymap(lambda x: re.sub(r'[^0-9^\-\.]+', '', x)).replace('', np.nan).astype('float64')
				
				temp_df = csv_data_df[['HOURLYPressureTendency']].copy()
				x=temp_df["HOURLYPressureTendency"].astype('float64').mean()
				csv_data_df["HOURLYPressureTendency"]=csv_data_df["HOURLYPressureTendency"].fillna(x)
				
				csv_data_df["HOURLYPressureChange"]=csv_data_df["HOURLYPressureChange"].replace(0.0, np.nan)
				x=csv_data_df["HOURLYPressureChange"].astype('float64').mean()
				csv_data_df["HOURLYPressureChange"]=csv_data_df["HOURLYPressureChange"].fillna(x)
			
				temp_df = csv_data_df[csv_data_df["HOURLYVISIBILITY"]!=0]
				x=temp_df["HOURLYVISIBILITY"].mean()
				csv_data_df["HOURLYVISIBILITY"]=csv_data_df["HOURLYVISIBILITY"].replace(0.0,x)
				csv_data_df["HOURLYVISIBILITY"]=csv_data_df["HOURLYVISIBILITY"].fillna(x)
			
				temp_df = csv_data_df[csv_data_df["HOURLYDRYBULBTEMPF"]!=0]
				x=temp_df["HOURLYDRYBULBTEMPF"].mean()
				csv_data_df["HOURLYDRYBULBTEMPF"]=csv_data_df["HOURLYDRYBULBTEMPF"].replace(0.0,x)
				csv_data_df["HOURLYDRYBULBTEMPF"]=csv_data_df["HOURLYDRYBULBTEMPF"].fillna(x)
			
				temp_df = csv_data_df[csv_data_df["HOURLYDRYBULBTEMPC"]!=0]
				x=temp_df["HOURLYDRYBULBTEMPC"].mean()
				csv_data_df["HOURLYDRYBULBTEMPC"]=csv_data_df["HOURLYDRYBULBTEMPC"].replace(0.0,x)
				csv_data_df["HOURLYDRYBULBTEMPC"]=csv_data_df["HOURLYDRYBULBTEMPC"].fillna(x)
			
				temp_df = csv_data_df[['HOURLYWETBULBTEMPF']].copy()
				x=temp_df["HOURLYWETBULBTEMPF"].astype('float64').mean()
				csv_data_df["HOURLYWETBULBTEMPF"]=csv_data_df["HOURLYWETBULBTEMPF"].fillna(x)
			
				temp_df = csv_data_df[csv_data_df["HOURLYWETBULBTEMPC"]!=0]
				temp_df["HOURLYWETBULBTEMPC"] = temp_df["HOURLYWETBULBTEMPC"].replace('*',np.nan)
				x=temp_df["HOURLYWETBULBTEMPC"].mean()
				csv_data_df["HOURLYWETBULBTEMPC"]=csv_data_df["HOURLYWETBULBTEMPC"].replace(0.0,x)
				csv_data_df["HOURLYWETBULBTEMPC"]=csv_data_df["HOURLYWETBULBTEMPC"].fillna(x)
			
				temp_df = csv_data_df[csv_data_df["HOURLYDewPointTempF"]!=0]
				x=temp_df["HOURLYDewPointTempF"].mean()
				csv_data_df["HOURLYDewPointTempF"]=csv_data_df["HOURLYDewPointTempF"].replace(0.0,x)
				csv_data_df["HOURLYDewPointTempF"]=csv_data_df["HOURLYDewPointTempF"].fillna(x)
			
				temp_df = csv_data_df[csv_data_df["HOURLYDewPointTempC"]!=0]
				x=temp_df["HOURLYDewPointTempC"].mean()
				csv_data_df["HOURLYDewPointTempC"]=csv_data_df["HOURLYDewPointTempC"].replace(0.0,x)
				csv_data_df["HOURLYDewPointTempC"]=csv_data_df["HOURLYDewPointTempC"].fillna(x)
			
				temp_df = csv_data_df[['HOURLYRelativeHumidity']].copy()
				x=temp_df["HOURLYRelativeHumidity"].astype('float64').mean()
				csv_data_df["HOURLYRelativeHumidity"]=csv_data_df["HOURLYRelativeHumidity"].fillna(x)
			
				temp_df = csv_data_df[csv_data_df["HOURLYWindSpeed"]!=0]
				x=temp_df["HOURLYWindSpeed"].mean()
				csv_data_df["HOURLYWindSpeed"]=csv_data_df["HOURLYWindSpeed"].replace(0.0,x)
				csv_data_df["HOURLYWindSpeed"]=csv_data_df["HOURLYWindSpeed"].fillna(x)
			
				temp_df = csv_data_df[['HOURLYWindDirection']].copy()
				x=temp_df["HOURLYWindDirection"].astype('float64').mean()
				csv_data_df["HOURLYWindDirection"]=csv_data_df["HOURLYWindDirection"].fillna(x)
			
				temp_df = csv_data_df[['HOURLYWindGustSpeed']].copy()
				temp_df["HOURLYWindGustSpeed"] = temp_df["HOURLYWindGustSpeed"].replace('*',np.nan)
				x=temp_df["HOURLYWindGustSpeed"].astype('float64').mean()
				csv_data_df["HOURLYWindGustSpeed"]=csv_data_df["HOURLYWindGustSpeed"].fillna(x)
			
				temp_df = csv_data_df[csv_data_df["HOURLYStationPressure"]!=0]
				x=temp_df["HOURLYStationPressure"].mean()
				csv_data_df["HOURLYStationPressure"]=csv_data_df["HOURLYStationPressure"].replace(0.0,x)
				csv_data_df["HOURLYStationPressure"]=csv_data_df["HOURLYStationPressure"].fillna(x)
			
				temp_df = csv_data_df[csv_data_df["HOURLYSeaLevelPressure"]!=0]
				x=temp_df["HOURLYSeaLevelPressure"].mean()
				csv_data_df["HOURLYSeaLevelPressure"]=csv_data_df["HOURLYSeaLevelPressure"].replace(0.0,x)
				csv_data_df["HOURLYSeaLevelPressure"]=csv_data_df["HOURLYSeaLevelPressure"].fillna(x)
				
				with open(actual_file_clean, 'w') as myfile:
					myfile.write(csv_data_df.to_csv(index=False))
    
				os.unlink(actual_file)
    
				print('Data Wrangling process completed!!!!!')
				logging.warning("Data Wrangling process completed!!!!!")
			else:
				print('Data Wrangling process is already completed for today!!!!!')
				logging.warning("Data Wrangling process is already completed for today!!!!!")
				
		else:
			print('File is not present for today on s3!!!!!')
			logging.warning("File is not present for today on s3!!!!!")
		
		
	def output(self):
        return luigi.LocalTarget(os.path.expanduser("~") + "\\Team6_ADS_Assignment1\\Luigi\\Data\\")
		
		
		
		