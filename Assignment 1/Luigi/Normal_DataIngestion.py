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

class DownloadIllinoisDataSet(luigi.Task):

	def input(self):
        return luigi.LocalTarget(homedir + "\\Team6_ADS_Assignment1\\Luigi\\Conf\\config.json")
		return luigi.LocalTarget(homedir + "\\Team6_ADS_Assignment1\\Luigi\\Conf\\Initial_config.json")

	def run(self):
		
		homedir = os.path.expanduser("~")
		data_path = homedir + "\\Team6_ADS_Assignment1\\Luigi\\Data"
		if not os.path.exists(data_path):
			os.makedirs(data_path)
			
		
	
		log_date = datetime.datetime.now().strftime("%d%m%Y_%M%S")

		logging.basicConfig(filename = log_date + '.txt',
							filemode='a',
							format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
							datefmt='%H:%M:%S',
							level=logging.DEBUG)

		with self.input().open('config.json') as json_file:
			json_txt =json.load(json_file)
		AWS_ACCESS_KEY = json_txt["AWSAccess"]
		AWS_SECRET_KEY = json_txt["AWSSecret"]

		conn = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY, aws_secret_access_key=AWS_SECRET_KEY)

		connResponse = conn.list_buckets()
		bucket_list = []
		for bucket in connResponse["Buckets"]:
			bucket_list.append(bucket['Name'])



		if 'Team6ILAssignment01' in bucket_list:
    
			# If initial large file is present
    
			with self.input().open('config.json') as json_file:    # opening files one by one 
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
    
			initial_file = glob.glob('*.csv')
			appendedfile = initial_file[0]
			date = appendedfile[3:11]
			maxdate = date[:4] + '-' + date[4:6] + '-' + date[6:]
        
			final_df = Data_df_new[(Data_df_new['Date_Formatted'] > maxdate)]
			Date_new = max(Data_df_new['DATE'])
			date_formatted_new = Date_new[8:10] + Date_new[5:7] + Date_new[:4]
			actual_file_new = State + '_' + date_formatted_new + '_' + St_Id + '.csv'
    
			# Write to .CSV
			if not os.path.exists(actual_file_new):
				print('Starting new file Download!!!!!', '\n')
				with self.output().open(appendedfile, "a") as f:
					f.write(final_df.to_csv(index=False,header=None))
				os.rename(appendedfile,actual_file_new)
				print('New file Downloaded and appended to Initial File!!!!!', '\n')
        
			else: 
				logging.warning("New file already present!!!!")
				print('New file already present!!!!!','\n')
        
		else:
    
			# If initial large file is not present
    
			with self.input().open('Initial_config.json') as json_file:    # opening files one by one 
				json_txt =json.load(json_file)
			State=json_txt["state"]
			Team =json_txt["team"]
			Link =json_txt["link"]
			St_Id = json_txt["Station_Id"]
			ACCESS_KEY = json_txt["AWSAccess"]
			SECRET_KEY = json_txt["AWSSecret"]
    
			if not os.path.exists('*.csv'):
				print('Starting Initial File Download!!!!!', '\n')
				response_initial = None
				for x in Link:
					for z,y in x.items():
						response_initial = requests.get(y)
						# Write to .CSV
						if z == 'link1':
							with self.output().open ('Temp.csv', "a") as f:
								f.write(response_initial.text)
						else:
							with self.output().open ('Temp.csv', "a") as f:
								for x in response_initial.text.strip().split("\n")[1:]:
									f.write(x+"\n")
                            
				Data_df_initial = pd.read_csv(io.StringIO(response_initial.content.decode('utf-8')), low_memory=False)                  
				Date_Initial = max(Data_df_initial['DATE'])
				date_formatted_initial = Date_Initial[8:10] + Date_Initial[5:7] + Date_Initial[:4]
				actual_file_initial = State + '_' + date_formatted_initial + '_' + St_Id + '.csv'
				os.rename('Temp.csv', actual_file_initial)
                            
				print('Ending Initial File Download!!!!!', '\n')
        
			else: 
				logging.warning("File already present!!!!")
				print('Initial File already present!!!!!', '\n')
				
	def output(self):
		return luigi.LocalTarget(os.path.expanduser("~") + "\\Team6_ADS_Assignment1\\Luigi\\Data\\RawData\\")