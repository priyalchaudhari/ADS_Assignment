
# coding: utf-8

# In[13]:

#importing required modules
import os
from os import listdir
from os.path import isfile, join
import glob
import string
import operator
import csv
import datetime
import pandas as pd
import numpy as np
import re
import json
import boto3
from boto3.s3.transfer import S3Transfer
import logging


# In[15]:

# Creating logfile for each run of the ipython notebook
log_date = datetime.datetime.now().strftime("%d%m%Y_%M%S")

logging.basicConfig(filename = log_date + '.txt',
                            filemode='a',
                            format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                            datefmt='%H:%M:%S',
                            level=logging.DEBUG)


# In[16]:

# Reading the properties file to start wrangling
properties_df = pd.read_csv('./data/properties_2016.csv', low_memory=False)
#properties_df


# In[17]:

# Filling nulls with OTHER code as given in the dictionary file
properties_df['airconditioningtypeid'] = properties_df['airconditioningtypeid'].fillna(6.0)


# In[18]:

# Filling nulls with OTHER code as given in the dictionary file
properties_df['architecturalstyletypeid'] = properties_df['architecturalstyletypeid'].fillna(19.0)


# In[19]:

#temp_df = properties_df[['regionidcounty', 'basementsqft']].copy()
#temp_df['basementsqft'] = temp_df['basementsqft'].fillna(0000.0)
#temp_df = temp_df[temp_df.basementsqft != 0000.0]
#temp_df['regionidzip'] = temp_df['regionidzip'].fillna(999999.0)
#temp_df = properties_df[properties_df['basementsqft'].isnull() == False].\
                                    #groupby('regionidzip')['basementsqft'].mean().reset_index()

#new_df = temp_df.groupby('regionidcounty')['basementsqft'].mean().reset_index()

#new_df.tail(200)


# In[20]:

# Calculating average basementsqft and filling nulls with it
basementsqft_Mean = float("{0:.2f}".format(properties_df['basementsqft'].mean()))
properties_df['basementsqft'] = properties_df['basementsqft'].fillna(basementsqft_Mean)


# In[21]:

# First replacing 0.0 with NAN to minimize wrong average calculation. 
# Replaced 0.0 with NAN as there is high possiblity that a house has a bathroom.
properties_df['bathroomcnt'] = properties_df['bathroomcnt'].replace(0.0, np.nan)

# Calculating average bathroomcount and filling nulls with it
bathroomcnt_Mean = float("{0:.2f}".format(properties_df['bathroomcnt'].mean()))
properties_df['bathroomcnt'] = properties_df['bathroomcnt'].fillna(bathroomcnt_Mean)


# In[22]:

# First replacing 0.0 with NAN to minimize wrong average calculation. 
# Replaced 0.0 with NAN as there is high possiblity that a house has a bedroom.
properties_df['bedroomcnt'] = properties_df['bedroomcnt'].replace(0.0, np.nan)

# Calculating average bathroomcount and filling nulls with it
bedroomcnt_Mean = float("{0:.2f}".format(properties_df['bedroomcnt'].mean()))
properties_df['bedroomcnt'] = properties_df['bedroomcnt'].fillna(bedroomcnt_Mean)


# In[23]:

# If no value is there then replacing it with default value as given in dictionary file
properties_df['buildingclasstypeid'] = properties_df['buildingclasstypeid'].fillna(5.0)


# In[24]:

# Calculating average value and filling nulls with it
buildingqualitytype_Mean = float("{0:.2f}".format(properties_df['buildingqualitytypeid'].mean()))
properties_df['buildingqualitytypeid'] = properties_df['buildingqualitytypeid'].fillna(buildingqualitytype_Mean)


# In[25]:

# Calculating average value and filling nulls with it
calculatedbathnbr_Mean = float("{0:.2f}".format(properties_df['calculatedbathnbr'].mean()))
properties_df['calculatedbathnbr'] = properties_df['calculatedbathnbr'].fillna(calculatedbathnbr_Mean)


# In[26]:

# If no value is there then replacing it with default value as given in dictionary file
properties_df['decktypeid'] = properties_df['decktypeid'].fillna(66.0)


# In[27]:

# Calculating average value and filling nulls with it
finishedfloor1squarefeet_Mean = float("{0:.2f}".format(properties_df['finishedfloor1squarefeet'].mean()))
properties_df['finishedfloor1squarefeet'] = properties_df['finishedfloor1squarefeet'].fillna(finishedfloor1squarefeet_Mean)


