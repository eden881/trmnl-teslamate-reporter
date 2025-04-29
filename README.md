# trmnl-teslamate-reporter

Use this to push data from a local Teslamate deployment to the TRMNL plugin via
a webhook.

## Usage

This app can be easily included in an existing Teslamate deployment by using the
`docker-compose.yml` file:

```yaml
trmnl-reporter:
  image: ghcr.io/eden881/trmnl-teslamate-reporter:latest
  environment:
    - TZ=Asia/Jerusalem
    - WEBHOOK_URL=https://usetrmnl.com/api/custom_plugins/6b29fc40-ca47-1067-b31d-00dd010662da
  volumes:
    - /etc/localtime:/etc/localtime:ro
  depends_on:
    teslamate:
      condition: service_started
    mosquitto:
      condition: service_started
```

This configuration assumes you have the MQTT feature in Teslamate enabled, named
the broker's service `mosquitto`, and named the main app `teslamate`.

Replace the `WEBHOOK_URL` with your own URL from the plugin's page on the TRMNL
dashboard.
You can also pass more settings in - see below.

## Environment Variables

To run this application, you need to set the following environment variables:

- `MQTT_BROKER`: The address of the MQTT broker (default: `mosquitto`)
- `MQTT_PORT`: The port of the MQTT broker (default: `1883`)
- `MQTT_USERNAME`: The username for MQTT authentication (if required)
- `MQTT_PASSWORD`: The password for MQTT authentication (if required)
- `WEBHOOK_URL`: The URL of the webhook to post data to
- `CAR_ID`: The ID of the car (default: `1`)
- `FETCH_FREQUENCY`: The frequency (in minutes) to fetch data (default: `15`)
