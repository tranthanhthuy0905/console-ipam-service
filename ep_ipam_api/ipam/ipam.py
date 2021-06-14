from .auth import IpamAuth
import requests
from ipaddress import IPv4Interface

BASE_URL = 'http://localhost:8000/api/ipam/'
auth = IpamAuth('Token 23d2827a727c8d7e87e6400066ddd436a12d8547')


def build_ipam_request(method, url, params=None, data=None):
    if data is None:
        data = {}
    if params is None:
        params = {}
    r = requests.request(method=method, url=url, auth=auth, params=params, data=data)
    return r


# def build_ipam_get_request(url, params):
#     r = requests.get(url=url, auth=auth, params=params)
#     return r
#
#
# def build_ipam_post_request(url, data):
#     r = requests.request(method='POST', url=url, auth=auth, data=data)
#     return r


def get_prefix(vlan_id):
    payload = {"vid": vlan_id}
    url = BASE_URL + 'prefixes'
    r = build_ipam_request(method='GET', url=url, params=payload)
    result = r.json()
    prefix_url = result['results'][0]['url']
    return prefix_url


def get_available_ips(vlan_id, request_length):
    prefix_url = get_prefix(vlan_id)
    url = prefix_url + 'available-ips'
    r = build_ipam_request(method='GET', url=url)
    result = r.json()
    ips = [ip['address'] for ip in result]
    return ips[:request_length]


def create_ips(vlan_id, request_length):
    ips = get_available_ips(vlan_id, request_length)
    url = BASE_URL + 'ip-addresses/'
    ips_list = [str(IPv4Interface(ip).ip) for ip in ips]
    for ip in ips_list:
        data = {'address': ip}
        r = build_ipam_request(method='POST', url=url, data=data)

    return ips_list


def get_ip_id(ip):
    url = BASE_URL + 'ip-addresses/'
    params = {'address': ip}
    r = build_ipam_request(method='GET', url=url, params=params)
    result = r.json()['results']
    if result:
        return result[0]['id']
    return result


def delete_ips(ips):
    for ip in ips:
        address_id = get_ip_id(ip)
        url = BASE_URL + f'ip-addresses/{address_id}/'
        r = build_ipam_request(method='DELETE', url=url)
