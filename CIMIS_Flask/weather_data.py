import io
import base64
import numpy as np
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from CIMIS_Flask.db import get_db
from sklearn.linear_model import LinearRegression
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('Agg')

bp = Blueprint('weather_data', __name__, url_prefix='/weather')

def get_plot(rows, col_value, station_id):
    dates, vals = zip(*[[row['date'], row[f'{col_value}']] for row in rows])
    dates, vals = np.array(dates), np.array(vals)
    make_ordinal = np.vectorize(lambda x: x.toordinal())
    dates_ordinal = make_ordinal(dates)
    station_name = rows[0]['stn_name']

    x = dates_ordinal.reshape(-1,1)
    y = vals

    model = LinearRegression()
    model.fit(x,y)

    linear_reg = model.predict(x)

    tick_interval = max(1, len(vals) // 15)

    plt.figure(figsize=(12,6))
    plt.plot(
            dates,
            vals,
            marker='.',
            markersize=0.7,
            linestyle='-',
            linewidth=0.5,
            color='b',
            label=f'{col_value} Data'
        )
    plt.plot(
            dates,
            linear_reg,
            linestyle='--',
            linewidth=3,
            color='r',
            label='Line of best fit'
        )
    plt.title(f'{col_value} for station {station_id}, {station_name}')
    plt.xlabel('Date')
    plt.legend()
    plt.ylabel(f'{col_value}')
    plt.grid(True)
    plt.xticks(
            ticks=dates[::tick_interval],
            labels=dates[::tick_interval],
            rotation=45
        )
    plt.tight_layout()

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.close()

    return base64.b64encode(buf.getvalue()).decode('utf-8')

@bp.route('/', methods=['GET', 'POST'])
def get_weather():
    db = get_db()

    station_pairs = db.execute(
        'SELECT DISTINCT stn_id, stn_name FROM weather_data'
    ).fetchall()

    exclude_vals = ['stn_id', 'stn_name', 'cimiss_region', 'date', 'jul']
    col_vals = [
        col[0]
        for col
        in db.execute('SELECT * FROM weather_data').description
        if col[0] not in exclude_vals
    ]

    if request.method == 'POST':
        station_id = request.form.get('station_id')
        col_value = request.form.get('col_val')

        rows = db.execute(
            f'SELECT {col_value}, date, stn_name FROM weather_data WHERE stn_id == ?',
            (int(station_id),)
        ).fetchall()

        img_base64 = get_plot(rows, col_value, station_id) 

        return render_template(
            'weather.html',
            station_pairs=station_pairs,
            col_vals=col_vals,
            image=img_base64
        )

    return render_template('weather.html', station_pairs=station_pairs, col_vals=col_vals)
