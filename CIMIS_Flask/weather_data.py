from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from CIMIS_Flask.db import get_db

bp = Blueprint('weather_data', __name__, url_prefix='/weather')

@bp.route('/', methods=['GET', 'POST'])
def get_weather():
    if request.method == 'POST':
        station_id = request.form.get('station_id')
        col_value = request.form.get('col_val')

        flash(f'Selected Station ID: {station_id}, and value: {col_value}')

        return redirect(url_for('weather_data.get_weather'))

    db = get_db()

    station_ids = [
        station['stn_id']
        for station
        in db.execute('SELECT DISTINCT stn_id FROM weather_data').fetchall()
    ]

    exclude_vals = ['stn_id', 'stn_name', 'cimiss_region', 'date', 'jul']
    col_vals = [
        col[0]
        for col
        in db.execute('SELECT * FROM weather_data').description
        if col[0] not in exclude_vals
    ]

    return render_template('weather.html', station_ids=station_ids, col_vals=col_vals)
