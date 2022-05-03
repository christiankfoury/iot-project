import dash, dash_daq as daq, RPi.GPIO as GPIO
import paho.mqtt.subscribe as subscribe, dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
from dash import dcc
from datetime import datetime
from dcMotor import *
from readSendEmail import *
from dash import html
import plotly.graph_objs as go
from phase4 import *
import threading
# Imports

# Dashboard
app = dash.Dash(__name__)
app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

# method to change the picture of the lightbulb from ON or OFF
def light_Image(lightValue, lightThreshold):
    if lightValue >= lightThreshold:
        lightbulbStatus = 'https://cdn.discordapp.com/attachments/758112392637972520/967979920124968980/closedLight.png'
        return lightbulbStatus
    else:
        lightbulbStatus = 'https://cdn.discordapp.com/attachments/758112392637972520/967979920389185536/lightOpen.png'
        return lightbulbStatus

# method to change the color of the thermometer depending on the tempValue
def temp_color(tempValue):
    if tempValue <= 20:
        tempColor = ValueColor['low']
        return tempColor
    if tempValue > 20 and tempValue <= 35:
        tempColor = ValueColor['medium']
        return tempColor
    else:
        tempColor = ValueColor['high']
        return tempColor

# method to switch the picture from a static fan image to a animated fan depending on the temperature
def fan_Image(tempValue, tempThreshold, userRespondedYes):
    if (tempValue >= tempThreshold) and userRespondedYes == True:
        fanStatus = 'https://cdn.discordapp.com/attachments/949484785661792269/969694613717803080/fan2.png'
        return fanStatus
    else:
        fanStatus = 'https://cdn.discordapp.com/attachments/949484785661792269/969694771847266334/fan.png'
        return fanStatus

# method to changet the status (ON/OFF) of the powerButton depending on temperature
def powerBtnStatus(tempValue, tempThreshold, userRespondedYes):
    if (tempValue >= tempThreshold) and userRespondedYes == True:
        buttonStatus = 'True'
        return buttonStatus
    else:
        buttonStatus = 'False'
        return buttonStatus

# method to change the color of the powerButton depenidng on the temperature
def powerBtnColor(tempValue, tempThreshold, userRespondedYes):
    if (tempValue >= tempThreshold) and userRespondedYes == True:
        buttonColor = 'green'
        return buttonColor
    else:
        buttonColor = 'white'
        return buttonColor

# method that changes the color of the Gauge depending on the humidity level
def humidity_color(humValue):
    if humValue <= 35:
        humColor = ValueColor['low']
        return humColor
    if humValue > 35 and humValue <= 75:
        humColor = ValueColor['medium']
        return humColor
    else:
        humColor = ValueColor['high']
        return humColor

# method that may or may not being used
def light_Color(lightValue, lightThreshold):
    if lightValue <= lightThreshold:
        lightColor = ValueColor['low']
        return lightColor
    else:
        lightColor = ValueColor['medium']
        return lightColor


#--------Color Scheme--------
# color scheme for the general look of the dashboard
theme = {
    'dark': True,
    'detail': '#119ED4',
    'primary': '#0037EA',
    'secondary': '#FF001B',
}

# color scheme for the inside of the components
ValueColor = {
    'dark': True,
    'low': '#0031F6',
    'medium': '#FFF700',
    'high': '#EA071E',
}
#--------Color Scheme--------

#--------Graphs--------

xAxis = []
yAxis = []

# graph is using xAxis and Yaxis to plo the points from the array
fig = go.Figure(data=[go.Scatter(x=xAxis, y=yAxis)])

# design and demensions of the graph
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

graph = dcc.Graph(figure=fig, id='graph')

#--------Graphs--------

header_height = '6rem', '10rem'

# styling for the top nav bar
HEADER_STYLE = {
    'position': 'fixed',
    'top': 0,
    'left': 0,
    'right': 0,
    'height': header_height,
    'width': '80%',
    'margin-left': '20%',
    'padding': '2rem 1rem',
    'background-color': '#161616',
    'color': '#7FDBFF',
    'textAlign': 'center'
}

# styling for the sidebar nav
SIDEBAR_STYLE = {
    'position': 'fixed',
    'top': header_height,
    'left': 0,
    'bottom': 0,
    'width': '20%',
    'height': '100%',
    'padding': '1rem 1rem',
    'background-color': '#161616',
    'color': '#7FDBFF'
}

