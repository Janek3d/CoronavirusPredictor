import dash_core_components as dcc
import dash_html_components as html
from datetime import datetime

import layouts.style.style as style

DEFAULT_WEB_DATA = \
    'https://raw.githubusercontent.com/dtandev/coronavirus/master/data/CoronavirusPL%20-%20General.csv'


def upload_data_layout():
    """Function for generating layout section for uploading data from web or file

    :return: Generated layout
    :rtype: dash.development.base_component.ComponentMeta
    """
    return html.Div([
        dcc.Input(
            id='url',
            placeholder='URL to data csv',
            list='url_history',
            style={
                "textAlign": "center",
            },
        ),
        html.Datalist(
            id='url_history',
            children=[
                html.Option(
                    value=DEFAULT_WEB_DATA
                )
            ]),
        html.Button(
            id='url-button',
            n_clicks=0,
            children='Load',
            style={
                'margin': style.PADDING,
                'backgroundColor': style.BUTTON_COLOR
            }
        ),
        html.H4(
            children='or',
        ),
        dcc.Upload(
            id='upload-data',
            children=html.Div(
                ["Drap and drop or click to select a file to upload"]
            ),
            style={
                "width": "40%",
                "height": "60px",
                "lineHeight": "60px",
                "borderWidth": "1px",
                "borderStyle": "dashed",
                "borderRadius": "5px",
                "textAlign": "center",
                "margin": "10px",
                "margin-left": "30%",
            },
            multiple=False,
        ),
    ])

def predict_horizon_layout():
    """Function for generating layout section for selecting predict horizon

    :return: Generated layout
    :rtype: dash.development.base_component.ComponentMeta
    """
    return html.Div([
        html.H6(
            children='Set predict horizon:',
            style={
                "display": "inline-block"
            }
        ),
        dcc.DatePickerRange(
            id='horizon-picker',
            start_date=datetime(2020, 5, 20),
            min_date_allowed=datetime(2020, 3, 3),
            end_date=datetime(2020, 7, 20),
        )
    ])

def main_layout():
    """Create main layout for app

    :return: GUI layout as dash component
    :rtype: dash.development.base_component.ComponentMeta
    """
    return html.Div([
        html.Div(
            [
                html.H1(
                    children='COVID-19 in Poland',
                    style={
                        'font-family': 'helvetica',
                        'color': '#3B5DBC',
                        'font-size': '50',
                        'text-align': 'center',
                        'vertical-align': 'text-top'
                    }
                ),
        upload_data_layout(),
        predict_horizon_layout(),
        dcc.RadioItems(
            id='model-radio',
            options=[
                {'label': 'AR model', 'value': 'AR'},
                {'label': 'MA model', 'value': 'MA'}
            ],
            value='AR',
            labelStyle={'display': 'inline-block'}
        ),
        html.Button(
            'Predict',
            id='predict-button',
        ),
        html.Div(
            id='load-info'        )
        ]),
        html.Div(
            id='covid-graph',
        ),
    ],
        style={
            'text-align': 'center',
            'font-family': 'helvetica',
            'position': 'absolute',
            'top': '0',
            'left': '0',
            'width': '100%',
            'height': '100%',
            'backgroundColor': '#FFFFFF'
    })
