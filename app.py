# index page
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from server import app, server
from flask_login import logout_user, current_user
from views import success, login, login_fd, logout, abutus, searchResult

# header =
# html.Div(
#     className='header',
#     children=html.Div(
#         className='container-width',
#         style={'height': '100%'},
#         children=[
#             html.Img(
#                 # src='assets/dash-logo-stripe.svg',
#                 src='assets/LOGO.png',
#                 className='logo'
#             ),
header = html.Div(style={

    "list-style-type": "none",
    "margin": "0",
    "padding": "0",
    "overflow": "hidden",
    "background-color": "#333"
}, children=[
    html.Div(id='home', className='link', style={
        "float": "left"
    }),
    html.Div(id='Contact-us', className='link', style={
        "float": "left"
    }),
    html.Div(id='doctor', className='link', style={
        "float": "left"
    }),
    html.Div(id='search', className='link', style={
        "float": "left"
    }),
    html.Div(id='new', className='link', style={
        "float": "left"
    }),
    html.Div(id='login', className='link', style={
        "float": "left"
    }),
    html.Div(id='logout', className='link', style={
        "float": "left"
    })
])
#     ]
# )
# )

app.layout = html.Div(
    [
        header,
        html.Div([
            html.Div(
                html.Div(id='page-content', className='content'),
                className='content-container'
            ),
        ], className='container-width'),
        dcc.Location(id='url', refresh=False),
    ]
)


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/':
        return login.layout
    elif pathname == '/login':
        return login.layout_login
    # elif pathname == '/sign-up':
    #     return login.layout_signup
    elif pathname == '/Contact-us':
        return abutus.layout
    elif pathname == '/search':
        if current_user.is_authenticated:
            return searchResult.layout
        else:
            return login_fd.layout
    elif pathname == '/doctor':
        if current_user.is_authenticated:
            return searchResult.layout_doctor
        else:
            return login_fd.layout
    elif pathname == '/success':
        if current_user.is_authenticated:
            return success.layout
        else:
            return login_fd.layout
    elif pathname == '/logout':
        if current_user.is_authenticated:
            logout_user()
            return logout.layout
        else:
            return logout.layout
    else:
        return '404'


@app.callback(
    Output('search', 'children'),
    [Input('page-content', 'children')])
def cur_user(input1):
    if current_user.is_authenticated:
        return html.A('Search', href='/search', className="hoverHeader")
        # 'User authenticated' return username in get_id()
    else:
        return ''


@app.callback(
    Output('new', 'children'),
    [Input('page-content', 'children')])
def cur_user(input1):
    if current_user.is_authenticated:
        return html.A('Prediction', href='/success', className="hoverHeader")
        # 'User authenticated' return username in get_id()
    else:
        return ''


@app.callback(
    Output('Contact-us', 'children'),
    [Input('page-content', 'children')])
def cur_user(input1):
    return html.A('Contact-us', href='/Contact-us', className="hoverHeader")
    # 'User authenticated' return username in get_id()


@app.callback(
    Output('home', 'children'),
    [Input('page-content', 'children')])
def cur_user(input1):
    return html.A('Home', href='/', className="hoverHeader")
    # 'User authenticated' return username in get_id()


@app.callback(
    Output('logout', 'children'),
    [Input('page-content', 'children')])
def user_logout(input1):
    if current_user.is_authenticated:
        return html.A('Logout', href='/logout', className="hoverHeader")
    else:
        return ''


@app.callback(
    Output('doctor', 'children'),
    [Input('page-content', 'children')])
def doctor(input1):
    if current_user.is_authenticated:
        return html.A('Doctor', href='/doctor', className="hoverHeader")
    else:
        return ''


@app.callback(
    Output('login', 'children'),
    [Input('page-content', 'children')])
def user_logout(input1):
    if not current_user.is_authenticated:
        return html.A('Login', href='/login', className="hoverHeader")
    else:
        return ''


@app.callback(
    Output('sign-up', 'children'),
    [Input('page-content', 'children')])
def user_logout(input1):
    if not current_user.is_authenticated:
        return html.A('Sign up', href='/sign-up', className="hoverHeader")
    else:
        return ''


if __name__ == '__main__':
    app.run_server(debug=True)
