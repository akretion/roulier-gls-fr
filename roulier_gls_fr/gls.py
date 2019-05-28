""" Implementation for GLS """

from .encoder import GlsEncoder
from .decoder import GlsDecoder
from .transport import GlsTransport
from roulier.carrier import Carrier


class Gls(Carrier):
    """Implementation for GLS"""

    encoder = GlsEncoder()
    decoder = GlsDecoder()
    ws = GlsTransport()

    def api(self):
        """ Expose how to communicate with GLS """
        return self.encoder.api()

    def get(self, data, action):
        """ Run an action with data against Gls WS """
        request = self.encoder.encode(data, action)
        response = self.ws.send(request)
        return self.decoder.decode(
            response['body'],
            # response['parts'],
            # request['output_format']
        )

    # shortcuts
    def get_label(self, data):
        """ Generate a label """
        return self.get(data, 'label')
