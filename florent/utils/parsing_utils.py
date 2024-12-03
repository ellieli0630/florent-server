import json
import urlparse
from collections import defaultdict

from .errors import FlorentError

def form_urlencoded_parse(body):
    """
    Parse x-www-form-url encoded data
    """
    try:
        data = urlparse.parse_qs(body)
        if not data:
            raise FlorentError("No JSON object could be decoded")
        # parse_qs wraps text in a list, so it must be unpacked
        for key in data:
            data[key] = data[key][0]
        return data
    except ValueError:
        raise FlorentError("No JSON object could be decoded.")


def smart_parse(body):
    """
    Handle json, fall back to x-www-form-urlencoded
    """
    try:
        data_dict = json.loads(body)
        if not isinstance(data_dict, dict):
            raise FlorentError('Input must be JSON dictionary')
        return data_dict
    except ValueError:
        return form_urlencoded_parse(body)


def parse_apis(apis=None):
    """
    Helper function for parsing command line api loading syntax
    """

    if apis is None:
        apis = []
    api_map = defaultdict(dict)

    for i, api in enumerate(apis):
        # extract api name and number of processes
        if '=' in api:
            api, n_procs = api.split('=')
        else:
            n_procs = 1

        # try to extract a version number, default to v1
        try:
            metadata = apis[i]
            if 'version' in metadata:
                _, version = metadata.split('=')
            else:
                version = 'v1'
        except IndexError:
            version = 'v1'

        api_map[api][version] = int(n_procs)

    return dict(api_map)
