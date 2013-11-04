import pkg_resources
from pynavet.postaladdress import PostalAddress
from pynavet.plugins import MarshallXMLData
from unittest import TestCase
from mock import MagicMock


class TestPostalAddress(TestCase):
    def setUp(self):
        self.navet = PostalAddress('', '', '', True)
        data_dir = pkg_resources.resource_filename(__name__, 'data')
        self.data = open('%s/testdata.xml' % data_dir).read()

    def test_get_all_data_dict(self):
        self.navet.client.service.getData = MagicMock()
        self.navet.client.service.getData.return_value = self.data
        result = self.navet.get_all_data('xxxx')
        self.assertTrue(isinstance(result, dict))

    def test_get_all_data_xml(self):
        self.navet.client.service.getData = MagicMock()
        self.navet.client.service.getData.return_value = self.data
        result = self.navet.get_all_data('', as_xml=True)
        self.assertTrue(isinstance(result, str))

    def test_get_name(self):
        md = MarshallXMLData()
        self.navet.client.service.getData = MagicMock()
        context = MagicMock(reply=self.data)
        md.unmarshalled(context)
        self.navet.client.service.getData.return_value = context.reply
        result = self.navet.get_name('')
        self.assertEquals(result['Name']['GivenName'], 'John')
        try:
            result['OfficialAddress']
        except KeyError:
            pass

    def test_get__official_address(self):
        md = MarshallXMLData()
        self.navet.client.service.getData = MagicMock()
        context = MagicMock(reply=self.data)
        md.unmarshalled(context)
        self.navet.client.service.getData.return_value = context.reply
        result = self.navet.get_official_address('')
        self.assertEquals(result['OfficialAddress']['Address2'], 'Example road 10')
        try:
            result['Name']
        except KeyError:
            pass

    def test_get_name_and_official_address(self):
        md = MarshallXMLData()
        self.navet.client.service.getData = MagicMock()
        context = MagicMock(reply=self.data)
        md.unmarshalled(context)
        self.navet.client.service.getData.return_value = context.reply
        result = self.navet.get_name_and_official_address('')
        self.assertEquals(result['Name']['GivenName'], 'John')
        self.assertEquals(result['OfficialAddress']['Address2'], 'Example road 10')
