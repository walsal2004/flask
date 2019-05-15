import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

from server import app, User
from flask_login import login_user
from werkzeug.security import check_password_hash
import users_mgt as um
from flask_login import current_user


# is_login = "block" if current_user.is_authenticated else "none"
layout = html.Div(
    children=[
        html.Div(
            className="container",
            children=[
                # dcc.Location(id='url_go_to_login', refresh=True),
                dcc.Markdown('''
                        
                        
                        
                        
                        
# Breast Cancer Predictor 

Breast cancer begins when the cells in the breast begin to get out of control, that occurs almost entirely in women. Normal breast cells become cancer because of changes (mutations) in DNA. 

DNA is the chemical in our cells that makes up our gens. Genes have the instructions for how our cells function.



            '''),
                html.Img(
                    # src='assets/dash-logo-stripe.svg',
                    src='assets/dna.jpg',
                    className="six columns"
                ),
                html.Div('''Please log in to continue:''', id='h1'
                        #  , style={
#                         # "display": f"{is_login}"
#                     }
                                    ),
                html.Div(
                    # style={
                    #     "display": f"{is_login}"},
                    # # method='Post',
                    children=[
                        # dcc.Input(
                        #     placeholder='Enter your username',
                        #     type='text',
                        #     id='uname-box'
                        # ),
                        # dcc.Input(
                        #     placeholder='Enter your password',
                        #     type='password',
                        #     id='pwd-box'
                        # ),
                        # html.Button(
                        #     children='Login',
                        #     n_clicks=0,
                        #     type='submit',
                        #     id='login-button'
                        # ),
                        html.Button(
                            children=[
                                html.A('Login', href='/login')
                            ],
                            n_clicks=0,
                            type='button',
                            # id='go-to-login'
                        ),

                        # html.Div(id='output-container-button',
                        #     children='Enter a value and press submit'),
                        # html.Div(children='', id='output-state'),

                    ]
                ),
            ]
        )
    ]
)
layout_signup = html.Div(
    children=[
        html.Div(
            className="container",
            children=[
                dcc.Location(id='url_signup', refresh=True),
                dcc.Markdown('''
                        
                        
                        
                        
                        
# Breast Cancer Predictor 

Breast cancer begins when the cells in the breast begin to get out of control, that occurs almost entirely in women. Normal breast cells become cancer because of changes (mutations) in DNA. 

DNA is the chemical in our cells that makes up our gens. Genes have the instructions for how our cells function.



            '''),
                html.Img(
                    # src='assets/dash-logo-stripe.svg',
                    src='assets/dna.jpg',
                    className="six columns"
                ),
                html.Div('''Please log in to continue:''', id='h1'),
                html.Div(
                    # method='Post',
                    children=[
                        dcc.Input(
                            placeholder='Enter your username',
                            type='text',
                            id='name-singup'
                        ), dcc.Input(
                            placeholder='Enter your email address',
                            type='text',
                            id='email-singup'
                        ),
                        dcc.Input(
                            placeholder='Enter your password',
                            type='password',
                            id='pwd-singup'
                        ),
                        html.Button(
                            children='signup',
                            n_clicks=0,
                            type='submit',
                            id='signup-button'
                        ),
                        html.Button(
                            children='Contact Us',
                            n_clicks=0,
                            # type='submit',
                            id='AboutUs-button'
                        ),

                        # html.Div(id='output-container-button',
                        #     children='Enter a value and press submit'),
                        html.Div(children='', id='output-state-signup'),

                    ]
                ),
            ]
        )
    ]
)

layout_login = html.Div(

    children=[
        html.Div(
            className="container",
            style={
                "display": "grid"
            },
            children=[
                dcc.Location(id='url_login', refresh=True),
                dcc.Input(
                    placeholder='Enter your username',
                    type='text',
                    id='uname-box'
                ),
                dcc.Input(
                    placeholder='Enter your password',
                    type='password',
                    id='pwd-box'
                ),
                html.Button(
                    children='Login',
                    n_clicks=0,
                    type='submit',
                    id='login-button'
                ),
                html.Button(
                    children='Forget Password',
                    n_clicks=0,
                    type='submit',
                    id='Forget-password'
                ),
                html.Div(children='', id='output-state'
                         , style={
                        "color": "red"
                    }),
                html.Div(children='', id='forget-password'
                         , style={
                        "color": "green"
                    })
            ])
    ]
)


@app.callback(Output('url_login', 'pathname'),
              [Input('login-button', 'n_clicks')],
              [State('uname-box', 'value'),
               State('pwd-box', 'value')])
def sucess(n_clicks, input1, input2):
    user = User.query.filter_by(username=input1).first()
    if user:
        if check_password_hash(user.password, input2):
            login_user(user)
            return '/doctor'
        else:
            pass
    else:
        pass


@app.callback(Output('url_signup', 'pathname'),
              [Input('signup-button', 'n_clicks')],
              [State('name-singup', 'value'),
               State('email-singup', 'value'),
               State('pwd-singup', 'value')])
def signup(n_clicks, name, email, password):
    um.create_user_table()
    # username, password, email

    if name and password and email:
        try:
            um.add_user(name, password, email)
        except:
            pass
        user = User.query.filter_by(username=name).first()
        if check_password_hash(user.password, password):
            login_user(user)
            return '/success'
        else:
            pass
    else:
        pass


@app.callback(Output('output-state-signup', 'children'),
              [Input('signup-button', 'n_clicks')],
              [State('name-singup', 'value'),
               State('email-singup', 'value'),
               State('pwd-singup', 'value')])
def update_output_signup(n_clicks, name, email, password):
    if n_clicks > 0:
        if not name or not password or not email:
            return 'you should enter name and password'
    return ''


@app.callback(Output('output-state', 'children'),
              [Input('login-button', 'n_clicks')],
              [State('uname-box', 'value'),
               State('pwd-box', 'value')])
def update_output(n_clicks, input1, input2):
    if n_clicks > 0:
        user = User.query.filter_by(username=input1).first()
        if user:
            if check_password_hash(user.password, input2):
                return ''
            else:
                return 'Incorrect username or password'
        else:
            return 'Incorrect username or password'
    else:
        return ''


@app.callback(Output('forget-password', 'children'),
              [Input('Forget-password', 'n_clicks')])
def update_forget(n_clicks):
    if n_clicks > 0:
        return 'kindly email us at 435000118@pnu.edu.sa to get new password'
    else:
        pass

# @app.callback(Output('url_go_to_login', 'pathname'),
#               [Input('go-to-login', 'n_clicks')])
# def go_to_login(n_clicks):
#     # return '/login'
#     pass
