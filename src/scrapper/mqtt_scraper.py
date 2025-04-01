import os
import pytz
import paho.mqtt.client as mqtt
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, inspect
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import time

def main():
    # Read environment variables
    DATABASE_URL = os.getenv("DATABASE_URL")
    MQTT_BROKER = os.getenv("MQTT_BROKER")
    MQTT_PORT = int(os.getenv("MQTT_PORT", 1883))
    MQTT_KEEP_ALIVE_INTERVAL = int(os.getenv("MQTT_KEEP_ALIVE_INTERVAL", 60))
    MQTT_USERNAME = os.getenv("MQTT_USERNAME")
    MQTT_PASSWORD = os.getenv("MQTT_PASSWORD")
    TIMEZONE = os.getenv("TIMEZONE", "UTC")

    # Database setup
    Base = declarative_base()

    class MqttMessage(Base):
        __tablename__ = 'mqtt_messages'
        id = Column(Integer, primary_key=True, autoincrement=True)
        topic = Column(String, nullable=False)
        message = Column(Text, nullable=False)
        event_time = Column(DateTime, default=datetime.utcnow)

    # Set up the database connection
    engine = create_engine(DATABASE_URL)

    # Check if the table exists, and create it if it doesn't
    inspector = inspect(engine)
    if 'mqtt_messages' not in inspector.get_table_names():
        print("Table 'mqtt_messages' does not exist. Creating it.")
        Base.metadata.create_all(engine)
    else:
        print("Table 'mqtt_messages' already exists.")

    Session = sessionmaker(bind=engine)
    session = Session()

    # Get the timezone object from pytz
    try:
        timezone = pytz.timezone(TIMEZONE)
    except pytz.UnknownTimeZoneError:
        print(f"Unknown timezone {TIMEZONE}, defaulting to UTC.")
        timezone = pytz.UTC

    # MQTT callback when connected to the broker
    def on_connect(client, userdata, flags, rc):
        print(f"Connected to MQTT Broker with result code {rc}")
        client.subscribe('#')  # Subscribe to all topics

    # MQTT callback when a message is received on a topic
    def on_message(client, userdata, msg):
        print(f"Received message on topic: {msg.topic}")

        # Convert the timestamp to the configured timezone
        utc_now = datetime.utcnow().replace(tzinfo=pytz.UTC)
        local_timestamp = utc_now.astimezone(timezone)

        # Create a new MQTTMessage object
        mqtt_message = MqttMessage(
            topic=msg.topic,
            message=msg.payload.decode('utf-8'),
            event_time=local_timestamp  # Store the timestamp in the desired timezone
        )

        # Insert message into the database
        session.add(mqtt_message)
        session.commit()

    # Create MQTT client
    client = mqtt.Client()

    # Set up MQTT authentication if username and password are provided
    if MQTT_USERNAME and MQTT_PASSWORD:
        client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)

    # Set up callback functions
    client.on_connect = on_connect
    client.on_message = on_message

    # Connect to the broker
    client.connect(MQTT_BROKER, MQTT_PORT, MQTT_KEEP_ALIVE_INTERVAL)

    # Run MQTT in a background thread
    def run_mqtt_client():
        client.loop_forever()

    # Start the MQTT client in a separate thread
    import threading
    mqtt_thread = threading.Thread(target=run_mqtt_client)
    mqtt_thread.start()

    # Keep the script running
    while True:
        time.sleep(1)

if __name__ == "__main__":
    main()