# profile picture slot
profile = html.Center([
    html.Img(
        #--------FAN GIF--------
        src='https://animesher.com/orig/0/3/32/328/animesher.com_hakase-sad-nichijou-32839.jpg',
        style={'width': '50%', 'margin-top': '12%', 'border-radius': '15rem'},
        id='profile-image'
        #--------FAN GIF--------
    ),
    html.H5("UserName", id="username"),
])

# LEDD for displaying the users preference for temperature 
leddTemp = daq.LEDDisplay(
    value="0.00",
    color='#04D55C',
    id='darktheme-daq-leddisplay-1',
    className='dark-theme-control'
)

# LEDD for displaying the users preference for light intensity 
leddLight = daq.LEDDisplay(
    value="0.00",
    color='#FFDB00',
    id='darktheme-daq-leddisplay-3',
    className='dark-theme-control'
)

# sideBar nav codes
sideBar = html.Div([
    profile,
    html.Div(style={'margin-top': '5rem'}, children=[
        html.Center([
                    html.H5("Temperature Threshold"),
                    leddTemp,
                    html.Br(), html.Br(),
                    html.Br(), html.Br(),
                    html.H5("Light Intensity Threshold"),
                    leddLight
                    ]),
    ])
], style=SIDEBAR_STYLE, )

# topBar nav code
topBar = html.Div([
    html.H2("IoT Dash App")
], style=HEADER_STYLE)

#---------------COMPONENTS---------------

# uses light_Image() to change between the ON/OFF lightbulb image
lightImage = html.Img(
    src=light_Image(0, 0),
    id='image-light',
    style={'width': '70%', 'margin-top': '2%', 'margin-left': '40%'}
)

# uses fan_Image() to change between the ON/OFF fan image
image = html.Img(
    #--------FAN GIF--------
    src=fan_Image(0, 0, False),
    id="fan-image",
    style={'width': '50%', 'margin-top': '12%'}
    #--------FAN GIF--------
)

#thermometer component
temp = daq.Thermometer(
    # 10 is the default value
    min=0,
    max=50,
    label='Temperature',
    value=0,
    showCurrentValue=True,
    units='Celsius (c)',
    color=temp_color(0),
    id='darktheme-daq-thermometer',
    className='dark-theme-control',
    style={'color': 'white'}
)

#change the button ON/OFF depending of the tempValue
powerButton = html.Div([
    # 0 is the default value
    daq.PowerButton(
        label='Fan',
        disabled='True',
        id="powerButton",
        on=powerBtnStatus(0, 0, False),
        color=powerBtnColor(0, 0, False),
        style={'margin-right': '50%', 'color': 'white'}
    ),
    image
])

# Gauge component
gauge = daq.Gauge(
    min=0,
    max=100,
    # 0 is the default value
    value=0,
    label='Humidity',
    showCurrentValue=True,
    units='Percent (%)',
    color=humidity_color(0),
    id='darktheme-daq-gauge',
    className='dark-theme-control',
    style={'color': 'white', 'padding-top': '5px', 'margin-left': '25px'}
)

# light LEDD component to show the current value of the light
lightLEDD = html.Center([
                    daq.LEDDisplay(
                    value="0.00",
                    color='#FFDB00',
                    id='darktheme-daq-leddisplay-4',
                    className='dark-theme-control',
                    size=14
                )
            ])

# graduateBar component
graduateBar = html.Div(style={'margin-left': '10%', 'margin-top': '3%'}, children=[
    daq.GraduatedBar(
        value=0,
        max=4000,
        min=0,
        step=100,
        label='Light Intensity',
        color=theme['primary'],
        vertical="True",
        showCurrentValue=True,
        id='darktheme-daq-graduatedbar',
        className='dark-theme-control',
        style={'color': 'white'}
    ),
    lightLEDD
])

# toast message
toast = html.Div([
    dbc.Toast(
        "Light email has been sent!",
        id="toast",
        header="Email",
        is_open=False,
        dismissable=True,
        icon="success",
        # top: 66 positions the toast below the navbar
        style={"position": "fixed", "top": 66,
               "right": 10, "width": 350},
    )
])

