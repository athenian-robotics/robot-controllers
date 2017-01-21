#!/usr/bin/env python2

import argparse
import json
import logging
from threading import Thread

from common_constants import LOGGING_ARGS
from common_utils import mqtt_broker_info
from constants import *
from location_client import LocationClient
from mqtt_connection import MqttConnection

if __name__ == "__main__":
    # Parse CLI args
    parser = argparse.ArgumentParser()
    parser.add_argument("-g", "--grpc", required=True, help="gRPC location server hostname")
    parser.add_argument("-m", "--mqtt", required=True, help="MQTT broker hostname")
    args = vars(parser.parse_args())

    # Setup logging
    logging.basicConfig(**LOGGING_ARGS)

    # Start location reader in thread
    locations = LocationClient(args["grpc"])
    locations.start()


    # Setup MQTT
    def on_connect(client, userdata, flags, rc):
        print("Connected with result code: {0}".format(rc))
        Thread(target=publish_locations, args=(client, userdata)).start()


    def on_disconnect(client, userdata, rc):
        print("Disconnected with result code: {0}".format(rc))


    def on_publish(client, userdata, mid):
        print("Published value to {0} with message id {1}".format(COMMAND_TOPIC, mid))


    def publish_locations(client, userdata):
        while True:
            x_loc, y_loc = locations.get_xy()

            # Encode payload into json object
            json_val = json.dumps({DIRECTION: direction, SPEED: speed})
            result, mid = mqtt_conn.client.publish(COMMAND_TOPIC, payload=json_val.encode('utf-8'))


    # Create MQTT connection
    mqtt_conn = MqttConnection(*mqtt_broker_info(args["mqtt"]))
    mqtt_conn.client.on_connect = on_connect
    mqtt_conn.client.on_disconnect = on_disconnect
    mqtt_conn.client.on_publish = on_publish
    mqtt_conn.connect()