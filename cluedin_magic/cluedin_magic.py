# pylint: disable=missing-module-docstring missing-class-docstring missing-function-docstring
import base64
import itertools
import json
from urllib.parse import urlparse

import cluedin
import pandas as pd
from IPython.core.magic import Magics, line_magic, magics_class


@magics_class
class CluedInMagics(Magics):

    @line_magic
    def cluedin(self, line):
        command, _, args = line.partition(' ')
        command_handlers = {
            'get-context': self._handle_get_context,
            'search': self._handle_search,
        }

        if command in command_handlers:
            return command_handlers[command](args.strip())

        base_help = f'Available commands: {", ".join(command_handlers.keys())}\n' + \
            'Usage:\n' + \
            '%cluedin get-context --jwt <jwt>\n' + \
            '%cluedin search --context <context> --query <query> [--limit <limit>]'

        if not command or command == '--help':
            print(base_help)
            return

        print(f'Unknown command: "{command}".\n{base_help}')

    def _handle_get_context(self, line):
        params = self.parse_params(line)

        if 'jwt' not in params:
            print(
                'Missing required parameter: --jwt.\n' +
                'Usage: %cluedin get-context --jwt <jwt>.')
            return None

        try:
            return self._get_context(params['jwt'])
        # pylint: disable=broad-except
        except Exception as e:
            print(e)
            return

    def _get_context(self, jwt):
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

    def _handle_search(self, args):
        params = self.parse_params(args)

        if 'context' not in params:
            print(
                'Missing required parameter: --context.\n' +
                'Usage: %cluedin search --context <context> --query <query> [--limit <limit>].')
            return None

        if 'query' not in params:
            print(
                'Missing required parameter: --query.\n' +
                'Usage: %cluedin search --context <context> --query <query> [--limit <limit>].')
            return None

        ctx = self.shell.user_ns[params['context']]

        if 'limit' not in params:
            return pd.DataFrame(cluedin.gql.search(ctx, params['query']))
        return pd.DataFrame(
            itertools.islice(
                cluedin.gql.search(ctx,
                                   params['query'],
                                   min(int(params['limit']), 10_000)),
                int(params['limit'])))

    @staticmethod
    def parse_params(params):
        parsed_params = {}
        tokens = params.split('--')[1:]

        for token in tokens:
            key_value = token.split(None, 1)
            key = key_value[0]
            value = key_value[1] if len(key_value) > 1 else ''
            parsed_params[key] = value.strip()

        return parsed_params
