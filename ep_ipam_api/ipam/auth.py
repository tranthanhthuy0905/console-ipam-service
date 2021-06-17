

from requests.auth import AuthBase


class IpamAuth(AuthBase):
    """Attaches HTTP IPAM Authentication to the given Request object."""

    def __init__(self, token):
        # setup any auth-related data here
        self.token = token

    def __call__(self, r):
        # modify and return the request
        r.headers['Authorization'] = self.token
        return r
