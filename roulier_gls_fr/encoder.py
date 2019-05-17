"""Transform input to gls compatible xml"""

import logging
from jinja2 import Environment, PackageLoader
from roulier.codec import Encoder
from roulier.exception import InvalidApiInput
from .api import GlsApi


GLS_ACTIONS = ('generateLabelRequest', 'getProductInter')

_logger = logging.getLogger(__name__)


class GlsEncoder(Encoder):
    """Transform input to gls compatible xml."""

    def encode(self, api_input, action):
        """Transform input to gls compatible xml."""
        if not (action in GLS_ACTIONS):
            raise InvalidApiInput(
                'action %s not in %s' % (action, ', '.join(GLS_ACTIONS)))
        api = GlsApi()
        if not api.validate(api_input):
            _logger.warning('Laposte api call exception:')
            raise InvalidApiInput(
                {'api_call_exception': api.errors(api_input)})
        data = api.normalize(api_input)

    def api(self):
        """Return API we are expecting."""
        # api = GlsApi()
        import pdb; pdb.set_trace()
        return GlsApi().api_values()


    def lookup_label_format(self, label_format="ZPL"):
        """Get a Gls compatible format of label.

        args:
            label_format: (str) ZPL or ZPL_10x15_300dpi
        return
            a value taken in GLS_LABEL_FORMAT
        """
