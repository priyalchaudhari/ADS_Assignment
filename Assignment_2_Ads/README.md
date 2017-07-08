# Instruction to Run the code

- Download Assignment 2 folder from github in to your homedirectory
- To get the images in the local execute: 
   - docker pull prashantvksingh/assignment2
   
## Go in docker folder:
- Exececute docker build -t team6assignment2 .
- Execute   docker run -ti team6assignment2
  - Execute docker ps -l     (to get the ID of last run container)
  - Execute docker commit (ID received from above code) team6assignment2
  - Note: In above command brackets are not needed and it should be executed each time when the image is run
  - The commit is necessary after each time the image is run or else data will be lost
 
## Open run_csv.txt and perform following:
- Install sqlcmd from Microsoft into your machine
- Open command prompt and run following steps serially:
  - Execute create table script
  - Execute create function script
  - Modify the path for file accordingly and execute the command to start bulk loading
  - Execute the next command to view the results locally
  
## Open command prompt and perform following:
- python app.py
- API will be created and it can be accessed by the displayed URL
- Go to the displayed URL
- Provide latitude and longitude to the URL and the closest 10 houses will be displayed
