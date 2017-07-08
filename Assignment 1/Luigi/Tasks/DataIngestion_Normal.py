import luigi
import os
from os import listdir
from os.path import isfile, join
import glob
import requests
import csv
import json
import datetime
import boto3
import shutil
import logging
from boto3.s3.transfer import S3Transfer
import pandas as pd
import io
import UploadtoS3_Initial

class AppendIllinoisDataSet(luigi.Task):
	
	def requires(self):
		return UploadtoS3_Initial.UploadInitialData()

	def input(self):
		return luigi.LocalTarget(os.path.expanduser("~") + "\\Team6_ADS_Assignment1\\Luigi\\Conf\\config.json")

	def run(self):
		
		with self.output().open("w") as f:
			f.write(os.path.expanduser("~") + "\\Team6_ADS_Assignment1\\Luigi\\Logs\\Temp\\Normal_Log.txt")
		
		# If initial large file is present    
		with self.input().open('r') as json_file:
			json_txt =json.load(json_file)
		State=json_txt["state"]
		Team =json_txt["team"]
		Link =json_txt["link"]
		St_Id = json_txt["Station_Id"]
		ACCESS_KEY = json_txt["AWSAccess"]
		SECRET_KEY = json_txt["AWSSecret"]
    
		response_new = requests.get(Link)
		
		Data_df_new = pd.read_csv(io.StringIO(response_new.content.decode('utf-8')), low_memory=False)
		Data_df_new['Date_Formatted'] = pd.to_datetime(Data_df_new['DATE']).dt.strftime('%d-%m-%Y')    
		initial_file = glob.glob(os.path.expanduser("~") + "\\Team6_ADS_Assignment1\\Luigi\\Data\\DirtyData\\*.csv")
		appendedfile = initial_file[0]
		#date = appendedfile[3:11]
		date = appendedfile[-23:-15]
		maxdate = date[:4] + '-' + date[4:6] + '-' + date[6:]
        
		final_df = Data_df_new[(Data_df_new['Date_Formatted'] > maxdate)]
		
		Date_new = max(Data_df_new['DATE'])
		date_formatted_new = Date_new[8:10] + Date_new[5:7] + Date_new[:4]
		actual_file_new = State + '_' + date_formatted_new + '_' + St_Id + '.csv'
		
		if not os.path.exists(os.path.expanduser("~") + "\\Team6_ADS_Assignment1\\Luigi\\Data\\DirtyData\\" + actual_file_new):
			print('Starting new file Download!!!!!', '\n')
			with open(appendedfile, "a") as f:
				f.write(final_df.to_csv(index=False,header=None))
			os.rename(appendedfile, os.path.expanduser("~") + "\\Team6_ADS_Assignment1\\Luigi\\Data\\DirtyData\\" + actual_file_new)
			print('New file Downloaded and appended to Initial File!!!!!', '\n')
        
		else: 
			print('New file already present!!!!!','\n')
		
	def output(self):
		return luigi.LocalTarget(os.path.expanduser("~") + "\\Team6_ADS_Assignment1\\Luigi\\Logs\\Temp\\Normal_Log.txt")
		
#if __name__ == "__main__":
    #luigi.run()