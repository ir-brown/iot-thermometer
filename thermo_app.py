from flask import Flask
import thermometer

app = Flask(__name__)

@app.route("/read")
def checkTemp():
    temp = thermometer.read_temp()
    return 'Temperature: ' + temp + 'F'
