#!/usr/bin/env python3
import dash, dash_daq as daq, dash_html_components as html, RPi.GPIO as GPIO
import paho.mqtt.subscribe as subscribe, dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
from dash import dcc
from datetime import datetime
from dcMotor import *
from readSendEmail import *
from tinydb import TinyDB, Query
from phase4 import createTable, verifyUser, sendUserEmail

# Cleaning up the GPIO pins
GPIO.cleanup()

# Initialize some global variables
global isLightEmailSent, isTemperatureEmailSent, userRespondedYes
isLightEmailSent = isTemperatureEmailSent = userRespondedYes = False
LED_PIN = 21
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)


#app = dash.Dash(__name__)
# Dashboard
app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
app.layout = html.Center([
    html.H1("Welcome to your dashboard!"),
    html.Div([
        html.Div(daq.Gauge(
            id='my-gauge',
            label="Temperature",
            value=50,
            max=50,
            min=0,
            color={"gradient":True,"ranges":{"green":[0,30],"yellow":[30,40],"red":[40,50]}},
            showCurrentValue=True,
        ), style={'margin':'5px','display':'inline-block'}),
        html.Div(daq.GraduatedBar(
            id='my-bar',
            color={"gradient":True,"ranges":{"green":[0,33],"yellow":[34,66],"red":[67,100]}},
            showCurrentValue=True,
            label="Humidity",
            value=5,
            min = 0,
            max = 100,
            step=5
        ), style={'margin':'5px','display':'inline-block'}),
        html.Div(daq.GraduatedBar(
            id="light-bar",
            max=4000,
            label="Light Intensity: 3000",
            value=3000,
            min = 0,
            step=100,
            color="yellow",
        ), style={'margin':'5px','display':'inline-block'}),
        html.Div(dash.html.Img(
            id='image-light',
            src='https://media.istockphoto.com/photos/digital-illustration-of-electric-bulb-picture-id519960558?b=1&k=20&m=519960558&s=170667a&w=0&h=o_3Jzd17NT2p4yWif5lqDsGB96uhpvSm1vnBcP8kwhY=',
            height=200,
            width=200,
            style={'border-radius':'100px'}
        ), style={'margin':'5px','display':'inline-block'}),
        dbc.Toast(
            "Email has been sent",
            id="toast",
            header="Email",
            is_open=False,
            dismissable=True,
            icon="success",
            # top: 66 positions the toast below the navbar
            style={"position": "fixed", "top": 66, "right": 10, "width": 350},
        ),
        dcc.Interval(
            id='interval-component',
            interval=10*1000, # in milliseconds
            n_intervals=0,
        )
    ])
])

# Callback called at every m_interval change.
@app.callback(Output('my-gauge', 'value'), Output('my-bar', 'value'), Output('light-bar', 'value'), Output('light-bar', 'label'),
    #Output('light-status', 'label'), Output('light-status', 'color'),
    Output('image-light', 'src'), Output('toast', 'is_open'),
    Input('interval-component', 'n_intervals'), Input('toast', 'is_open'))
def update_output(value, value2):
    print("Running Callback")
    # Global variables
    global isLightEmailSent, isOpen, isTemperatureEmailSent, userRespondedYes
    isOpen = value2

    # Should create its own method for temp, hum, and light
    # Subscribe MQTT variables
    lightMessage = subscribe.simple("IoTlab/light", msg_count=1, keepalive=1)
    temperatureMessage = subscribe.simple("IoTlab/temperature",msg_count=1, keepalive=1)
    humidityMessage = subscribe.simple("IoTlab/humidity",msg_count=1, keepalive=1)
    rfidMessage = subscribe.simple("IoTlab/rfid",msg_count=1, keepalive=1);
    #print("%s %s" % (msg.topic, msg.payload))

    while(run_once < 1):
        createTable()
        run_once = 1

    rfidPayload = rfidMessage.payload.decode()
    print("RFID Tag: " + rfidPayload)

    if rfidPayload:
        verifyUser(rfidPayload)


    # Decoding the message
    lightPayload = lightMessage.payload.decode("utf-8")
    print("LIGHT " + lightPayload)
    lightNumber = int(lightPayload)

    temperaturePayload = temperatureMessage.payload.decode("utf-8")
    print("temp " + temperaturePayload)
    temperatureNumber = float(temperaturePayload)

    humidityPayload = humidityMessage.payload.decode("utf-8")
    humidityNumber = float(humidityPayload)
    print("hum " + humidityPayload)

    # Light Intensity --> Should create its own method
    if lightNumber < 4000:
        if isLightEmailSent == False:
            value2 = "sent"
            print('sent!!!!!!')
            sendEmailLight()
            isLightEmailSent = True
            isOpen = True
        GPIO.output(LED_PIN, GPIO.HIGH)
        print("sent email" + lightPayload)
        lightStatusLabel = 'Light: ON'
        lightStatusColor = 'green'
        lightLink = 'https://static.scientificamerican.com/sciam/cache/file/2B38DE31-C1D3-4339-8808D61972976EE4.jpg'
    else:
        GPIO.output(LED_PIN, GPIO.LOW)
        lightStatusLabel = 'Light: OFF'
        lightStatusColor = 'red'
        isLightEmailSent = False
        lightLink = 'https://media.istockphoto.com/photos/digital-illustration-of-electric-bulb-picture-id519960558?b=1&k=20&m=519960558&s=170667a&w=0&h=o_3Jzd17NT2p4yWif5lqDsGB96uhpvSm1vnBcP8kwhY='
        isOpen = False

    # TESTING WITH LIGHT SINCE TEMP IS SLOW TO CHANGE. DONT FORGET TO FLIP < >
    # For temperature --> should create its own method
    if lightNumber < 4000:
        if isTemperatureEmailSent == False:
            sendEmailTemperature(lightNumber)
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


    print(str(int(temperatureNumber)) + " " + str(int(humidityNumber)) + " " + str(int(lightNumber))
        + " " + lightStatusLabel + " " + lightStatusColor)
    #return random.randint(0,50), random.randint(0,100), random.randint(0,3000), "red", "blue"
    #return temperatureNumber, humidityNumber, lightNumber, 'Light Intensity: ' + str(lightNumber), lightStatusLabel, lightStatusColor
    return temperatureNumber, humidityNumber, lightNumber, 'Light Intensity: ' + str(lightNumber), lightLink, isOpen

if __name__ == '__main__':
    app.run_server(debug=True)