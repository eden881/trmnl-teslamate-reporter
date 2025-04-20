# trmnl-teslamate-reporter

Use this to push data from a local Teslamate deployment to the TRMNL plugin via a webhook.

## Environment Variables

To run this application, you need to set the following environment variables:

- `MQTT_BROKER`: The address of the MQTT broker (default: `mosquitto`)
- `MQTT_PORT`: The port of the MQTT broker (default: `1883`)
- `MQTT_USERNAME`: The username for MQTT authentication (if required)
- `MQTT_PASSWORD`: The password for MQTT authentication (if required)
- `WEBHOOK_URL`: The URL of the webhook to post data to
- `CAR_ID`: The ID of the car (default: `1`)
- `FETCH_FREQUENCY`: The frequency (in minutes) to fetch data (default: `15`)
