import dash
from dash.dependencies import Input, Output
import dash_daq as daq
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
from dash import html
import plotly.graph_objs as go
import csv
import random

app = dash.Dash(__name__)

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])


#--------Color Scheme--------
theme = {
    'dark': True,
    'detail': '#119ED4',
    'primary': '#0037EA',
    'secondary': '#FF001B',
}

ValueColor = {
    'dark': True,
    'low': '#0031F6',
    'medium': '#FFF700',
    'high': '#EA071E',
}
#--------Color Scheme--------

#--------Graphs--------
xAxis = [1, 2, 3, 4, 5, 6, 7]
yAxis = [1, 4, 6, 3, 2, 6, 7, 2 , 5, 2 , 6,7]


fig = go.Figure(data=[go.Scatter(x=xAxis, y=yAxis)])

fig.update_layout(
    autosize=True,
    width=500,
    height=300,
    margin=dict(
        l=10,
        r=10,
        b=10,
        t=20,
        pad=3
    ),
    paper_bgcolor='#161616',
)

graph = dcc.Graph(figure=fig)

#--------Graphs--------


header_height = '6rem', '10rem'

HEADER_STYLE = {
        'position': 'fixed',
        'top': 0,
        'left': 0,
        'right': 0,
        'height': header_height,
        'width':'80%',
        'margin-left':'20%',
        'padding': '2rem 1rem',
        'background-color': '#161616',
        'color': '#7FDBFF',
        'textAlign': 'center'
    }

SIDEBAR_STYLE = {
        'position': 'fixed',
        'top': header_height,
        'left': 0,
        'bottom': 0,
        'width': '20%',
        'height':'100%',
        'padding': '1rem 1rem',
        'background-color': '#161616',
        'color': '#7FDBFF'
    }


profile = html.Center([
                html.Img(
                #--------FAN GIF--------
                src='https://animesher.com/orig/0/3/32/328/animesher.com_hakase-sad-nichijou-32839.jpg',
                style={'width':'50%', 'margin-top':'12%', 'border-radius':'15rem'}
                #--------FAN GIF--------
            ),
            html.H5("UserName"),
        ])



leddTemp = daq.LEDDisplay(
                value="3.14159",
                color='#04D55C',
                id='darktheme-daq-leddisplay-1',
                className='dark-theme-control'
                )

leddHum = daq.LEDDisplay(
                value="3.14159",
                color='#9F01FF',
                id='darktheme-daq-leddisplay-2',
                className='dark-theme-control'
                )

leddLight = daq.LEDDisplay(
                value="3.14159",
                color='#FFDB00',
                id='darktheme-daq-leddisplay-3',
                className='dark-theme-control'
                )

sideBar = html.Div([
            profile,
            html.Div(style={'margin-top':'5rem'}, children=[
                html.Center([
                    html.H5("Temperature"),
                    leddTemp,
                    html.Br(), html.Br(),
                    html.H5("Humidity"),
                    leddHum,
                    html.Br(), html.Br(),
                    html.H5("Light Intensity"),
                    leddLight
                ]),
            ])
        ],style=SIDEBAR_STYLE, )

topBar = html.Div([
    html.H2("IoT Dash App")
    ],style=HEADER_STYLE)

#---------------COMPONENTS---------------


image = html.Img(
                #--------FAN GIF--------
                src='https://akela.mendelu.cz/~xzboril7/wa-projekt-zboril/pictures/spinning-fan.gif',

                style={'width':'50%', 'margin-top':'12%'}
                #--------FAN GIF--------
            )

lightValue = 100

def light_Image():
    if lightValue >400:
        lightbulbStatus = 'https://cdn.discordapp.com/attachments/758112392637972520/967979920124968980/closedLight.png'
        return lightbulbStatus
    else:
        lightbulbStatus = 'https://cdn.discordapp.com/attachments/758112392637972520/967979920389185536/lightOpen.png'
        return lightbulbStatus

lightImage = html.Img(
                src=light_Image(),
                style={'width':'70%', 'margin-top':'2%', 'margin-left':'40%'}
            )


#value of the temperature
tempValue = 10

#function to change the color of the temperature
def temp_color():
    if tempValue <= 20:
        tempColor = ValueColor['low']
        return tempColor
    if tempValue >=21 and tempValue <= 35:
        tempColor = ValueColor['medium']
        return tempColor
    else:
        tempColor = ValueColor['high']
        return tempColor

