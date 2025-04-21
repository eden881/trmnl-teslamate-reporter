import os
import logging
import schedule
import time
import requests
import paho.mqtt.subscribe as subscribe

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("trmnl-teslamate-reporter")

# Load dev environment variables is available
try:
    from dotenv import load_dotenv
    load_dotenv()  # Development mode
except ImportError:
    pass           # Production mode

# Get configuration from environment variables
FETCH_FREQUENCY = int(os.environ.get("FETCH_FREQUENCY", "15"))
MQTT_BROKER = os.environ.get("MQTT_BROKER", "mosquitto")
MQTT_PORT = int(os.environ.get("MQTT_PORT", "1883"))
MQTT_USER = os.environ.get("MQTT_USERNAME")
MQTT_PASSWORD = os.environ.get("MQTT_PASSWORD")
WEBHOOK_URL = os.environ.get("WEBHOOK_URL")
CAR_ID = int(os.environ.get("CAR_ID", "1"))

def fetch_data_mqtt():
    """Fetch data from MQTT"""
    results = {}

    # Define topics to fetch
    topics = [
        f"teslamate/cars/{CAR_ID}/state",
        f"teslamate/cars/{CAR_ID}/battery_level",
        f"teslamate/cars/{CAR_ID}/rated_battery_range_km",
        f"teslamate/cars/{CAR_ID}/version",
        f"teslamate/cars/{CAR_ID}/odometer",
        f"teslamate/cars/{CAR_ID}/display_name",
        f"teslamate/cars/{CAR_ID}/charger_power",
        f"teslamate/cars/{CAR_ID}/charger_voltage"
    ]

    try:
        # Create a minimal client connection
        auth = None
        if MQTT_USER and MQTT_PASSWORD:
            auth = {"username": MQTT_USER, "password": MQTT_PASSWORD}

        # Query each topic for the retained message
        for topic in topics:
            try:
                msg = subscribe.simple(topic, hostname=MQTT_BROKER, port=MQTT_PORT, auth=auth, keepalive=1)
                if msg and msg.payload:
                    # Try to get the topic name without the prefix
                    key = topic.split("/")[-1]
                    results[key] = msg.payload.decode().strip()
            except Exception as e:
                logger.error(f"Could not get MQTT topic {topic}: {e}")

    except Exception as e:
        logger.error(f"Error fetching data from MQTT: {e}")

    return results

def post_to_webhook(data):
    """Post data to webhook endpoint"""
    if not data:
        logger.warning("No data to send")
        return

    payload = {
        "merge_variables": data
    }

    try:
        logger.debug(f"POSTing payload: {payload}")
        response = requests.post(WEBHOOK_URL, json=payload)
        if response.status_code == 200:
            logger.info(f"Successfully posted {len(data)} records to webhook")
        else:
            logger.error(f"Webhook post failed with status {response.status_code}: {response.text}")
    except Exception as e:
        logger.error(f"Error posting to webhook: {e}")

def report_data():
    """Main function to report data from MQTT to webhook"""
    logger.info("Starting data reporter job")
    data = fetch_data_mqtt()
    if data:
        post_to_webhook(data)
        logger.info("Data reporter job completed")
    else:
        logger.warning("Data reporter job failed")

def start_scheduler():
    """Set up and start the scheduler"""
    logger.info("Starting scheduler")
    schedule.every(FETCH_FREQUENCY).minutes.do(report_data)

    # Run once immediately on startup
    report_data()

    # Keep the script running
    try:
        while True:
            schedule.run_pending()
            time.sleep(60)  # Check every minute for pending jobs
    except KeyboardInterrupt:
        logger.info("Scheduler stopped by user (CTRL+C). Exiting gracefully.")
        exit(0)

if __name__ == "__main__":
    if not WEBHOOK_URL:
        logger.critical("WEBHOOK_URL environment variable is not set. Exiting.")
        exit(1)

    logger.info("Reporter service starting up")
    start_scheduler()