# In[28]:

# Calculating average value and filling nulls with it
calculatedfinishedsquarefeet_Mean = float("{0:.2f}".format(properties_df['calculatedfinishedsquarefeet'].mean()))
properties_df['calculatedfinishedsquarefeet'] = properties_df['calculatedfinishedsquarefeet'].                fillna(calculatedfinishedsquarefeet_Mean)


# In[29]:

# Calculating average value and filling nulls with it
finishedsquarefeet12_Mean = float("{0:.2f}".format(properties_df['finishedsquarefeet12'].mean()))
properties_df['finishedsquarefeet12'] = properties_df['finishedsquarefeet12'].                fillna(finishedsquarefeet12_Mean)


# In[30]:

# Calculating average value and filling nulls with it
finishedsquarefeet13_Mean = float("{0:.2f}".format(properties_df['finishedsquarefeet13'].mean()))
properties_df['finishedsquarefeet13'] = properties_df['finishedsquarefeet13'].                fillna(finishedsquarefeet13_Mean)


# In[31]:

# Calculating average value and filling nulls with it
finishedsquarefeet15_Mean = float("{0:.2f}".format(properties_df['finishedsquarefeet15'].mean()))
properties_df['finishedsquarefeet15'] = properties_df['finishedsquarefeet15'].                fillna(finishedsquarefeet15_Mean)


# In[32]:

# Calculating average value and filling nulls with it
finishedsquarefeet50_Mean = float("{0:.2f}".format(properties_df['finishedsquarefeet50'].mean()))
properties_df['finishedsquarefeet50'] = properties_df['finishedsquarefeet50'].                fillna(finishedsquarefeet50_Mean)


# In[33]:

# Calculating average value and filling nulls with it
finishedsquarefeet12_Mean = float("{0:.2f}".format(properties_df['finishedsquarefeet12'].mean()))
properties_df['finishedsquarefeet12'] = properties_df['finishedsquarefeet12'].                fillna(finishedsquarefeet12_Mean)


# In[34]:

# Calculating average value and filling nulls with it
finishedsquarefeet6_Mean = float("{0:.2f}".format(properties_df['finishedsquarefeet6'].mean()))
properties_df['finishedsquarefeet6'] = properties_df['finishedsquarefeet6'].                fillna(finishedsquarefeet6_Mean)


# In[35]:

# Calculating average value and filling nulls with it
fireplacecnt_Mean = float("{0:.2f}".format(properties_df['fireplacecnt'].mean()))
properties_df['fireplacecnt'] = properties_df['fireplacecnt'].                fillna(fireplacecnt_Mean)


# In[36]:

# Calculating average value and filling nulls with it
fullbathcnt_Mean = float("{0:.2f}".format(properties_df['fullbathcnt'].mean()))
properties_df['fullbathcnt'] = properties_df['fullbathcnt'].                fillna(fullbathcnt_Mean)


# In[37]:

# Calculating average value and filling nulls with it
garagecarcnt_Mean = float("{0:.2f}".format(properties_df['garagecarcnt'].mean()))
properties_df['garagecarcnt'] = properties_df['garagecarcnt'].                fillna(garagecarcnt_Mean)


# In[38]:

# Calculating average value and filling nulls with it
garagetotalsqft_Mean = float("{0:.2f}".format(properties_df['garagetotalsqft'].mean()))
properties_df['garagetotalsqft'] = properties_df['garagetotalsqft'].                fillna(garagetotalsqft_Mean)


# In[39]:

# Filling with average won't be a good idea here so replacing nulls with 'Unknown'
properties_df['hashottuborspa'] = properties_df['hashottuborspa'].                fillna('Unknown')


# In[40]:

# Filling nulls with the default value as given in the dictionary file
properties_df['heatingorsystemtypeid'] = properties_df['heatingorsystemtypeid'].                fillna(14.0)


# In[41]:

# Calculating average value and filling nulls with it
lotsizesquarefeet_Mean = float("{0:.2f}".format(properties_df['lotsizesquarefeet'].mean()))
properties_df['lotsizesquarefeet'] = properties_df['lotsizesquarefeet'].                fillna(lotsizesquarefeet_Mean)


# In[42]:

# Replacing nulls with zero as taking average and filling nulls with average would violate the next column values
properties_df['poolcnt'] = properties_df['poolcnt'].                fillna(0.0)


# In[43]:

