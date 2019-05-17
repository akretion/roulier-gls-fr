"""API implementation for GLS"""

from roulier.api import Api


class GlsApi(Api):
    def _service(self):
        schema = super(GlsApi, self)._service()
        print(schema)
        { 'agencyId': '',
          'shippingId': '',
          }
        schema['reference1'] = {'maxlength': 20}
        schema['reference2'] = {'maxlength': 20}
        schema['instructions'] = {'maxlength': 35}
        schema['shippingDate'] = {'date': '%Y%m%d', 'required': True}
        schema['is_test'] = {'type': 'boolean', 'default': False}
        schema['customerId'].update(
            {'maxlength': 10, 'minlength': 10, 'required': True})
        schema['product'].update({'required': True, 'empty': False})
        DELIVERY_MODEL = {
            # 'address': ADDRESS_MODEL,
            "consignee_ref":    {'maxlength': 20},
            "parcel_total_number": {'max': 999, 'type': int, 'required': True},
        }
        DELIVERY_MAPPING = {
            # 'address': ADDRESS_MODEL,
            'T859': "consignee_ref",
            'T854': "reference1",
            'T8907': "reference1",
            'T8908': "reference2",
            'T540': "shippingDate",
            'T8318': "instructions",
            'T8975': "gls_origin_reference",
            'T8905': "parcel_total_number",
            'T8702': "parcel_total_number",
        }
        ACCOUNT_MAPPING = {
            'T8915': "customerId",
            'T8914': "contact_id",
            'T8700': "outbound_depot",
            # shipper
            'T820': "street1",
            'T810': "name",
            'T822': "zip",
            'T823': "city",
            'T821': "country",
        }
        SENDER_MODEL = {
            "contact_id":        {'maxlength': 10},
            "outbound_depot":    {'maxlength': 6, 'minlength': 6, 'required': True},
            "name":      {'maxlength': 35, 'required': True},
            "street1":    {'maxlength': 35, 'required': True},
            "street2":   {'maxlength': 35},
            "zip":       {'maxlength': 10, 'required': True},
            "city":      {'maxlength': 35, 'required': True},
        }
        return schema

    def _address(self):
        schema = super(GlsApi, self)._address()
        ADDRESS_MODEL = {
            "consignee_name":   {'maxlength': 35, 'required': True},
            "contact":          {'maxlength': 35},
            "street":           {'maxlength': 35, 'required': True},
            "street2":          {'maxlength': 35},
            "street3":          {'maxlength': 35},
            "zip":              {'maxlength': 10, 'required': True},
            "city":             {'maxlength': 35, 'required': True},
            "consignee_phone":  {'maxlength': 20},
            "consignee_mobile": {'maxlength': 20},
            "consignee_email":  {'maxlength': 100},
            # for uniship label only
            "country_norme3166": {'max': 999, 'min': 1, 'type': int},
        }
        # Here is all fields called in mako template
        ADDRESS_MAPPING = {
            'T860': "consignee_name",
            'T8906': "contact",
            'T863': "street",
            'T861': "street2",
            'T862': "street3",
            'T330': "zip",
            'T864': "city",
            'T100': "country_code",
            'T871': "consignee_phone",
            'T1230': "consignee_mobile",
            'T1229': "consignee_email",
        }
        tmp = {
            'company': '',
            'name': '',
            'street1': '',
            'street2': '',
            'country': '',
            'city': '',
            'zip': '',
            'phone': '',
            'email': '',
            'firstName': ''
    }

        return schema

    def _from_address(self):
        schema = super(GlsApi, self)._from_address()
        return schema

    def _to_address(self):
        schema = super(GlsApi, self)._to_address()
        schema['firstName'] = {'default': ''}
        return schema

    def _parcel(self):
        schema = super(GlsApi, self)._parcel()
        PARCEL_MODEL = {
            "parcel_number_label": {'max': 999, 'type': int, 'required': True},
            "parcel_number_barcode": {'max': 999, 'type': int, 'required': True},
            # TODO validate a weight of XX.XX (5 chars)  {0:05.2f}
            "custom_sequence": {'maxlength': 10, 'minlength': 10, 'required': True},
            "weight": {'maxlength': 5, 'required': True},
        }
        PARCEL_MAPPING = {
            'T530': "weight",
            'T8973': "parcel_number_barcode",
            'T8904': "parcel_number_label",
        }
        return schema
