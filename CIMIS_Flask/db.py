import sqlite3
import click
import csv
from flask import current_app, g

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db

def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

def populate_db():
    db = get_db()
    lines_read = 0

    with current_app.open_resource('data/combined_daily.csv', mode='rt') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                db.execute(
                    '''
                    INSERT INTO weather_data (
                        stn_id, stn_name, cimiss_region, date, jul, 
                        eto_in, precip_in, sol_rad, avg_vap_pres, max_air_temp, 
                        min_air_temp, avg_air_temp, max_rel_hum, min_rel_hum, 
                        avg_rel_hum, dew_point, avg_wind_speed, wind_run, avg_soil_temp
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''',
                    (
                        int(row['Stn Id']), row['Stn Name'], row['CIMIS Region'], row['Date'], int(row['Jul']),
                        float(row['ETo (in)']), float(row['Precip (in)']), float(row['Sol Rad (Ly/day)']),
                        float(row['Avg Vap Pres (mBars)']), float(row['Max Air Temp (F)']),
                        float(row['Min Air Temp (F)']), float(row['Avg Air Temp (F)']),
                        float(row['Max Rel Hum (%)']), float(row['Min Rel Hum (%)']),
                        float(row['Avg Rel Hum (%)']), float(row['Dew Point (F)']),
                        float(row['Avg Wind Speed (mph)']), float(row['Wind Run (miles)']),
                        float(row['Avg Soil Temp (F)'])
                    )
                )
            except:
                print(f'Exception with : {row["Stn Id"]} - {row["Date"]}')
            else:
                lines_read += 1

        db.commit()

        return lines_read


@click.command('init-db')
def init_db_command():
    '''Clear existing data and create new tables'''

    init_db()
    click.echo('Initialized the database.')

@click.command('populate-db')
def populate_db_command():
    '''Populate the db with the .csv file'''

    added_items = populate_db()
    click.echo(f'Populated the database with {added_items} instanced.')

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
    app.cli.add_command(populate_db_command)

