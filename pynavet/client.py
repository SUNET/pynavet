"""
This module provides a wrapper for suds.client
"""
import os
from pynavet.transport import CertAuthTransport
from pynavet.plugins import SerializablePlugin
from suds.client import Client
from suds.cache import ObjectCache
from suds.xsd.doctor import ImportDoctor, Import


class NavetClient(object):
    """
    This class represents a wrapper for suds.client
    """
    def __init__(self, wsdl, cert, url, use_cache, **kwargs):
        """
        @param wsdl: Which bundled wsdl file to load
        @type wsdl: str
        @param cert: Path to certificate file and key file
        @type cert: tuple (cert, key)
        @param url: Service URL endpoint
        @type url: str
        @param use_cache: Enable or disable XSD caching in suds
        @type use_cache: bool
        @param verify: (optional) Whether to verify SSL endpoint certificate or not, default True
        @type verify: bool
        @param serializable: (optional) Return values will be returned in a serializable format instead of as a suds object
        @type serializable: bool
        @param plugins: (optional) List of suds plugins to load
        @type plugins: list of plugins
        """
        path = os.path.abspath(os.path.dirname(__file__))
        cache = ObjectCache(days=1) if use_cache else None

        plugins = kwargs.pop('plugins', None)
        if plugins is not None:
            self.plugins = plugins
        else:
            self.plugins = []

        serializable = kwargs.pop('serializable', False)
        transport = CertAuthTransport(cert=cert, **kwargs)
        headers = {"Content-Type": "text/xml;charset=UTF-8"}

        # Do the magic XSD dance, required since the WSDL lack explicit xsd imports
        imp = Import('http://schemas.xmlsoap.org/soap/encoding/', location='file://%s/schema/soap-encoding.xsd' % path)
        doctor = ImportDoctor(imp)

        self.client = Client('file://%s/%s' % (path, wsdl), location=url, transport=transport, headers=headers,
                             cache=cache, plugins=self.plugins, doctor=doctor)

        if serializable:
            self.load_plugin(SerializablePlugin)

    def load_plugin(self, plugin, *args):
        """
        Load suds plugin.

        @param plugin: Plugin class to load
        @type plugin: Class
        @param *args: Args passed on to the plugin on class instantiation
        """
        found = False
        plugins = self.client.options.plugins
        for p in plugins:
            if isinstance(p, plugin):
                found = True
        if not found:
            p = plugin(*args)
            plugins.append(p)
            self.client.set_options(plugins=plugins)

    def unload_plugin(self, plugin):
        """
        Unload suds plugin.

        @param plugin: Plugin class to unload
        @type plugin: Class
        """
        plugins = self.client.options.plugins
        for p in plugins:
            if isinstance(p, plugin):
                plugins.remove(p)
        self.client.set_options(plugins=plugins)
