from flask import render_template
from CIMIS_Flask import create_app

def test_config():
    assert not create_app().testing
    assert create_app({'TESTING': True}).testing

def test_home(client):
    response = client.get('/')
    assert response.status_code == 200

def test_weather_data(client):
    assert client.get('/weather/').status_code == 200
    response = client.post('/weather/', data={'station_id': '184', 'col_val': 'eto_in'})
    assert response.status_code == 200
