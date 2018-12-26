import thermometer
import time
import datetime
import json
import logging
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient

logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.INFO,
                    filename='/home/pi/thermometer/output.log')

# Static variables
ca = '/home/pi/aws/root-CA.crt'
cert = '/home/pi/aws/Bodie.cert.pem'
priv = '/home/pi/aws/Bodie.private.key'
topic = 'Temperature'

def initBodieClient():
    client = AWSIoTMQTTClient('bodie')
    client.configureEndpoint('a21yhbyv0utwbr-ats.iot.us-west-2.amazonaws.com', 8883)
    client.configureCredentials(ca, priv, cert)
    client.configureOfflinePublishQueueing(-1)
    client.configureDrainingFrequency(2)
    client.configureConnectDisconnectTimeout(10)
    client.configureMQTTOperationTimeout(5)
    return client

def pollThermometer():
    logging.info('Polling the thermometer...')
    data = {}
    data['Temperature'] = thermometer.read_temp()
    data['Datetime'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    json_data = json.dumps(data)
    logging.info('Temperature captured!')
    return json_data

# Initialize Raspberry Pi (Bodie) to use MQTT
logging.info('Establishing connection to AWS IoT...')
client = initBodieClient()

# Connect and wait
client.connect()
time.sleep(2)
logging.info('Successfully connected to AWS IoT!')

# Publish temperature data to AWS IoT
payload = pollThermometer()
logging.info('Publishing temperature data to AWS IoT...')
client.publish(topic, payload , 0)
time.sleep(2)
logging.info('Successfully published data!')

# Disconnect
logging.info('Disconnecting...')
client.disconnect()
