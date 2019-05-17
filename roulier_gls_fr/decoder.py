"""Gls XML -> Python"""

from lxml import objectify
from roulier.codec import Decoder


class GlsDecoder(Decoder):
    """Gls XML -> Python."""

    def decode(self, body, parts, output_format):
        """Gls XML -> Python."""
        def get_product_inter(msg):
            """Understand a getProductInterResponse."""
            x = {
            }
            return x

        return {}
