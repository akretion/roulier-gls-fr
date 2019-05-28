""" Implementation for GLS """

import logging
from string import Template
from roulier.carrier import Carrier
from .encoder import GlsEncoder
from .decoder import GlsDecoder
from .transport import GlsTransport

ZPL_FILE_PATH = "roulier-gls-fr/roulier_gls_fr/templates/zpl.zpl"

log = logging.getLogger(__name__)


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
        if not action:
            action = 'label'
        request = self.encoder.encode(data, action)
        response = self.ws.send(request)
        data = self.decoder.decode(response['body'])
        if action == 'label':
            with open(ZPL_FILE_PATH, 'r') as f:
                zpl = f.read()
                unmatch_keys = self.validate_template(zpl, data.keys())
                key_with_empty_vals = {x: '' for x in unmatch_keys}
                print(data)
                data.update(key_with_empty_vals)
                t = Template(zpl)
                res = t.substitute(data)
                import pdb; pdb.set_trace()
                print(data)

    # shortcuts
    def get_label(self, data):
        """ Generate a label """
        return self.get(data, 'label')

    def validate_template(self, template_string, available_keys):
        import re
        keys2match = []
        for match in re.findall(r'\$(T[0-9].*) ', template_string):
            keys2match.append(match)
        print(keys2match)
        # import pdb; pdb.set_trace()
        unmatch = list(set(keys2match) - set(available_keys))
        not_in_tmpl_but_known_case = ['T8900', 'T8901', 'T8717', 'T8911']
        unknown_unmatch = list(unmatch)
        for elm in not_in_tmpl_but_known_case:
            if elm in unknown_unmatch:
                unknown_unmatch.remove(elm)
        if len(unknown_unmatch) > 0:
            log.info("GLS carrier : these keys \n%s\nare defined "
                     "in template but without valid replacement "
                     "values\n" % unknown_unmatch)
        return unmatch
