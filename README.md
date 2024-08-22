# [CIMIS Weather Data Visualizer](https://github.com/squee72564/CIMIS-Weather-Data-Visualizer)  
  
This is a simple website to view [California Irrigation Management Information System (CIMIS)](https://cimis.water.ca.gov/) sensor data.

All data has been manually collected from their website and rendered into a simple web-page using Flask, Matplotlib, and Scikit-learn.

## Running the application in development environment
1. First clone the repository using `git clone https://github.com/squee72564/CIMIS-Weather-Data-Visualizer.git`
2. Setup a  python virtual environment using `python -m venv venv`
3. Activate the virtual environment by running the activate script in the created `/venv` directory
4. One the virtual environment is activated install the required python packages with `pip install -r > requirements.txt`
5. The .csv file that has the sensor data is over 100mb, so [git-lfs](https://git-lfs.com/) is used. Make sure it is installed and run `git lfs pull` to replace the lfs pointer with the actual .csv file
6. You will need to init and populate the database for the flask server by doing the following:
	* Run `flask --app CIMIS_Flask init-db` to initialize the database
	* Run `flask --app CIMIS_Flask populate-db` to populate the database with the rows from the .csv file of sensor data
7. Once all of this is done you can run the server locally in debug mode with `flask --app CIMIS_Flask run --debug`

## Deploy to production
* Follow steps 1-3 from above
4. Build a .whl file with the build tool:
    * `pip install build`
    * `python -m build --wheel`
    * You can find the file in dist/cimis_flask-1.0.0-py3-none-any.whl
    * Install the file with `pip install cimis_flask-1.0.0-py3-none-any.whl`
5. The .csv file that has the sensor data is over 100mb, so [git-lfs](https://git-lfs.com/) is used. Make sure it is installed and run `git lfs pull` to replace the lfs pointer with the actual .csv file
6. You will need to init and populate the database for the flask server by doing the following:
	* Run `flask --app CIMIS_Flask init-db` to initialize the database
	* Run `flask --app CIMIS_Flask populate-db` to populate the database with the rows from the .csv file of sensor data
8. Configure a SECRET_KEY to some random bytes and copy to your venv instance folder:
    * `python -c 'import secrets; print(f'SECRET_KEY = {secrets.token_hex()}')'`
    * Create a config.py file in venv/var/CIMIS_Flask-instance and copy the ouput key into it
7. Install a production server like Waitress
    * pip install waitress
8. Tell Waitress to serve the application:
    * `waitress-serve --call 'CIMIS_Flask:create_app'`
