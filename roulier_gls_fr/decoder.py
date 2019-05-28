"""Gls XML -> Python"""

import logging

from roulier.codec import Decoder
from roulier.exception import CarrierError

log = logging.getLogger(__name__)


class GlsDecoder(Decoder):
    """Gls XML -> Python."""

    def decode(self, body):
        """Gls -> Python."""

        data = self.exotic_serialization_to_dict(body)
        self.raise_on_error(data)
        import pdb; pdb.set_trace()
        print(data)
        return data

        def get_product_inter(msg):
            """Understand a getProductInterResponse."""
            x = {
            }
            return x

        return {}

    def exotic_serialization_to_dict(self, data):
        res = {}
        for val in data.split('|')[1:-1]:
            key, value = val.split(':', 1)
            res[key] = value
            # res[key] = value.decode(WEB_SERVICE_CODING, 'ignore')
        return res

    def raise_on_error(self, data):
        errors = []
        result = data.get('RESULT')
        components = result.split(':')
        code, message = components[0], components[1]
        if code == 'E000':
            return True
        else:
            log.info("""Web service error :
code: %s ; message: %s ; result: %s""" % (code, message, result))
            if message == 'T330':
                zip_code = ''
                if data['T330']:
                    zip_code = data['T330']
                errors.append(
                    "Postal code '%s' is wrong (relative to the "
                    "destination country)" % zip_code)
            elif message == 'T100':
                cnty_code = ''
                if data['T100']:
                    cnty_code = data['T100']
                errors.append("Country code '%s' is wrong" % cnty_code)
            else:
                if code == 'E999':
                    log.info(
                        "Unibox server (web service) is not responding")
                else:
                    log.info("""
        >>> An unknown problem is happened : check network connection,
        webservice accessibility, sent datas and so on""")
                log.info("""
        >>> Rescue label will be printed instead of the standard label""")
        if len(errors) > 0:
            import pdb; pdb.set_trace()
            raise CarrierError(ResponseObject(result), errors[0])
        print("la")
        return False


class ResponseObject():
    """ Minimal response object for Roulier integration
    """
    text = None

    def __init__(self, text):
        self.text = text
