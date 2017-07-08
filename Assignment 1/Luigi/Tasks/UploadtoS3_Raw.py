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
import DataIngestion_Normal

class UploadDirtyData(luigi.Task):

	def requires(self):
		return DataIngestion_Normal.AppendIllinoisDataSet()
	
	def input(self):
		return luigi.LocalTarget(os.path.expanduser("~") + "\\Team6_ADS_Assignment1\\Luigi\\Conf\\config.json")

	def run(self):
	
		with self.output().open("w") as f:
			f.write(os.path.expanduser("~") + "\\Team6_ADS_Assignment1\\Luigi\\Logs\\Temp\\Upload_Log.txt")
	
		with self.input().open('r') as json_file:
			json_txt =json.load(json_file)
		AWS_ACCESS_KEY = json_txt["AWSAccess"]
		AWS_SECRET_KEY = json_txt["AWSSecret"]
		conn = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY, aws_secret_access_key=AWS_SECRET_KEY)
		transfer = S3Transfer(conn)
		
		response = conn.list_buckets()    
		existent = []
		for bucket in response["Buckets"]:
			existent.append(bucket['Name'])
		
		bucket_name = 'Team6ILAssignment01'
		target_dir = os.path.expanduser("~") + "\\Team6_ADS_Assignment1\\Luigi\\Data\\DirtyData\\"
		filename = None
		file_list = os.listdir(target_dir)
		for file in file_list:
			if file.endswith('.csv'):
				filename = file
			
		if bucket_name in existent:
			filenames = []
			for key in conn.list_objects(Bucket=bucket_name)['Contents']:
				filenames.append(key['Key']) 
			
			if filename not in filenames:
				print('File upload started to s3!!!!!', '\n')
				transfer.upload_file(os.path.join(target_dir, filename), bucket_name, filename)
				print('File uploaded to s3!!!!!','\n')
				
			else:
				print('File already present on s3!!!!!', '\n')
				
		else:
			conn.create_bucket(Bucket=bucket_name)
			print('File upload started to s3!!!!!', '\n')
			transfer.upload_file(os.path.join(target_dir, filename), bucket_name, filename)
			print('File uploaded to s3!!!!!','\n')
			
	def output(self):
		return luigi.LocalTarget(os.path.expanduser("~") + "\\Team6_ADS_Assignment1\\Luigi\\Logs\\Temp\\Upload_Log.txt")