"""
This module implements "personpostXML" for the Swedish government population register service (NAVET)
"""
from pynavet.client import NavetClient
from pynavet.plugins import MarshallXMLData
from suds import WebFault
from xmltodict import parse as xmltodict
from lxml import etree
from logging import getLogger

LOG = getLogger(__name__)


class PostalAddress(NavetClient):
    """
    This class is used to retrieve postal address information for a provided national identity number
    """
    def __init__(self, cert, key_file, order_id, use_cache=True, **kwargs):
        """
        @param cert: Path to authentication client certificate in PEM format
        @type cert: str
        @param key_file: Path to key file in PEM format
        @type key_file: str
        @param order_id: Organisation number + Ordering ID ie (16XXXXXXXXXX XXXXXXXX-XXXX-XXXX)
        @type order_id: str
        @param use_cache: (Optional) Enable/Disable XSD caching in python-suds
        @type use_cache: bool
        @param verify: (optional) Whether to verify SSL endpoint certificate or not, default True
        @type verify: bool
        """
        ws_url = 'https://www2.skatteverket.se/na/na_epersondata/services/personpostXML'
        self.cert = cert
        self.key_file = key_file
        self.order_id = order_id
        NavetClient.__init__(self, wsdl='wsdl/personpostXML.wsdl', cert=(cert, key_file), url=ws_url,
                             use_cache=use_cache, **kwargs)
        # This plugin translates all XML-tags from Swedish to English
        self.load_plugin(MarshallXMLData)

    def get_all_data(self, identity_number, as_xml=False):
        """
        Get all data available for the provided national identity number from the Swedish population register.

        @param identity_number: The national identity number to lookup
        @type identity_number: str
        @param as_xml: If 'True' return the data as XML, if 'False' return data as an ordered dict (default: False)
        @type as_xml: bool
        """
        try:
            result = self.client.service.getData(self.order_id, identity_number)
            if as_xml:
                return result
            return xmltodict(result)
        except WebFault, e:
            raise e.message

    def get_official_address(self, identity_number):
        """
        Retrieve the official postal address for the provided national identity number from the Swedish population
        register.

        @param identity_number: The national identity number to lookup
        @type identity_number: str
        """
        try:
            result = self.client.service.getData(self.order_id, identity_number)
            xml = etree.fromstring(result)
            xml = xml.xpath('/NavetNotifications/PopulationItems/PopulationItem/PersonItem/PostalAddresses/OfficialAddress')
            if len(xml) <= 0:
                return False
            return xmltodict(etree.tostring(xml[0]))
        except WebFault, e:
            raise e.message

    def get_name(self, identity_number):
        """
        Retrieve the official postal address for the provided national identity number from the Swedish population
        register.

        @param identity_number: The national identity number to lookup
        @type identity_number: str
        """
        try:
            result = self.client.service.getData(self.order_id, identity_number)
            xml = etree.fromstring(result)
            xml = xml.xpath('/NavetNotifications/PopulationItems/PopulationItem/PersonItem/Name')
            if len(xml) <= 0:
                return False
            return xmltodict(etree.tostring(xml[0]))
        except WebFault, e:
            raise e.message

    def get_name_and_official_address(self, identity_number):
        """
        Retrieve the name and the official postal address for the provided national identity number from the Swedish
        population register.

        @param identity_number: The national identity number to lookup
        @type identity_number: str
        """
        try:
            result = self.client.service.getData(self.order_id, identity_number)
            xml = etree.fromstring(result)
            name = xml.xpath('/NavetNotifications/PopulationItems/PopulationItem/PersonItem/Name')
            address = xml.xpath('/NavetNotifications/PopulationItems/PopulationItem/PersonItem/PostalAddresses/OfficialAddress')
            if len(name) <= 0 or len(address) <= 0:
                return False
            result = xmltodict(etree.tostring(name[0]))
            result.update(xmltodict(etree.tostring(address[0])))
            return result
        except WebFault, e:
            raise e.message
