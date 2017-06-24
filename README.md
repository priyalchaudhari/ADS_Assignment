# Instruction to Run the code:

# Report of the analysis 

## Step 1 : Initial data Ingestion 
- Firstly constructed a Initialcongig.json file with liks from the data from 1947 to current date in 2017 
- Using those links data all all those years will be dounloaded in .csv format. 
### If you order data again and run the code only new data will be appended to the file and that file will be uploaded to amazon s3 bucket. 
- If file for that day is already present on amazon bucket it will not upload the data. 

## Step 2: Dataingestion : 
- This step will run after the initial data ingestion step. 
- The new data from the receiving response will be uploaded to s3 bucket 
- this step will creat a new file for every day it will run and it will contain the data till current date

## Step 3 : Performed EDA on RAW data : 
- First performed data analysis on raw data and tried finding some insights 

### 1. Dry Bulb Temp Analysis

- The dry-bulb temperature (DBT) is the temperature of air measured by a thermometer freely exposed to the air but shielded from radiation and moisture. 
- DBT is the temperature that is usually thought of as air temperature, and it is the true thermodynamic temperature.
