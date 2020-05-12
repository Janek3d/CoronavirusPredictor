#!/usr/bin/python

import dash
import flask

from layouts.app_layout import main_layout

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
server = flask.Flask(__name__)
app = dash.Dash(
    __name__, server=server, external_stylesheets=external_stylesheets)
app.layout = main_layout()
app.title = 'COVID-19 in Poland'

if __name__ == '__main__':
    server.run(debug=True, host='0.0.0.0', port=8080)