toast2 = html.Div([
    dbc.Toast(
        "Access Denied!",
        id="toast2",
        header="New Scan from Unknown User",
        is_open=False,
        dismissable=True,
        icon="danger",
        # top: 66 positions the toast below the navbar
        style={"position": "fixed", "top": 66,
               "left": 10, "width": 350},
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
    ]), style={'background-color': '#161616', 'height': '70%', 'width': '45%',
               'border-radius': '1rem', 'margin-left': '50%', 'margin-top': '15%'}
)

#----------------CARD 1----------------


#----------------CARD 2----------------
temp_card = dbc.Card(
    dbc.CardBody([
        html.Div([
            #---------Temperature/Button/Gif---------
            dbc.Row([
                    dbc.Col(temp),
                    dbc.Col(powerButton),
                    ])
            #---------Temperature/Button/Gif---------
        ]),
    ]), style={'background-color': '#161616', 'height': '70%', 'width': '80%',
               'border-radius': '1rem', 'margin-top': '15%'},
)
#----------------CARD 2----------------


#----------------CARD 3----------------
ledd_card = dbc.Card(
    dbc.CardBody([
        html.Div([
            dbc.Row([
                    dbc.Col(graph),
                    dbc.Col(lightImage),
                    dbc.Col(graduateBar),
                    ])
        ]),
    ]), style={'background-color': '#161616', 'height': '100%', 'width': '65.5%',
               'border-radius': '1rem', 'margin-left': '24.5%', 'margin-top': '1%'},
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

# the interval in miliseconds
interval = dcc.Interval(
    id='interval-component',
    interval=3*1000,  # in milliseconds
    n_intervals=0,
)


app.layout = html.Div(style={'background-color': '#1D1D1E', 'height': '1000px', 'width': '100%', 'position': 'fixed'}, children=[
    daq.DarkThemeProvider(
        theme=theme, children=cardDisplay), topBar, toast, interval, toast2
])

# Initialize some global variables
global isLightEmailSent, isTemperatureEmailSent, userRespondedYes
userLoggedIn = isLightEmailSent = isTemperatureEmailSent = userRespondedYes = False
LED_PIN = 21
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)
GPIO.output(LED_PIN, GPIO.LOW)


rfidPayload = ""
def getRfid():
    global rfidPayload
    while True:
        rfidPayload = subscribe.simple("IoTlab/rfid")
        rfidPayload = rfidPayload.payload.decode("utf-8")

first_thread = threading.Thread(target=getRfid)
first_thread.start()
user = getDefaultUser()
oldUser = ""
lightThreshold = user['light']
temperatureThreshold = user['temperature']
profileImage = user['profile']

xAxis = []
yAxis = []

# Callback called at every m_interval change.
@app.callback(Output('darktheme-daq-thermometer', 'value'), Output('darktheme-daq-gauge', 'value'),
              Output('darktheme-daq-graduatedbar', 'value'), Output('image-light', 'src'),Output('toast', 'is_open'),
              Output('darktheme-daq-thermometer', 'color'), Output('darktheme-daq-gauge', 'color'),
              Output('fan-image', 'src'), Output('powerButton', 'on'), Output('powerButton', 'color'),
              Output('graph', 'figure'), Output('darktheme-daq-leddisplay-1', 'value'), Output('darktheme-daq-leddisplay-3', 'value'),
              Output('darktheme-daq-leddisplay-4', 'value'), Output('username', 'children'), Output('toast2', 'is_open'),
              Output('profile-image', 'src'),
              Input('interval-component', 'n_intervals'), Input('toast', 'is_open'), Input('toast2', 'is_open'))
