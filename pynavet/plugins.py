"""
This module provides suds plugins.
"""
from suds.plugin import MessagePlugin
from suds.sudsobject import asdict
from logging import getLogger
from lxml import etree
from pkg_resources import resource_filename

LOG = getLogger(__name__)


class SerializablePlugin(MessagePlugin):
    """
    This class is a suds plugin that convert all suds results into serializable format.
    """
    def unmarshalled(self, context):
        if isinstance(context.reply, list) and len(context.reply) > 0:
            LOG.debug("context.reply list size %s", len(context.reply))
            reply = []
            for item in context.reply:
                reply.append(self._recursive_asdict(item))
        elif isinstance(context.reply, dict):
            reply = self._recursive_asdict(context.reply)
        else:
            reply = context.reply

        context.reply = reply

    def _recursive_asdict(self, suds_dict):
        """
        Convert Suds object into serializable format.
        """
        out = {}
        for key, val in asdict(suds_dict).iteritems():
            if hasattr(val, '__keylist__'):
                out[key] = self._recursive_asdict(val)
            elif isinstance(val, list):
                out[key] = []
                for item in val:
                    if hasattr(item, '__keylist__'):
                        out[key].append(self._recursive_asdict(item))
                    else:
                        out[key].append(item)
            else:
                out[key] = val
        return out


class MarshallXMLData(MessagePlugin):
    """
    This class marshall the received data from NAVET by removing unneeded attributes from the XML, translate remaining
    attributes to english, then converts the XML into a python dict.
    """
    def unmarshalled(self, context):
        xslt_dir = resource_filename(__name__, 'xslt')
        xslt = etree.parse('%s/addressdata.xsl' % xslt_dir)
        xml = etree.fromstring(context.reply.encode('iso-8859-1'))
        transform = etree.XSLT(xslt)
        context.reply = etree.tostring(transform(xml))
