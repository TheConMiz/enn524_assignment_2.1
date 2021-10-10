import paho.mqtt.client as mqtt
import time

# TODO - client both publishes and subscribes

def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT Server at IP 192.168.0.221")
    print("Connection returned result: " + str(rc))

    # Define 3 topics
    topic1 = "message/rtd"
    topic2 = "message/10kb"
    topic3 = "message/100kb"

    # Subscribe to 3 topics
    client.subscribe(topic1)
    client.subscribe(topic2)
    client.subscribe(topic3)

    # Prepare large messages.
    smallFile = open("./10kb.txt", "r")
    largeFile = open("./100kb.txt", "r")
    smallMessage = smallFile.readlines()
    largeMessage = largeFile.readlines()

    # Publish messages to those 3 topics
    client.publish(topic1, str(time.time()))
    # client.publish(topic2, str(smallMessage))
    # client.publish(topic3, str(largeMessage))


def on_message(client, userdata, msg):


    if msg.topic == "message/rtd":
        
        currentTime = time.time()
        sendTime = float(msg.payload.decode("utf-8"))

        roundTripTime = currentTime - sendTime

        print("Message Received: " + msg.topic + "\n")

        print("Sent Timestamp: " + str(sendTime) + " seconds. \n")
        print("Received Timestamp: " + str(currentTime) + " seconds. \n")
        print("Round Trip Time: " + str(roundTripTime) + " seconds. \n")

    else:
        print("Message Received: " + msg.topic + "\n" + msg.payload.decode("utf-8"))

def on_subscribe(client, userdata, mid, granted_qos):
    print(str(userdata) + " " + str(granted_qos))


def on_publish(client,userdata,result):             
    #create function for callback
    print("Data published \n")
    pass



# IP Address of personal Raspberry Pi 
host = "192.168.0.221"
# Mosquitto Broker listening on Port 1884
port = 1884
keepalive = 60

topic1 = "message/rtd"
topic2 = "message/10kb"
topic3 = "message/100kb"


client = mqtt.Client()

client.on_connect = on_connect
client.on_message = on_message
client.on_subscribe = on_subscribe
client.on_publish = on_publish

client.connect(host=host, port=port, keepalive=keepalive)
client.loop_forever()