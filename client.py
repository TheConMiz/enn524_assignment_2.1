import paho.mqtt.client as mqtt
import time

# TODO - client both publishes and subscribes

def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT Server at IP 192.168.0.221")
    print("Connection returned result: " + str(rc))

    subscribe(client=client, topic1=topic1, topic2=topic2, topic3=topic3)


def on_message(client, userdata, msg):
    # Count 10/100kb messages received. TODO: MOVE VARAIBLES ELSEWHERE. THEY KEEP GETTING RESET. 
    smallMessageCount = 0
    largeMessageCount = 0
    expectedMessageCount = 600

    if msg.topic == "message/rtd":
        # Get the current timestamp
        currentTime = time.time()
        # Get the timestamp in the message
        sendTime = float(msg.payload.decode("utf-8"))
        # Calculate the round trip time
        roundTripTime = currentTime - sendTime
        # Summarise findings
        print("Message Received: " + msg.topic + "\n")
        print("Sent Timestamp: " + str(sendTime) + " seconds. \n")
        print("Received Timestamp: " + str(currentTime) + " seconds. \n")
        print("Round Trip Time: " + str(roundTripTime) + " seconds. \n")

    elif msg.topic == "message/10kb":
        print("Topic: " + msg.topic)
        
        if msg.payload.decode("utf-8") == "done":
            packetLossRate = (expectedMessageCount - smallMessageCount) / expectedMessageCount * 100

            print(str(smallMessageCount) + " messages received with packet loss of " + str(packetLossRate) + " percent. \n")
        
        else:
            smallMessageCount += 1
            smallMessageSize = len(msg.payload)
            print("Message received. Size: " + str(smallMessageSize) + "B")

    # TODO: Finish 10kb, and copy paste. 
    # elif msg.topic == "message/100kb":
    #     print("Topic: " + msg.topic)



def on_subscribe(client, userdata, mid, granted_qos):
    print("Subscribed to " + str(mid) + ". ")


def on_publish(client,userdata,result):             
    #create function for callback
    print("Data published \n")
    pass


def publish(client, topic1, topic2, topic3):
    
    # Prepare large messages.
    smallFile = open("./10kb.txt", "r")
    largeFile = open("./100kb.txt", "r")
    smallMessage = smallFile.readlines()
    largeMessage = largeFile.readlines()

    # TODO: Define a timer of 600 seconds. 
    timeCount = 5

    while timeCount >= 0:
        time.sleep(1)
        
        # Publish messages to those 3 topics
        # Since the timestamp value changes each time it is sent, it must only be sent once. Hence, QoS = 1
        # client.publish(topic1, str(time.time()), qos=1)
        # Each of these messages must be sent at least once for the packet loss calculations, so QoS = 1
        client.publish(topic2, str(smallMessage), qos=1)

        if timeCount == 0:
            client.publish(topic2, "done", qos=1)

        client.publish(topic3, str(largeMessage), qos=1)
        
        if timeCount == 0:
            client.publish(topic3, "done", qos=1)

        # Reduce counter every second. 
        timeCount -= 1


def subscribe(client, topic1, topic2, topic3):
    # Subscribe to 3 topics
    client.subscribe(topic1)
    client.subscribe(topic2)
    client.subscribe(topic3)

# IP Address of personal Raspberry Pi 
host = "192.168.0.221"
# Mosquitto Broker listening on Port 1884
port = 1884
keepalive = 60
# Define 3 topics
topic1 = "message/rtd"
topic2 = "message/10kb"
topic3 = "message/100kb"

client = mqtt.Client()

client.on_connect = on_connect
client.on_message = on_message
client.on_subscribe = on_subscribe
client.on_publish = on_publish

client.connect(host=host, port=port, keepalive=keepalive)
client.loop_start()

publish(client=client, topic1=topic1, topic2=topic2, topic3=topic3)