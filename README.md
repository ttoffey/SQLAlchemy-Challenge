# SQLAlchemy-Challenge - Surfs Up

![surfs-up.png](Resources/surfs-up.png)

Congratulations! You've decided to treat yourself to a long holiday vacation in Honolulu, Hawaii! this research project involved the hawaii.sqlite databse and the two tables - Measurement and Stations. 


### Objectives

Using SQLAlchemy ORM queries, Pandas and Matplotlib, we were challenged to complete the following:

## Step One - Precipitation and Station Analysis

### Precipitation Analysis

   1. Start by finding the most recent date in the data set.

   2. Using this date, retrieve the average precipitation per day for the previous 12 months. The query should be sorted by date ascending. 
   
   3. Load the query results into a Pandas DataFrame and set the index to the date column.
   
   4. Plot the results using the DataFrame `plot` method. 

![precipitation](Resources/Precipitation.png)

   5. Use Pandas to print the summary statistics for the precipitation data. 

### Station Analysis

   1. Design a query to calculate the total number of stations in the dataset.

   2. Design a query that lists all stations with their corresponding observation count in descending order (observation count corresponds to the number of rows per station).

   3. Which station id is the most active (i.e., has the greatest number of observations)?

   4. Calculate the lowest, highest, and average temperature for that station id (i.e., the one with the greatest number of observations).

   5. Design a query to retrieve the last 12 months of temperature observation data (TOBS) for the most active station.

   6. Plot the results as a histogram with `bins=12`.

![station-histogram](Resources/MostActiveStation.png)


## Step 2 - Climate App

   1. Use Flask to create the following routes.

### Routes

* `/`

  * Home page.

  * List all routes that are available.

* `/api/v1.0/precipitation`

  * Using the query from part 1 (most recent 12 months of precipitation data), convert the query results to a dictionary using `date` as the key and `prcp` as the value.
  * Return the JSON representation of your dictionary (note the specific format of your dictionary as required from above).

* `/api/v1.0/stations`

  * Return a JSON list of stations from the dataset.

* `/api/v1.0/tobs`

  * Query the dates and temperature observations of the **most active station** for the most recent 12 months of data.
  * Return a JSON list of temperature observations (TOBS) for that year.

* `/api/v1.0/<start>` and `/api/v1.0/<start>/<end>`

  * Create a query that returns the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
  * When given the start date only, calculate min, max, and avg for all dates greater than and equal to the start date.
  * When given the start and the end date, calculate the minimum, average, and maximum obvserved temperature for dates between the start and end date inclusive.
  * Return a JSONified dictionary of these minimum, maximum, and average temperatures.

### Analysis
Dataset contains 9 stations and daily temperature readings from 1/1/2010 to 8/23/2017.
Based on the Precipitation Analysis for August 2016 to August 2017, October to January, April and June to July may be a good time to visit.


### Techologies Used
SQLAlchemy
Pandas 
Matplotlib

### Project Status
Base project completed.

### Suggestions to Improve Analysis
Considering location of the stations using the longitude and latitude contained in the Stations table. 

### Issues
1. Issue with Visual Studio Code finding Python debugger and Flask. 