#thermometer component
temp = daq.Thermometer(
                min=0,
                max=50,
                label='Temperature',
                value=tempValue,
                showCurrentValue=True,
                units='Celsius (c)',
                color=temp_color(),
                id='darktheme-daq-thermometer',
                className='dark-theme-control',
                style={'color':'white'}
                )

#change the button ON/OFF depending of the tempValue
def powerBtnStatus():
    if tempValue >= 35:
        buttonStatus = 'True'
        return buttonStatus
    else:
        buttonStatus = 'False'
        return buttonStatus

def powerBtnColor():
    if tempValue >= 35:
        buttonColor = 'green'
        return buttonColor
    else:
        buttonColor = 'white'
        return buttonColor

powerButton = html.Div([
                daq.PowerButton(
                label='Fan',
                disabled='True',
                on=powerBtnStatus(),
                color=powerBtnColor(),
                style={'margin-right':'50%', 'color':'white'}
                ),
                image
            ])

humValue = 40
def humidity_color():
    if humValue <= 35:
        humColor = ValueColor['low']
        return humColor
    if humValue >= 36 and humValue <= 75:
        humColor = ValueColor['medium']
        return humColor
    else:
        humColor = ValueColor['high']
        return humColor

gauge = daq.Gauge(
                min=0,
                max=100,
                value=humValue,
                label='Humidity',
                showCurrentValue=True,
                units='Percent (%)',
                color=humidity_color(),
                id='darktheme-daq-gauge',
                className='dark-theme-control',
                style={'color':'white', 'padding-top':'5px', 'margin-left':'25px'}
                )


ledd = daq.LEDDisplay(
                value="3.14159",
                color=theme['primary'],
                id='darktheme-daq-leddisplay',
                className='dark-theme-control'
                )


indicator = daq.Indicator(
                value=True,
                color='#FFDB00',
                id='darktheme-daq-indicator',
                className='dark-theme-control'
            )


def light_Color():
    if lightValue <= 400:
        lightColor = ValueColor['low']
        return lightColor
    else:
        lightColor = ValueColor['medium']
        return lightColor

graduateBar = html.Div(style={'margin-left':'10%', 'margin-top':'3%'}, children=[
                daq.GraduatedBar(
                    value=lightValue,
                    label='light Intensity',
                    color=theme['primary'],
                    vertical = "True",
                    showCurrentValue=True,
                    id='darktheme-daq-graduatedbar',
                    className='dark-theme-control',
                )
            ])



#---------------COMPONENTS---------------


#----------------CARD 1----------------

hum_card = dbc.Card(
        dbc.CardBody([
            html.Div([
                #--------GAUGE--------
                gauge
                #--------GAUGE--------
            ])
        ]), style={'background-color': '#161616', 'height':'70%', 'width':'45%',
                    'border-radius':'1rem', 'margin-left':'50%', 'margin-top':'15%'}
    )

#----------------CARD 1----------------


#----------------CARD 2----------------
temp_card =  dbc.Card(
        dbc.CardBody([
            html.Div([
                #---------Temperature/Button/Gif---------
                dbc.Row([
                    dbc.Col(temp),
                    dbc.Col(powerButton),
                ])
                #---------Temperature/Button/Gif---------
            ]),
        ]), style={'background-color': '#161616', 'height':'70%', 'width':'80%',
                    'border-radius':'1rem', 'margin-top':'15%'},
    )
#----------------CARD 2----------------


#----------------CARD 3----------------
ledd_card =  dbc.Card(
        dbc.CardBody([
            html.Div([
                dbc.Row([
                    dbc.Col(graph),
                    dbc.Col(lightImage),
                    dbc.Col(graduateBar),
                ])
            ]),
        ]), style={'background-color': '#161616', 'height':'100%', 'width':'65.5%',
                    'border-radius':'1rem', 'margin-left':'24.5%', 'margin-top':'1%'},
    )
#----------------CARD 3----------------


#-----------------ROW #1-----------------
cards = dbc.Row([
    dbc.Col(hum_card),
    dbc.Col(temp_card)
])
#-----------------ROW #1-----------------

#-----------------ROW #2-----------------
cards2 = dbc.Row([
    dbc.Col(ledd_card)
])
#-----------------ROW #2-----------------

cardDisplay = html.Div([
    sideBar,
    cards,
    cards2
])


app.layout = html.Div(style={'background-color': '#1D1D1E', 'height':'1000px', 'width':'100%', 'position':'fluid'}, children=[
    daq.DarkThemeProvider(theme=theme, children=cardDisplay), topBar
    ])

@app.callback(Output('my-gauge-1', 'value'))
def update_output(value):
    return value

if __name__ == '__main__':
    app.run_server(debug=True)