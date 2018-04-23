from urllib.parse import urlparse, urlunparse
from socket import gethostbyname


def print_server_info(url, method, headers=None):
    res = requests.head(url)
    print(
        'Server Software: %s' %
        res.headers.get('server', 'Unknown'))
    print('Running %s %s' % (method, url))

    if headers:
        for k, v in headers.items():
            print('\t%s: %s' % (k, v))


def resolve(url):
    parts = urlparse(url)

    if not parts.port and parts.scheme == 'https':
        port = 443
    elif not parts.port and parts.scheme == 'http':
        port = 80
    else:
        port = parts.port

    hostname = parts.hostname

    # Don't use a resolved hostname for SSL requests otherwise the
    # certificate will not match the IP address (resolved)
    if parts.scheme != 'https':
        resolved = gethostbyname(hostname)
        netloc = '%s:%d' % (resolved, port) if port else resolved
    else:
        resolved = hostname
        netloc = parts.netloc

    if port not in (443, 80):
        host += ':%d' % port
        original += ':%d' % port

    parts = (parts.scheme, netloc, parts.path or '',
             '', parts.query or '', parts.fragment or '')

    return urlunparse(parts), hostname, resolved
