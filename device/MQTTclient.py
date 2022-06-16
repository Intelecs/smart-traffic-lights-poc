import os,sys

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(CURRENT_DIR))


from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import secrets
import json
from dataclasses import dataclass
from typing import List
from utils.utils import get_logger

@dataclass
class MQTTclient:
    """_summary_

    Raises:
        NotImplementedError: _description_

    Returns:
        _type_: _description_
    """

    logger = get_logger(name=__name__)
    client_id: str = secrets.token_urlsafe(8)
    certificate_path: str = ""
    private_key_path: str = ""
    root_ca_path: str = ""
    port: int = 443
    web_socket: bool = False
    is_connected: bool = False
    host: str = ""
    topics: List[str] = None

    mqtt_client: AWSIoTMQTTClient = None

    def __on_message__(self, message: dict) -> None:
        self.logger.info("Message received: %s", message)

    def __on_offline__(self) -> None:
        self.is_connected = False
    
    def __on_online__(self) -> None:
        self.is_connected = True

    def __on_publish__(self, client, userdata, mid):
        self.logger.info(f"Message published - mid: {mid}, client: {client}, userdata: {userdata}")
    
    def __on_subscribe__(self, mid: str, data: dict):
        self.logger.info(f"Message published - mid: {mid}, data: {data}")

    def __connection_callback__(self, mid, data):
        self.logger.info(f"Message published - mid: {mid}, data: {data}")
    
    def __disconnect_callback__(self, mid, data):
        self.logger.info(f"Message published - mid: {mid}, data: {data}")
    
    def __publish__(self, topic: str, payload: dict, qos: int = 1) -> bool:
        try:
            self.mqtt_client.publishAsync(topic, json.dumps(payload), qos,)
            return True
        except Exception as e:
            self.logger.error("Error publishing message: %s", e)
            return False   
    def __unsubscribe__(self) -> bool:
        try:
            for topic in self.topics:
                self.mqtt_client.unsubscribeAsync(topic)
            return True
        except Exception as e:
            self.logger.error("Error unsubscribing: %s", e)
            return False
    
    def __subscribe__(self, qos: int = 0) -> None:
        try:
            for topic in self.topics:
                self.mqtt_client.subscribeAsync(topic, QoS=qos, ackCallback=self.__on_subscribe__)
            return True
        except Exception as e:
            self.logger.error("Error subscribing: %s", e)
            return False

    def __disconnect__(self):
        self.__unsubscribe__()
        self.mqtt_client.disconnect()
        
    def __setup__(self):
        if self.web_socket == True:
            raise NotImplementedError("WebSocket is not yet implemented")
        self.mqtt_client = AWSIoTMQTTClient(self.client_id)
        self.mqtt_client.configureEndpoint(self.host, self.port)
        self.mqtt_client.configureCredentials(
            CAFilePath=self.root_ca_path, KeyPath=self.private_key_path, CertificatePath=self.certificate_path
        )
        self.mqtt_client.configureAutoReconnectBackoffTime(1, 32, 20)
        self.mqtt_client.configureOfflinePublishQueueing(-1)
        self.mqtt_client.configureDrainingFrequency(2)
        self.mqtt_client.configureConnectDisconnectTimeout(10)
        self.mqtt_client.onMessage = self.__on_message__
        self.mqtt_client.connect(
            keepAliveIntervalSecond=600,
        )
        self.mqtt_client.onOffline = self.__on_offline__
        self.mqtt_client.onOnline = self.__on_online__
        self.mqtt_client.connect()
    
    
    