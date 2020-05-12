import dash_html_components as html


def graph_layout():
    """Function for generating graph layout with its components.

    :return: Graph layout as dash component
    :rtype: dash.development.base_component.ComponentMeta
    """
    layout = html.Div([
        html.H1(
            id='graph',
            children='Graph placeholder',
            style={
                'font-family': 'helvetica',
                'color': '#3B5DBC',
                'font-size': '50',
                'text-align': 'center',
                'vertical-align': 'text-top'
            }
        ),
    ])
    return layout
