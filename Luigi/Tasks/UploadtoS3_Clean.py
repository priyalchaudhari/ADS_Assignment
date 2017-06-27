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
import luigi
import DataWrangling

class UploadCleanData(luigi.Task):

	def requires(self):
		return DataWrangling.DataCleaning()
	
	def input(self):
		return luigi.LocalTarget(os.path.expanduser("~") + "\\Team6_ADS_Assignment1\\Luigi\\Conf\\configWrangle.json")

	def run(self):
	
		os.unlink(os.path.expanduser("~") + "\\Team6_ADS_Assignment1\\Luigi\\Logs\\Temp\\Initial_Log.txt")
		os.unlink(os.path.expanduser("~") + "\\Team6_ADS_Assignment1\\Luigi\\Logs\\Temp\\Normal_Log.txt")
		os.unlink(os.path.expanduser("~") + "\\Team6_ADS_Assignment1\\Luigi\\Logs\\Temp\\Wrangle_Log.txt")
		os.unlink(os.path.expanduser("~") + "\\Team6_ADS_Assignment1\\Luigi\\Logs\\Temp\\Upload_Log.txt")
		os.unlink(os.path.expanduser("~") + "\\Team6_ADS_Assignment1\\Luigi\\Logs\\Temp\\UploadInitial_Log.txt")
	
		with self.input().open('r') as json_file:
			json_txt =json.load(json_file)
		AWS_ACCESS_KEY = json_txt["AWSAccess"]
		AWS_SECRET_KEY = json_txt["AWSSecret"]
		State=json_txt["state"]
		St_Id = json_txt["Station_Id"]
		
		conn = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY, aws_secret_access_key=AWS_SECRET_KEY)
		transfer = S3Transfer(conn)
		
		
		response = conn.list_buckets()
		existent = []
		for bucket in response["Buckets"]:
			existent.append(bucket['Name'])
		
		bucket_name = 'Team6ILAssignment01'
		target_dir = os.path.expanduser("~") + "\\Team6_ADS_Assignment1\\Luigi\\Data\\CleanData\\"
		
		current_file = glob.glob(target_dir + '*.csv')
		current_date = current_file[0][-29:-21]
		actual_file_clean = State + '_' + current_date + '_' + St_Id + '_clean' + '.csv'
		filename = None
		file_list = os.listdir(target_dir)
		
		if actual_file_clean in file_list:
			filename = actual_file_clean    
			
			if bucket_name in existent:
				filenames = []
				for key in conn.list_objects(Bucket=bucket_name)['Contents']:
					filenames.append(key['Key'])
			
				if filename not in filenames:
					print('File upload started to s3!!!!!', '\n')
					transfer.upload_file(os.path.join(target_dir, filename), bucket_name, filename)
					print('File uploaded to s3 for ', current_date,'!!!!!','\n')
				
				else:
					logging.warning("File already exist on s3!!!!")
					print('File already present on s3 for ', current_date,'!!!!!', '\n')
				
			else:
				conn.create_bucket(Bucket=bucket_name)
				print('File upload started to s3 for ', current_date,'!!!!!', '\n')
				transfer.upload_file(os.path.join(target_dir, filename), bucket_name, filename)
				print('File uploaded to s3 for ', current_date,'!!!!!','\n')
				
		else:
			print("Data file is either not present for ", current_date, " or wrangling is already been completed for ", current_date,".Check previous msg!!!!!")
			
	def output(self):
		return []