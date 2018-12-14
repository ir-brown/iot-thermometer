import thermometer
import time
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient

# Custom MQTT message callback
def customCallback(client, userdata, message):
    print("Received a new message: ")
    print(message.payload)
    print("from topic: ")
    print(message.topic)
    print("--------------\n\n")


ca = '/home/pi/aws/root-CA.crt'
cert = '/home/pi/aws/Bodie.cert.pem'
priv = '/home/pi/aws/Bodie.private.key'

client = AWSIoTMQTTClient('bodie')
client.configureEndpoint('a21yhbyv0utwbr-ats.iot.us-west-2.amazonaws.com', 8883)
client.configureCredentials(ca, priv, cert)
client.configureOfflinePublishQueueing(-1)
client.configureDrainingFrequency(2)
client.configureConnectDisconnectTimeout(10)
client.configureMQTTOperationTimeout(5)
client.connect()
time.sleep(2)

client.subscribe("topic_1", 0, customCallback)
for i in range(100):
    client.publish("topic_1", "yeet", 0)
    time.sleep(10)

client.disconnect()
