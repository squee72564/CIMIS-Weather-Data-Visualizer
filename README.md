# [CIMIS Weather Data Visualizer](https://github.com/squee72564/CIMIS-Weather-Data-Visualizer)  
  
This is a simple website to view [California Irrigation Management Information System (CIMIS)](https://cimis.water.ca.gov/) sensor data.

All data has been manually collected from their website and rendered into a simple web-page using Flask, Matplotlib, and Scikit-learn.

## Running the application
* First clone the repository using `git clone https://github.com/squee72564/CIMIS-Weather-Data-Visualizer.git`
* Setup a  python virtual environment using `python -m venv venv`
* Activate the virtual environment by running the activate script in the created `/venv` directory
* One the virtual environment is activated install the required python packages with `pip install -r > requirements.txt`
* The .csv file that has the sensor data is over 100mb, so [git-lfs](https://git-lfs.com/) is used. Make sure it is installed and run `git lfs pull` to replace the lfs pointer with the actual .csv file
* You will need to init and populate the database for the flask server by doing the following:
	* Run `flask --app CIMIS_Flask init-db` to initialize the database
	* Run `flask --app CIMIS_Flask populate-db` to populate the database with the rows from the .csv file of sensor data
* Once all of this is done you can run the server locally in debug mode with `flask --app CIMIS_Flask run --debug`