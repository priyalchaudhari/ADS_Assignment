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

class DownloadInitialDataSet(luigi.Task):
	
	def requires(self):
		return []
	
	def input(self):
		return luigi.LocalTarget(os.path.expanduser("~") + "\\Team6_ADS_Assignment1\\Luigi\\Conf\\Initial_config.json")

	def run(self):
		
		log_date = datetime.datetime.now().strftime("%d%m%Y_%M%S")
		logging.basicConfig(filename = os.path.expanduser("~") + "\\Team6_ADS_Assignment1\\Luigi\\Logs\\Task_Log\\" + log_date + '.txt',
							filemode='a',
							format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
							datefmt='%H:%M:%S',
							level=logging.DEBUG)
			
		with self.output().open("w") as f:
			f.write(os.path.expanduser("~") + "\\Team6_ADS_Assignment1\\Luigi\\Logs\\Temp\\Initial_Log.txt")
		
		with self.input().open('r') as json_file:
			json_txt =json.load(json_file)
		State=json_txt["state"]
		Team =json_txt["team"]
		Link =json_txt["link"]
		St_Id = json_txt["Station_Id"]
		AWS_ACCESS_KEY = json_txt["AWSAccess"]
		AWS_SECRET_KEY = json_txt["AWSSecret"]
		conn = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY, aws_secret_access_key=AWS_SECRET_KEY)
		connResponse = conn.list_buckets()
		bucket_list = []
		for bucket in connResponse["Buckets"]:
			bucket_list.append(bucket['Name'])
		aws_bucket = 'Team' + Team + State + 'Assignment01'
		
		if aws_bucket not in bucket_list:

			if not os.path.exists(os.path.expanduser("~") + "\\Team6_ADS_Assignment1\\Luigi\\Data\\DirtyData\\*.csv"):
				print('Starting Initial File Download!!!!!', '\n')
				response_initial = None
				for x in Link:
					for z,y in x.items():
						response_initial = requests.get(y)
						# Write to Dataframes
						if z == 'link1':
							Data_df1 = pd.read_csv(io.StringIO(response_initial.content.decode('utf-8')), low_memory=False)
						elif z == 'link2':
							Data_df2 = pd.read_csv(io.StringIO(response_initial.content.decode('utf-8')), low_memory=False)
						elif z == 'link3':
							Data_df3 = pd.read_csv(io.StringIO(response_initial.content.decode('utf-8')), low_memory=False)
						elif z == 'link4':
							Data_df4 = pd.read_csv(io.StringIO(response_initial.content.decode('utf-8')), low_memory=False)
						elif z == 'link5':
							Data_df5 = pd.read_csv(io.StringIO(response_initial.content.decode('utf-8')), low_memory=False)
						elif z == 'link6':
							Data_df6 = pd.read_csv(io.StringIO(response_initial.content.decode('utf-8')), low_memory=False)
						elif z == 'link7':
							Data_df7 = pd.read_csv(io.StringIO(response_initial.content.decode('utf-8')), low_memory=False)
						elif z == 'link8':
							Data_df8 = pd.read_csv(io.StringIO(response_initial.content.decode('utf-8')), low_memory=False)
							
				Data_df_initial = pd.concat([Data_df1, Data_df2, Data_df3, Data_df4, Data_df5, Data_df6, Data_df7, Data_df8], ignore_index=True)
					
				with open(os.path.expanduser("~") + "\\Team6_ADS_Assignment1\\Luigi\\Data\\DirtyData\\Temp.csv", "w") as f:
					f.write(Data_df_initial.to_csv(index=False))
				
				#Data_df_initial = pd.read_csv(io.StringIO(response_initial.content.decode('utf-8')), low_memory=False)                  
				Date_Initial = max(Data_df_initial['DATE'])
				date_formatted_initial = Date_Initial[8:10] + Date_Initial[5:7] + Date_Initial[:4]
				actual_file_initial = State + '_' + date_formatted_initial + '_' + St_Id + '.csv'
				os.rename(os.path.expanduser("~") + "\\Team6_ADS_Assignment1\\Luigi\\Data\\DirtyData\\Temp.csv", os.path.expanduser("~") + "\\Team6_ADS_Assignment1\\Luigi\\Data\\DirtyData\\" + actual_file_initial)
							
				print('Ending Initial File Download!!!!!', '\n')
			
			else: 
				logging.warning("Initial File already present!!!!")
				print('Initial File already present!!!!!', '\n')
	
		else:
			print('File already present!!!!!')
			logging.warning("File already present!!!!!")
			
	def output(self):
		return luigi.LocalTarget(os.path.expanduser("~") + "\\Team6_ADS_Assignment1\\Luigi\\Logs\\Temp\\Initial_Log.txt")
		
#if __name__ == "__main__":
    #luigi.run()
		