#poolsizesum_Mean = float("{0:.2f}".format(properties_df['poolsizesum'].mean()))

#properties_df['poolsizesum'] = 0.0
#properties_df.ix[(properties_df['poolcnt'] >= 1.0) & \
                 #(properties_df['poolsizesum'].isnull() == True), 'poolsizesum'] = poolsizesum_Mean

# Replacing nulls with zero as taking average and filling nulls with average would violate the previous column values
properties_df['poolsizesum'] = properties_df['poolsizesum'].                fillna(0.0)


# In[44]:

# Filling nulls with 0.0
properties_df['pooltypeid10'] = properties_df['pooltypeid10'].                fillna(0.0)


# In[45]:

# Filling nulls with 0.0
properties_df['pooltypeid2'] = properties_df['pooltypeid2'].                fillna(0.0)


# In[46]:

# Filling nulls with 0.0
properties_df['pooltypeid7'] = properties_df['pooltypeid7'].                fillna(0.0)


# In[47]:

# Filling with average won't be a good idea here so replacing nulls with 'Unknown'
properties_df['propertycountylandusecode'] = properties_df['propertycountylandusecode'].                fillna('Unknown')


# In[48]:

# Filling with average won't be a good idea here so replacing nulls with 'Unknown'
properties_df['propertyzoningdesc'] = properties_df['propertyzoningdesc'].                fillna('Unknown')


# In[49]:

# Filling with average won't be a good idea here so replacing nulls with a default value of '00000.0'
properties_df['regionidcity'] = properties_df['regionidcity'].                fillna(00000.0)


# In[50]:

# Filling with average won't be a good idea here so replacing nulls with a default value of '00000.0'
properties_df['regionidneighborhood'] = properties_df['regionidneighborhood'].                fillna(00000.0)


# In[51]:

# Filling with average won't be a good idea here so replacing nulls with a default value of '00000.0'
properties_df['regionidzip'] = properties_df['regionidzip'].                fillna(00000.0)


# In[52]:

# Filling with average won't be a good idea here so replacing nulls with a default value of '0.0'
properties_df['storytypeid'] = properties_df['storytypeid'].                fillna(0.0)


# In[53]:

# Calculating average value and filling nulls with it
threequarterbathnbr_Mean = float("{0:.2f}".format(properties_df['threequarterbathnbr'].mean()))
properties_df['threequarterbathnbr'] = properties_df['threequarterbathnbr'].                fillna(threequarterbathnbr_Mean)


# In[54]:

# Filling nulls with the default value as given in the dictionary file
properties_df['typeconstructiontypeid'] = properties_df['typeconstructiontypeid'].                fillna(14.0)


# In[55]:

# Calculating average value and filling nulls with it
unitcnt_Mean = float("{0:.2f}".format(properties_df['unitcnt'].mean()))
properties_df['unitcnt'] = properties_df['unitcnt'].                fillna(unitcnt_Mean)


# In[56]:

# Calculating average value and filling nulls with it
yardbuildingsqft17_Mean = float("{0:.2f}".format(properties_df['yardbuildingsqft17'].mean()))
properties_df['yardbuildingsqft17'] = properties_df['yardbuildingsqft17'].                fillna(yardbuildingsqft17_Mean)


# In[57]:

# Calculating average value and filling nulls with it
yardbuildingsqft26_Mean = float("{0:.2f}".format(properties_df['yardbuildingsqft26'].mean()))
properties_df['yardbuildingsqft26'] = properties_df['yardbuildingsqft26'].                fillna(yardbuildingsqft26_Mean)


# In[58]:

# Filling with average won't be a good idea here so replacing nulls with a default value of '0000.0'
properties_df['yearbuilt'] = properties_df['yearbuilt'].                fillna(0000.0)


# In[60]:

# Calculating average value and filling nulls with it
numberofstories_Mean = float("{0:.2f}".format(properties_df['numberofstories'].mean()))
properties_df['numberofstories'] = properties_df['numberofstories'].                fillna(numberofstories_Mean)


# In[61]:

# Filling with average won't be a good idea here so replacing nulls with a default value of 'Unknown'
properties_df['fireplaceflag'] = properties_df['fireplaceflag'].                fillna('Unknown')


# In[62]:

# Calculating average value and filling nulls with it
structuretaxvaluedollarcnt_Mean = float("{0:.2f}".format(properties_df['structuretaxvaluedollarcnt'].mean()))
properties_df['structuretaxvaluedollarcnt'] = properties_df['structuretaxvaluedollarcnt'].                fillna(structuretaxvaluedollarcnt_Mean)


