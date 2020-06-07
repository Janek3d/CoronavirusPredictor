#!/usr/bin/python

from dash import Dash
from dash.dependencies import Input, Output, State
from datetime import datetime
import flask
import re

from layouts.app_layout import main_layout
from callbacks.callbacks import CovidEstimator

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
server = flask.Flask(__name__)
app = Dash(
    __name__, server=server, external_stylesheets=external_stylesheets)
app.layout = main_layout()
app.title = 'COVID-19 in Poland'
covid_estimator = CovidEstimator()


@app.callback(
    Output('load-info', 'children'),
    [Input('url-button', 'n_clicks'),
     Input('upload-data', 'contents')],
    [State('upload-data', 'filename'),
     State('url', 'value')]
)
def load_data(n_clicks, contents, filename, value):
    if n_clicks or filename:
        if filename:
            covid_estimator.load_data(filename)
        else:
            covid_estimator.load_data(value, web=True)
        return 'Data loaded'

@app.callback(
    Output('covid-graph', 'children'),
    [Input('predict-button', 'n_clicks')],
    [State('horizon-picker', 'start_date'),
     State('horizon-picker', 'end_date'),
     State('model-radio', 'value')])
def predict(n_clicks, start_date, end_date, value):
    if n_clicks:
        start_date = datetime.strptime(re.split('T| ', start_date)[0], '%Y-%m-%d')
        end_date = datetime.strptime(re.split('T| ', end_date)[0], '%Y-%m-%d')
        covid_estimator.set_predict_horizon(start_date, end_date)
        if value == "AR":
            covid_estimator.train_AR()
        elif value == 'VAR':
            covid_estimator.train_VAR()
        else:
            covid_estimator.train_MA()
        covid_estimator.predict()
        return [covid_estimator.get_dcc_Graph()]


if __name__ == '__main__':
    server.run(debug=True, host='0.0.0.0', port=8080)
