
# coding: utf-8

# In[1]:

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


# In[ ]:

log_date = datetime.datetime.now().strftime("%d%m%Y_%M%S")

logging.basicConfig(filename = log_date + '.txt',
                            filemode='a',
                            format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                            datefmt='%H:%M:%S',
                            level=logging.DEBUG)


# In[3]:

with open('config.json') as json_file:
    json_txt =json.load(json_file)
AWS_ACCESS_KEY = json_txt["AWSAccess"]
AWS_SECRET_KEY = json_txt["AWSSecret"]

conn = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY, aws_secret_access_key=AWS_SECRET_KEY)

connResponse = conn.list_buckets()
bucket_list = []
for bucket in connResponse["Buckets"]:
    bucket_list.append(bucket['Name'])


# In[ ]:

if 'Team6ILAssignment01' in bucket_list:
    
    # If initial large file is present
    
    with open('config.json') as json_file:    # opening files one by one 
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
        with open(appendedfile, "a") as f:
            #for x in response_new.text.strip().split("\n")[1:]:
                #f.write(x+"\n")
            f.write(final_df.to_csv(index=False,header=None))
        os.rename(appendedfile,actual_file_new)
        print('New file Downloaded and appended to Initial File!!!!!', '\n')
        
    else: 
        logging.warning("New file already present!!!!")
        print('New file already present!!!!!','\n')
        
else:
    
    # If initial large file is not present
    
    with open('Initial_config.json') as json_file:    # opening files one by one 
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
                    with open ('Temp.csv', "a") as f:
                        f.write(response_initial.text)
                else:
                    with open ('Temp.csv', "a") as f:
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


# In[ ]:

def sync_to_s3(target_dir, bucket_name, AWS_ACCESS_KEY, AWS_SECRET_KEY):
    if not os.path.isdir(target_dir):
        raise ValueError('target_dir %r not found.' % target_dir)

    s3 = boto3.resource('s3', aws_access_key_id=AWS_ACCESS_KEY, aws_secret_access_key=AWS_SECRET_KEY)
    conn = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY, aws_secret_access_key=AWS_SECRET_KEY)
    transfer = S3Transfer(conn)

    response = conn.list_buckets()
    existent = []
    for bucket in response["Buckets"]:
        existent.append(bucket['Name'])
        
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
            #s3.Object(bucket_name, filename[0]).put(Body=open(os.path.join(target_dir, filename[0]), 'rb'))
            #s3.meta.client.upload_file(os.path.join(target_dir, filename), bucket_name, filename)
            print('File upload started to s3!!!!!', '\n')
            transfer.upload_file(os.path.join(target_dir, filename), bucket_name, filename)
            print('File uploaded to s3!!!!!','\n')
            logging.warning("File uploaded to s3!!!!!")
            
        else:
            logging.warning("File already exist on s3!!!!")
            print('File already present on s3!!!!!', '\n')
            
    else:
        conn.create_bucket(Bucket=bucket_name)
        #s3.Object(bucket_name, filename[0]).put(Body=open(os.path.join(target_dir, filename[0]), 'rb'))
        #s3.meta.client.upload_file(os.path.join(target_dir, filename), bucket_name, filename)
        print('File upload started to s3!!!!!', '\n')
        transfer.upload_file(os.path.join(target_dir, filename), bucket_name, filename)
        print('File uploaded to s3!!!!!','\n')
        logging.warning("File uploaded to s3!!!!!")
        
    #s3.Bucket(bucket_name).download_file(filename, os.path.join(target_dir, filename))
    #print(glob.glob('*'))
        
sync_to_s3('/usr/src/Assignment1', 'Team6ILAssignment01', AWS_ACCESS_KEY, AWS_SECRET_KEY)


# In[ ]:



