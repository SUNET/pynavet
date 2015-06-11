from pynavet.client import NavetClient
from pynavet.plugins import SerializablePlugin, MarshallXMLData
from pynavet.transport import CertAuthTransport
from suds.cache import ObjectCache, NoCache
from unittest import TestCase


class TestNavetClient(TestCase):
    def test_client_use_cache(self):
        navet = NavetClient('wsdl/personpostXML.wsdl', '', '', True)
        self.assertTrue(isinstance(navet.client.options.cache, ObjectCache))

    def test_client_no_cache(self):
        navet = NavetClient('wsdl/personpostXML.wsdl', '', '', None)
        self.assertTrue(isinstance(navet.client.options.cache, NoCache))

    def test_client_serializable_plugin_loaded(self):
        navet = NavetClient('wsdl/personpostXML.wsdl', '', '', None, serializable=True)
        self.assertTrue(isinstance(navet.client.options.plugins[0], SerializablePlugin))

    def test_client_cert_auth_transport(self):
        navet = NavetClient('wsdl/personpostXML.wsdl', '', '', None)
        self.assertTrue(isinstance(navet.client.options.transport, CertAuthTransport))

    def test_client_multiple_plugins(self):
        navet = NavetClient('wsdl/personpostXML.wsdl', '', '', None)
        navet.load_plugin(SerializablePlugin)
        navet.load_plugin(MarshallXMLData)
        self.assertTrue(isinstance(navet.client.options.plugins[0], SerializablePlugin))
        self.assertTrue(isinstance(navet.client.options.plugins[1], MarshallXMLData))
        self.assertEquals(len(navet.client.options.plugins), 2)

    def test_client_unload_plugins(self):
        navet = NavetClient('wsdl/personpostXML.wsdl', '', '', None, serializable=True)
        self.assertEquals(len(navet.client.options.plugins), 1)
        navet.load_plugin(MarshallXMLData)
        self.assertEquals(len(navet.client.options.plugins), 2)
        navet.unload_plugin(SerializablePlugin)
        self.assertEquals(len(navet.client.options.plugins), 1)
        self.assertTrue(isinstance(navet.client.options.plugins[0], MarshallXMLData))

    def test_client_load_plugins_alternative_way(self):
        sp = SerializablePlugin()
        md = MarshallXMLData()
        navet = NavetClient('wsdl/personpostXML.wsdl', '', '', None, plugins=[sp, md], serializable=True)
        self.assertTrue(isinstance(navet.client.options.plugins[0], SerializablePlugin))
        self.assertTrue(isinstance(navet.client.options.plugins[1], MarshallXMLData))
        self.assertEquals(len(navet.client.options.plugins), 2)
