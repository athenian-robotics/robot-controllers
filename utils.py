import platform
import sys

TOPIC = "topic"

FORMAT_DEFAULT = "%(asctime)s %(name)-10s %(funcName)-10s():%(lineno)i: %(levelname)-6s %(message)s"


def mqtt_broker_info(val):
    return (val[:val.index(":")], int(val[val.index(":") + 1:])) if ":" in val else (val, 1883)


def is_raspi():
    return platform.system() == "Linux"


def is_python3():
    return sys.version_info[0] >= 3