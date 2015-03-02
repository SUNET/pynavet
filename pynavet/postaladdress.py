"""
This module implements "personpostXML" for the Swedish government population register service (NAVET)
"""
from pynavet.client import NavetClient
from pynavet.plugins import MarshallXMLData
from suds import WebFault
from xmltodict import parse as xmltodict
from lxml import etree
from logging import getLogger
from collections import OrderedDict
import pprint

LOG = getLogger(__name__)


class PostalAddress(NavetClient):
    """
    This class is used to retrieve postal address information for a provided national identity number
    """
    def __init__(self, cert, key_file, order_id, use_cache=True, debug=False, **kwargs):
        """
        @param cert: Path to authentication client certificate in PEM format
        @type cert: str
        @param key_file: Path to key file in PEM format
        @type key_file: str
        @param order_id: Organisation number + Ordering ID ie (16XXXXXXXXXX XXXXXXXX-XXXX-XXXX)
        @type order_id: str
        @param use_cache: (Optional) Enable/Disable XSD caching in python-suds
        @type use_cache: bool
        @param debug: (Optional) Set to True to get some debug logging.
        @type debug: bool
        @param verify: (optional) Whether to verify SSL endpoint certificate or not, default True
        @type verify: bool
        """
        ws_url = 'https://www2.skatteverket.se/na/na_epersondata/services/personpostXML'
        self.cert = cert
        self.key_file = key_file
        self.order_id = order_id
        self.debug = debug
        self.logger = getLogger()
        NavetClient.__init__(self, wsdl='wsdl/personpostXML.wsdl', cert=(cert, key_file), url=ws_url,
                             use_cache=use_cache, **kwargs)
        # This plugin translates all (known) XML-tags from Swedish to English
        self.load_plugin(MarshallXMLData)

    def get_all_data(self, identity_number, as_xml=False):
        """
        Get all data available for the provided national identity number from the Swedish population register.

        @param identity_number: The national identity number to lookup
        @type identity_number: str
        @param as_xml: If 'True' return the data as XML, if 'False' return data as an ordered dict (default: False)
        @type as_xml: bool
        @return: Navet data, either as XML string or parsed (ordered) dict.
        """
        try:
            result = self.client.service.getData(self.order_id, identity_number)
            if not as_xml:
                result = xmltodict(result)
            if self.debug:
                self.logger.debug("NAVET get_all_data lookup result:\n{!r}".format(result))
            return result
        except WebFault as e:
            LOG.error(e.message)  # TODO: Add translation for exceptions
            raise
        except:
            LOG.error("Unexpected error.")
            raise

    def get_official_address(self, identity_number, data=None):
        """
        Retrieve the official postal address for the provided national identity number from the Swedish population
        register.

        @param identity_number: The national identity number to lookup
        @type identity_number: str
        @param data: Results previously fetched with get_all_data(identity_number, as_xml=False) (optional)
        @type data: OrderedDict | None
        """
        try:
            if data is None:
                data = self.get_all_data(identity_number, as_xml=False)
            try:
                person = data['NavetNotifications']['PopulationItems']['PopulationItem']['PersonItem']
                result = OrderedDict([(u'OfficialAddress', person['PostalAddresses']['OfficialAddress']),
                                      ])
            except KeyError:
                LOG.exception("NAVET address lookup failure")
                result = False
            if self.debug:
                self.logger.debug("NAVET get_official_address result:\n{!r}".format(result))
            return result
        except WebFault, e:
            raise e

    def get_name(self, identity_number, data=None):
        """
        Retrieve the official postal address for the provided national identity number from the Swedish population
        register.

        @param identity_number: The national identity number to lookup
        @type identity_number: str
        @param data: Results previously fetched with get_all_data(identity_number, as_xml=False) (optional)
        @type data: OrderedDict | None
        """
        try:
            if data is None:
                data = self.get_all_data(identity_number, as_xml=False)
            try:
                person = data['NavetNotifications']['PopulationItems']['PopulationItem']['PersonItem']
                result = OrderedDict([(u'Name', person['Name']),
                                      ])
            except KeyError:
                LOG.exception("NAVET name lookup failure")
                result = False
            if self.debug:
                self.logger.debug("NAVET get_name result:\n{!r}".format(result))
            return result
        except WebFault, e:
            raise e

    def get_name_and_official_address(self, identity_number, data=None):
        """
        Retrieve the name and the official postal address for the provided national identity number from the Swedish
        population register.

        @param identity_number: The national identity number to lookup
        @type identity_number: str
        @param data: Results previously fetched with get_all_data(identity_number, as_xml=False) (optional)
        @type data: OrderedDict | None
        """
        try:
            if data is None:
                data = self.get_all_data(identity_number, as_xml=False)
            if self.debug:
                self.logger.debug("NAVET get_name_and_official_address parsing:\n{!s}".format(pprint.pformat(data)))
            try:
                person = data['NavetNotifications']['PopulationItems']['PopulationItem']['PersonItem']
                result = OrderedDict([(u'Name', person['Name']),
                                      (u'OfficialAddress', person['PostalAddresses']['OfficialAddress']),
                                      ])
            except KeyError:
                LOG.exception("NAVET name/address lookup failure")
                result = False
            if self.debug:
                self.logger.debug("NAVET get_name_and_official_address result:\n{!s}".format(pprint.pformat(result)))
            return result
        except WebFault, e:
            raise e
