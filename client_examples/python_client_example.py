import paho.mqtt.client as mqtt
import json
import time

def on_publish(client, userdata, mid):
    print(f"[✅] Message Published with mid: {mid}")

def send_test_message():
    # Define MQTT parameters
    MQTT_BROKER = "localhost"  # Updated to match docker-compose config
    MQTT_PORT = 1883
    MQTT_TOPIC = "test/test"
    MQTT_USERNAME = "sensor"
    MQTT_PASSWORD = "sensor"

    # Create a new MQTT client instance with a unique client ID
    client = mqtt.Client(client_id="mqtt2prometheus")

    # Set up authentication
    client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)

    # Assign the callback to the client
    client.on_publish = on_publish

    # Connect to the MQTT Broker
    client.connect(MQTT_BROKER, MQTT_PORT)

    # Prepare a sample message
    message = {"temperature": 25.3, "humidity": 60}
    payload = json.dumps(message)

    # Publish a message to the broker
    result = client.publish(MQTT_TOPIC, payload)

    # Run the MQTT client loop to process events
    client.loop_start()

    # Wait for the message to be published
    time.sleep(2)
    client.loop_stop()

    print("Test message sent.")

if __name__ == "__main__":
    send_test_message()
