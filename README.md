# Instruction to Run the code:

- Download Assignment 1 folder from github in to your homedirectory
- Go in beforewrangling folder 
- Exececute docker build -t assignment01beforewrangling .
- Execute   docker run -it assignment01beforewrangling
- Execute docker ps -l     (to get the ID of last run container)
 - Execute docker commit (ID received from above code) assignment01beforewrangling
 - Note: In above command brackets are not needed and it should be executed each time when the image is run
 - The commit is necessary after each time the image is run or else data will be lost.
 - Go in afterwrangling folder 
 - Exececute docker build -t assignment01afterwrangling .
 - Execute   docker run -it assignment01afterwrangling
 - Execute docker ps -l     (to get the ID of last run container)
 - Execute docker commit (ID received from above code) assignment01afterwrangling
 - Note: In above command brackets are not needed and it should be executed each time when the image is run
 - The commit is necessary after each time the image is run or else data will be lost.
  - To get the images in the local: execute docker pull prashantvksingh/assignment1
 - Log File will be created inside dockerImage. You can see it by executing ls inside /bin/bash of image path.

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

![This is the graph for dry bulb analysis ovet the years](https://user-images.githubusercontent.com/25044602/27504622-8edba18e-585b-11e7-8f26-9f30bae1e3d3.png)
- Conclusion
- We can see two important results from above plotted graph:
- 1954 is the hottest year as on average the temperature is highest as compared to other years
- 1993 is the coldest year as on average the temperature is lowest as compared to other years
- In the below two graphs we dig deeper into month level to see the temperature variation.

### 2. Monthly analysis of the hottest and coldest year 

![Graph for year 1954](https://user-images.githubusercontent.com/25044602/27504642-20155a64-585c-11e7-9183-da661a8df2d7.png)
- conclusion
- From above graph we can see that:
- The temperature variation is not smooth or we can say that slope is not gradual for most of the months.
- Due to these sudden rise of temperature between months, the temperature rise could have felt more to the people.
- The below graph shows that during 1954 the average wind speed was 9.4 mph, which was 5th highest recorded average windspeed till date. 
- Combine this with the wind speed during those months, the real feel temperature would have felt more.

### 3. Wind Speed Analysis 

![Graph for average wind speed over the years](https://user-images.githubusercontent.com/25044602/27504650-5c21f120-585c-11e7-8551-2528537e2644.png)

### 4.Temparature Graph for year 1993 

![1993 graph](https://user-images.githubusercontent.com/25044602/27504666-ae5b95e0-585c-11e7-91a4-29e80b6977a7.png)
- conclusion 
#### From the above graph we can say that:
- The temperature variation is smooth or we can say that slope is gradual for most of the months.
- Due to these gradual rise of temperature between months, the temperature decrease could have felt more to the people.
- As from the windspeed graph, we can see that during 1993 the average wind speed was 8.6 mph, which was way above the average windspeed as compared with average windspeed in adjacent years.
- Combine this gradual decrease in temperature with the wind speed during those months, the real feel temperature would have dropped more.

### 5. Average Dew Point Temperature and Humidity over the months

![Humidity](https://user-images.githubusercontent.com/25044602/27504689-06a8439c-585d-11e7-96a0-ae728f3d0748.png)

- Conclusion 
 #### From the above graph we can say that:
- The average humidity remains more or less the same throught the year.
- The top three most humid months each year in ascending order are as follows:
    - January
    - August
    - December
 ### Dew point graph : 
![newplot 4](https://user-images.githubusercontent.com/25044602/27504717-8b6cc738-585d-11e7-9033-1d260d67447d.png)
- conclusion :
#### We can see from the above two graphs that:
- Relative humidity is highest in the months of January, August and December.
- The average dew point temperature is lowest in January, quite low in December and pretty high in August.
- We can assume below two things from above two observations that:
    - It snows heavily in the months of January and December
    - It rains heavily in the month of August
    
### 6 . Wet bulb analysis: 
- The wet-bulb temperature (WBT) is the lowest temperature that can be reached by evaporating water into the air.
- The difference between the dry bulb temperature and wet bulb temperature determines how much dry the air is. 
- If DBT-WBT is large, then the air has lower relative humidity

![newplot 5](https://user-images.githubusercontent.com/25044602/27504734-d5b37490-585d-11e7-910c-da7e50aab3eb.png)

- conclusion 
### From the above graph we can say that:
- Data is not proper between 1973-2003.
- There is sudden rise and fall of wet bulb temperature.
- Ideally a wet bulb temperature increases with the relative humidity and we have seen that relative humidity is more or less through the year.So, there is something wrong with the data provided.

# Data Wrangling Proposal
- There are many null values in the columns that we are using. So, we will be filling them with proper values in the data wrangling process.
- For few temperature columns the temperature is appended with alphabets. So, we will either remove those alphabets as we are not using those alphabets in our analysis or we will strip those alphabets to a new column to preserve them.
- There are few columns that we are not using in our analysis and have constant data. So, we will be removing them.
- Plus, there are many columns that have no data at all from 1947 till date. So, we will be removing them

## Step 5: Dockerize the whole part as a docker image. 
- Dockerized the whole set as 1 docker image and constructed a run.sh file for running the image 

## Step 6: Data Wrangling 
- Perform oulier analysis and missing value analysis on dataset and cleaned the data 
- For cleaning removed the columns which are constant and not needed for analysis. 
- Removed the tailing characters like 'S' and 'T' to the numeric values and created a separate column with the meaning of those characters 
- Also there are lot of blank rows and missing data in the file firstly calculated the mean of a column and the replaced blank values with the avg. value of that column. 
- Avg. is calculated using only the present values. 
- After these steps data seemed pretty cleaned and ready for analysis 

## Step 7 : Analysis on clean data: 


### 1. Dry Bulb Temp Analysis

- The dry-bulb temperature (DBT) is the temperature of air measured by a thermometer freely exposed to the air but shielded from radiation and moisture. 
- DBT is the temperature that is usually thought of as air temperature, and it is the true thermodynamic temperature.

![Nw graph after cleaned data for dry bulb temp.](https://user-images.githubusercontent.com/25044602/27504781-f10e579a-585e-11e7-8e13-17c071e66a5f.png)

- Conclusion
- We can see two important results from above plotted graph:
- 1954 is the hottest year as on average the temperature is highest as compared to other years
- 1979 is the coldest year as on average the temperature is lowest as compared to other years
- In the below two graphs we dig deeper into month level to see the temperature variation.
- As you can see the coldest year has changed and is correct one as the history suggest years between 1978 to 1984 were the coldest in ILLInois

### 2. Monthly analysis of the hottest and coldest year 

![1954 monthly graph](https://user-images.githubusercontent.com/25044602/27504812-a7eb862c-585f-11e7-8cba-1a115352d81b.png)
- From above graph we can see that:
- The temperature variation is not smooth or we can say that slope is not gradual for most of the months.
- Due to these sudden rise of temperature between months, the temperature rise could have felt more to the people.
- The below graph shows that during 1954 the average wind speed was 9.4 mph, which was 5th highest recorded average windspeed till date. 
- Combine this with the wind speed during those months, the real feel temperature would have felt more.

### 3. Wind Speed Analysis 

![Grapth for avg wind speed over the years](https://user-images.githubusercontent.com/25044602/27504823-d8fb12c8-585f-11e7-9b73-ddab54186ce4.png)
- As you can see chicago is known for it windy natute the speed is in high range 
### 4.Temparature Graph for year 1979

![1979 graph](https://user-images.githubusercontent.com/25044602/27504834-04068e7a-5860-11e7-8828-a682032b9ea8.png)
#### From the above graph we can say that:
- The temperature variation is smooth or we can say that slope is gradual for most of the months.
- Due to these gradual rise of temperature between months, the temperature decrease could have felt more to the people.
- As from the windspeed graph, we can see that during 1979 the average wind speed was 8.6 mph, which was way above the average windspeed as compared with average windspeed in adjacent years.
- Combine this gradual decrease in temperature with the wind speed during those months, the real feel temperature would have dropped more.

### 5. Average Dew Point Temperature and Humidity over the months

![Humidity](https://user-images.githubusercontent.com/25044602/27504839-20b27854-5860-11e7-8980-ccf4b028e1bd.png)

- Conclusion 
 #### From the above graph we can say that:
- The average humidity remains more or less the same throught the year.
- The top three most humid months each year in ascending order are as follows:
    - January
    - August
    - December
  - After cleaning this data remains pretty much the same so such changes observed after cleaning the data the graph is pretty much the same 
 ### Dew point graph : 
![Dew point analysis](https://user-images.githubusercontent.com/25044602/27504850-56605c6e-5860-11e7-9a45-58e4d756179c.png)

- this data is also remains the same after cleaning. 
#### We can see from the above two graphs that:
- Relative humidity is highest in the months of January, August and December.
- The average dew point temperature is lowest in January, quite low in December and pretty high in August.
- We can assume below two things from above two observations that:
    - It snows heavily in the months of January and December
    - It rains heavily in the month of August
    
### 6 . Wet bulb analysis: 
- The wet-bulb temperature (WBT) is the lowest temperature that can be reached by evaporating water into the air.
- The difference between the dry bulb temperature and wet bulb temperature determines how much dry the air is. 
- If DBT-WBT is large, then the air has lower relative humidity

![Wet bulb graph](https://user-images.githubusercontent.com/25044602/27504864-7f49be90-5860-11e7-868a-0dcdb0583ca4.png)


- conclusion 
### From the above graph we can say that:
- There is sudden rise and fall of wet bulb temperature.
- Ideally a wet bulb temperature increases with the relative humidity and we have seen that relative humidity is more or less through the year.So, there is something wrong with the data provided.
- As you can see there is a significant change here in analysis as we filled the missing values between 1997 to 2003. we are getting a straight because of the average values. 

### Step 8. Dockerize the second part 
- created the docker image of the second part with run.sh file 

### step 9: 
- Created a log file for the task everyday. Evry step in the code is recorded in a log file and that file is uploaded to s3 bucket everyday you run the code. 