# In[63]:

# Calculating average value and filling nulls with it
taxvaluedollarcnt_Mean = float("{0:.2f}".format(properties_df['taxvaluedollarcnt'].mean()))
properties_df['taxvaluedollarcnt'] = properties_df['taxvaluedollarcnt'].                fillna(taxvaluedollarcnt_Mean)


# In[64]:

# Calculating average value and filling nulls with it
landtaxvaluedollarcnt_Mean = float("{0:.2f}".format(properties_df['landtaxvaluedollarcnt'].mean()))
properties_df['landtaxvaluedollarcnt'] = properties_df['landtaxvaluedollarcnt'].                fillna(landtaxvaluedollarcnt_Mean)


# In[65]:

# Calculating average value and filling nulls with it
taxamount_Mean = float("{0:.2f}".format(properties_df['taxamount'].mean()))
properties_df['taxamount'] = properties_df['taxamount'].                fillna(taxamount_Mean)


# In[66]:

# Filling with average won't be a good idea here so replacing nulls with a default value of 'Unknown'
properties_df['taxdelinquencyflag'] = properties_df['taxdelinquencyflag'].                fillna('Unknown')


# In[67]:

# Filling with average won't be a good idea here so replacing nulls with a default value of '0000.0'
properties_df['taxdelinquencyyear'] = properties_df['taxdelinquencyyear'].                fillna(0000.0)


# In[68]:

# Filling with average won't be a good idea here so replacing nulls with a default value of '00000.0'
properties_df['censustractandblock'] = properties_df['censustractandblock'].                fillna(00000.0)


# In[69]:

# Opening the file after wrangling and writing clean data into it
with open('./data/after_wrangle.csv', 'w') as myfile:
            myfile.write(properties_df.to_csv(index=False))


# In[71]:

# Opening the config file to get AWS credentials
with open('config.json') as json_file:    # opening files one by one 
        json_txt =json.load(json_file)
AWS_ACCESS_KEY = json_txt["AWSAccess"]
AWS_SECRET_KEY = json_txt["AWSSecret"]


# In[72]:

# Defining a function which transfers file to AWS S3
def sync_to_s3(target_dir, bucket_name, AWS_ACCESS_KEY, AWS_SECRET_KEY):
    if not os.path.isdir(target_dir):
        raise ValueError('target_dir %r not found.' % target_dir)

    # Creating connection to S3
    s3 = boto3.resource('s3', aws_access_key_id=AWS_ACCESS_KEY, aws_secret_access_key=AWS_SECRET_KEY)
    conn = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY, aws_secret_access_key=AWS_SECRET_KEY)
    transfer = S3Transfer(conn)

    # Getting all the existing buckets on s3
    response = conn.list_buckets()
    existent = []
    for bucket in response["Buckets"]:
        existent.append(bucket['Name'])
        
    filename = 'after_wrangle.csv'
        
    # If bucket is already present then listing all the files inside it
    if bucket_name in existent:
        filenames = []
        for key in conn.list_objects(Bucket=bucket_name)['Contents']:
            filenames.append(key['Key']) 
        
        # If file is not already present on s3 then uploading it to s3
        if filename not in filenames:
            print('File upload started to s3!!!!!', '\n')
            logging.warning("File upload started to s3!!!!!")
            transfer.upload_file(os.path.join(target_dir, filename), bucket_name, filename)
            print('File uploaded to s3!!!!!','\n')
            logging.warning("File uploaded to s3!!!!!")
            
        else:
            logging.warning("File already exist on s3!!!!")
            print('File already present on s3!!!!!', '\n')
            
    else:
        conn.create_bucket(Bucket=bucket_name)
        print('File upload started to s3!!!!!', '\n')
        logging.warning("File upload started to s3!!!!!")
        transfer.upload_file(os.path.join(target_dir, filename), bucket_name, filename)
        print('File uploaded to s3!!!!!','\n')
        logging.warning("File uploaded to s3!!!!!")
        
sync_to_s3('/usr/src/Assignment1/data', 'ZillowDataTeam06', AWS_ACCESS_KEY, AWS_SECRET_KEY)
# Calling the above created function
#sync_to_s3('C:\\Users\\Prashant\\ADS\\Assignment2\\Assignment2\\data\\', 'ZillowDataTeam06', AWS_ACCESS_KEY, AWS_SECRET_KEY)


# In[ ]:



