#!/usr/bin/python

from dash import Dash
from dash.dependencies import Input, Output, State
import flask
from datetime import datetime

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
    Output('covid-graph', 'children'),  # TODO: Change to figure with proper graph
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
        covid_estimator.set_predict_horizon(datetime(2020, 6, 30))
        covid_estimator.train_AR()
        covid_estimator.predict()
        return covid_estimator.get_dcc_Graph()


if __name__ == '__main__':
    server.run(debug=True, host='0.0.0.0', port=8080)
