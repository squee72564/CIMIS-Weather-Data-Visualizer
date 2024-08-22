from flask import (
    Blueprint, g, request, jsonify
)
from CIMIS_Flask.db import get_db
from markupsafe import escape

bp = Blueprint('api', __name__, url_prefix='/api')

@bp.route('/stations', methods=['GET', 'OPTIONS'])
def stations_api():
    if request.method == 'OPTIONS':
        pass

    db = get_db()

    stations = db.execute(
        f'SELECT DISTINCT stn_id, stn_name, cimiss_region FROM weather_data'
    ).fetchall()

    if stations:
        result = [dict(row) for row in stations]
        return jsonify(result)

    return jsonify({'error': 'No data found'}), 404

@bp.route('/stations/<int:stn_id>', methods=['GET', 'OPTIONS'])
def station_api(stn_id):
    if request.method == 'OPTIONS':
        pass

    db = get_db()

    station_data = db.execute(
        f'SELECT * FROM weather_data WHERE stn_id = ?',
        (int(stn_id),)
    ).fetchall()

    if station_data:
        result = [dict(row) for row in station_data]
        return jsonify(result)

    return jsonify({'error': 'No data found'}), 404

@bp.route('/stations/<int:stn_id>/<string:param>', methods=['GET', 'OPTIONS'])
def station_data_api(stn_id,param):
    if request.method == 'OPTIONS':
        pass

    db = get_db()

    exclude_vals = ['stn_id', 'stn_name', 'cimiss_region', 'date', 'jul']
    col_vals = [
        col[0]
        for col
        in db.execute('SELECT * FROM weather_data LIMIT 1').description
        if col[0] not in exclude_vals
    ]

    if param not in col_vals:
        return jsonify({'error': 'Not a valid data parameter'}), 404

    station_data = db.execute(
        f'SELECT {param}, date FROM weather_data WHERE stn_id = ?',
        (int(stn_id),)
    ).fetchall()

    if station_data:
        result = [dict(row) for row in station_data]
        return jsonify(result)

    return jsonify({'error': 'No data found'}), 404
