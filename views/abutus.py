# Dash configuration
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output,State

from server import app

# Create app layout
layout = html.Div(children=[
    dcc.Location(id='abutus', refresh=True),
    dcc.Location(id='url_login2', refresh=True),
    html.Div(
        className="container",
        children=[
            html.Div(
                html.Div(
                    className="row",
                    children=[
                        html.Div(
                            className="ten columns",
                            children=[
                                html.Br(),
                                #html.Div('User disconnected - Please login to view the success screen again'),
                            ]
                        ),
                        html.Div(
                            className="two columns",
                            # children=html.A(html.Button('LogOut'), href='/')
                            children=[
                                html.Br(),
                                html.Button(id='back-button1', children='Go back', n_clicks=0)
                            ]
                            
                            
                            
                            
                            
                            
                        ),
                        dcc.Markdown('''
                        


# Contact us :
If you have any questions or comments you would like to share with us, please give us some of your time to do so, so that we can serve you better, please send a message by e-mail.

### Saudi Arabia ,Riyadh




'''),

                    ]
                )
            )
        ]
    )
])
layout2 ="<div><p>hellow world </p>"
# Create callbacks
@app.callback(Output('url_login2', 'pathname'),
              [Input('back-button1', 'n_clicks')])
def logout_dashboard(n_clicks):
    if n_clicks > 0:
        return '/'
