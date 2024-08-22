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
This is assuming you have already cloned and setup the repository on your development computer and want to run it on another computer

First you want to do this on the computer you cloned the repository on:
1. Make sure your virtual environment is activated with by running the activate script
2. Build a .whl file with the build tool:
    * `pip install build`
    * `python -m build --wheel`
    * You can find the file in dist/cimis_flask-1.0.0-x.x.x.x.whl

Now on the computer you want to run the production server on:
1. Move the .whl file that was created to that computer
2. To populate the database with CIMIS data, you can either download your own from the website, or alternatively move the data provided in this repository into the directory where the .whl file is located on your production computer.
    * If you use the data from this repo make sure it is within `./CIMIS_Flask/data/` where `./` is the same base directory the .whl file is located so the populate script works properly
3. Install the file with `pip install dist/cimis_flask-1.0.0-x.x.x.x.whl`
6. You will need to init and populate the database for the flask server by doing the following:
	* Run `flask --app CIMIS_Flask init-db` to initialize the database
	* Run `flask --app CIMIS_Flask populate-db` to populate the database with the rows from the .csv file of sensor data
8. Configure a SECRET_KEY to some random bytes and copy to your venv instance folder:
    * `python -c "import secrets; print(f'SECRET_KEY="{secrets.token_hex()}"')"`
    * Create a config.py file in venv/var/CIMIS_Flask-instance and copy the ouput key into it
7. Install a production server like Waitress
    * `pip install waitress`
8. Tell Waitress to serve the application:
    * `waitress-serve --call 'CIMIS_Flask:create_app'`
