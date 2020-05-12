import dash_core_components as dcc
import dash_html_components as html

import layouts.style.style as style

def main_layout():
    """Create main layout for app

    :return: GUI layout as dash component
    :rtype: dash,development.base_component.ComponentMeta
    """
    layout = html.Div([
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
                # Data Load section
                html.Div([
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
                        children=[]
                    ),
                    html.Button(
                        id='url-button',
                            n_clicks=0,
                            children='Load',
                            style={
                                'margin': style.PADDING,
                                'backgroundColor': style.BUTTON_COLOR
                            }
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
                        },
                        multiple=False,
                    ),
                ]),
            ]
        )
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
    return layout
