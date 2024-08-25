import base64
import json
from urllib.parse import urlparse

import cluedin
from IPython.core.magic import Magics, line_magic, magics_class


@magics_class
class CluedInMagics(Magics):

    @line_magic
    def cluedin(self, line):
        if line.startswith('get-context'):
            return self._get_context(line.split()[1])
        return self._no_op()

    def _no_op(self):
        return 'Usage: %cluedin get-context <access_token>'

    def _get_context(self, jwt):
        try:
            _, payload, _ = jwt.split('.')
            decoded_payload = base64.b64decode(
                payload + '=' * (4 - len(payload) % 4))
            jwt_json = json.loads(decoded_payload.decode('utf-8'))

            url = urlparse(jwt_json['iss'])
            context = cluedin.Context.from_dict({
                'protocol': url.scheme,
                'domain': '.'.join(url.hostname.split('.')[1:]),
                'org_name': jwt_json['ClientId'],
                'access_token': jwt
            })

            return context
        # pylint: disable=broad-except
        except Exception as e:
            print(e)
            return None