def update_output(value, value2, value3):
    print("Running Callback")
    # Global variables
    global isLightEmailSent, isOpen, isTemperatureEmailSent, userRespondedYes, user, oldUser, isOpen2
    global lightThreshold, temperatureThreshold, rfidPayload, profileImage
    isOpen = value2
    isOpen2 = value3

    # Should create its own method for temp, hum, and light
    # Subscribe MQTT variables
    lightMessage = subscribe.simple("IoTlab/light", msg_count=1, keepalive=1)
    temperatureMessage = subscribe.simple("IoTlab/temperature",msg_count=1, keepalive=1)
    humidityMessage = subscribe.simple("IoTlab/humidity",msg_count=1, keepalive=1)
    # rfidMessage = subscribe.simple("IoTlab/rfid",msg_count=1, keepalive=1)
    #print("%s %s" % (msg.topic, msg.payload))

    print("RFID Tag: " + rfidPayload)

    if (rfidPayload != ""):
        print("RFID Tag: " + rfidPayload)
        getUser = verifyUser(rfidPayload)
        if getUser != False:
            isOpen2 = False
            if oldUser == "":
                user = getUser
                oldUser = getUser
                lightThreshold = getUser['light']
                temperatureThreshold = getUser['temperature']
                profileImage = str(getUser['profile'])
            else:
                if oldUser != getUser:
                    oldUser = getUser
                    user = getUser
                    lightThreshold = getUser['light']
                    temperatureThreshold = getUser['temperature']
                    profileImage = str(getUser['profile'])
                    isOpen = False
                    isLightEmailSent = False
                    if userRespondedYes == True:
                        stopMotor()
                        isTemperatureEmailSent = False
                        userRespondedYes = False
        else:
            print("Invalid RFID Tag")
            isOpen2 = True
        rfidPayload = ""

    # Decoding the message
    # Light payload
    lightPayload = lightMessage.payload.decode("utf-8")
    print("LIGHT " + lightPayload)
    lightNumber = int(lightPayload)
    # Temperature Payload
    temperaturePayload = temperatureMessage.payload.decode("utf-8")
    print("temp " + temperaturePayload)
    temperatureNumber = float(temperaturePayload)
    # Humidity Payload
    humidityPayload = humidityMessage.payload.decode("utf-8")
    humidityNumber = float(humidityPayload)
    print("hum " + humidityPayload)

    if user['name'] != "Default":
        # Light Intensity --> Should create its own method
        if lightNumber <= lightThreshold:
            if isLightEmailSent == False:
                value2 = "sent"
                print('sent!!!!!!')
                sendEmailLight()
                isLightEmailSent = True
                isOpen = True
            GPIO.output(LED_PIN, GPIO.HIGH)
            print("sent email" + lightPayload)
        else:
            GPIO.output(LED_PIN, GPIO.LOW)
            isLightEmailSent = False
            isOpen = False

        # TESTING WITH LIGHT SINCE TEMP IS SLOW TO CHANGE. DONT FORGET TO FLIP < >
        # For temperature --> should create its own method
        if temperatureNumber >= temperatureThreshold:
            if isTemperatureEmailSent == False:
                sendEmailTemperature(temperatureNumber)
                isTemperatureEmailSent = True
            else:
                if userRespondedYes == True:
                    print("Continue")
                elif readEmail() == True:
                    userRespondedYes = True
                    runMotor()
        else:
            if userRespondedYes == True:
                stopMotor()
                isTemperatureEmailSent = False
                userRespondedYes = False

    # Graph
    xAxis.append(len(xAxis))
    yAxis.append(lightNumber)
    fig = go.Figure(data=[go.Scatter(x=xAxis, y=yAxis)])
    fig.update_layout(
    autosize=True,
    width=500,
    height=300,
    font_color='white',
    title=dict(
        text = 'Light Intensity'
        ),
    margin=dict(
        l=10,
        r=10,
        b=10,
        t=25,
        pad=0,
    ),
    paper_bgcolor='#161616',
)


    print(str(int(temperatureNumber)) + " " + str(int(humidityNumber)) + " " + str(int(lightNumber)))
    #return random.randint(0,50), random.randint(0,100), random.randint(0,3000), "red", "blue"
    return (temperatureNumber, humidityNumber, lightNumber,
    light_Image(lightNumber, lightThreshold), isOpen, temp_color(temperatureNumber), humidity_color(humidityNumber),
    fan_Image(lightNumber, lightThreshold, userRespondedYes), powerBtnStatus(temperatureNumber, temperatureThreshold, userRespondedYes),
    powerBtnColor(temperatureNumber, temperatureThreshold, userRespondedYes), fig, str(temperatureThreshold),
    str(lightThreshold), lightNumber, user['name'], isOpen2, profileImage)


if __name__ == '__main__':
    app.run_server(debug=True)