"""
This module implements "personpostXML" for the Swedish government population register service (NAVET)
"""
from pynavet.client import NavetClient
from pynavet.plugins import MarshallXMLData
from suds import WebFault
from xmltodict import parse as xmltodict
from logging import getLogger
from collections import OrderedDict
import pprint


class PostalAddress(NavetClient):
    """
    This class is used to retrieve postal address information for a provided national identity number
    """

    # ws_url = 'https://www2.skatteverket.se/na/na_epersondata/V2/personpostXML'                        # Production
    ws_url = 'https://ppx4.skatteverket.se/na/na_epersondata_demo/V2/namnsokningXML'  # Demo

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
        self.cert = cert
        self.key_file = key_file
        self.order_id = order_id
        self.debug = debug
        self.logger = getLogger(__name__)
        NavetClient.__init__(self, wsdl='wsdl/personpostXML.wsdl', cert=(cert, key_file), url=self.ws_url,
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
            self.logger.error(e.message)  # TODO: Add translation for exceptions
            raise
        except:
            self.logger.error("Unexpected error.")
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
            person = self._get_person(identity_number, data)
            result = OrderedDict([(u'OfficialAddress', person['PostalAddresses']['OfficialAddress']),
                                  ])
        except KeyError:
            self.logger.exception("NAVET address lookup failure")
            result = False
        if self.debug:
            self.logger.debug("NAVET get_official_address result:\n{!r}".format(result))
        return result

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
            person = self._get_person(identity_number, data)
            result = OrderedDict([(u'Name', person['Name']),
                                  ])
        except KeyError:
            self.logger.exception("NAVET get_name lookup failure")
            result = False
        if self.debug:
            self.logger.debug("NAVET get_name result:\n{!r}".format(result))
        return result

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
            person = self._get_person(identity_number, data)
            result = OrderedDict([(u'Name', person['Name']),
                                  (u'OfficialAddress', person['PostalAddresses']['OfficialAddress']),
                                  ])
        except KeyError:
            self.logger.exception("NAVET get_name_and_official_address lookup failure")
            result = False
        if self.debug:
            self.logger.debug("NAVET get_name_and_official_address result:\n{!s}".format(pprint.pformat(result)))
        return result

    def get_relations(self, identity_number, data=None):
        """
        Retrieve the relations information for the provided national identity number from the Swedish population
        register.

        @param identity_number: The national identity number to lookup
        @type identity_number: str
        @param data: Results previously fetched with get_all_data(identity_number, as_xml=False) (optional)
        @type data: OrderedDict | None
        """
        try:
            person = self._get_person(identity_number, data)
            result = OrderedDict([(u'Relations', person['Relations']),
                                  ])
        except KeyError:
            self.logger.exception("NAVET get_relations lookup failure")
            result = False
        if self.debug:
            self.logger.debug("NAVET get_relations result:\n{!r}".format(result))
        return result

    def _get_person(self, identity_number, data=None):
        """
        Get the 'PersonItem' object for a national identity number.

        @param identity_number: The national identity number to lookup
        @type identity_number: str
        @param data: Results previously fetched with get_all_data(identity_number, as_xml=False) (optional)
        @type data: OrderedDict | None
        @return: Person data
        @rtype: OrderedDict
        """
        # Only enable this excessive logging when really needed.
        #if self.debug:
        #    self.logger.debug("NAVET get_name_and_official_address parsing:\n{!s}".format(pprint.pformat(data)))
        try:
            if data is None:
                data = self.get_all_data(identity_number, as_xml=False)
            person = data['S:Envelope']['S:Body']['ns2:PersonpostResponse']['PopulationItems']['PopulationItem']['PersonItem']
            return person
        except WebFault as e:
            raise e
