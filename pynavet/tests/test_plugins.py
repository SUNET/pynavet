from pynavet.plugins import SerializablePlugin, MarshallXMLData
from pynavet.client import NavetClient
from unittest import TestCase
from mock import MagicMock
from lxml import etree
import pkg_resources
import cPickle


class TestSerializablePlugin(TestCase):
    def test_recursive_asdict(self):
        not_serializable = NavetClient('wsdl/personpostXML.wsdl', '', '', False).client.factory.create('ns0:Struct')
        try:
            cPickle.dumps(not_serializable)
        except AttributeError:
            pass

        sp = SerializablePlugin()
        serializable = sp._recursive_asdict(not_serializable)
        self.assertTrue(cPickle.dumps(serializable))

    def test_unmarshalled(self):
        struct = NavetClient('wsdl/personpostXML.wsdl', '', '', False).client.factory.create('ns0:Struct')
        struct2 = struct
        struct['_id'] = 'Test'
        struct['_href'] = 'Test'
        struct2['_id'] = 'Test2'
        struct2['_href'] = 'Test2'
        context = MagicMock(reply=[struct, struct2])
        plugin = SerializablePlugin()
        plugin.unmarshalled(context)
        self.assertTrue(len(context.reply) == 2)
        self.assertEquals(context.reply[1]['_href'], 'Test2')
        self.assertTrue(cPickle.dumps(context.reply))


class TestMarshallXMLData(TestCase):
    def test_unmarshalled(self):
        md = MarshallXMLData()
        data_dir = pkg_resources.resource_filename(__name__, 'data')
        context = MagicMock(reply=open('%s/testdata.xml' % data_dir).read())
        md.unmarshalled(context)
        xml = etree.fromstring(context.reply)
        self.assertEquals(xml.tag, 'NavetNotifications')
