from .auth import IpamAuth
import requests
from ipaddress import IPv4Address, IPv4Interface

BASE_URL = 'http://localhost:8000/api/ipam/'
auth = IpamAuth('Token 23d2827a727c8d7e87e6400066ddd436a12d8547')


def build_ipam_get_request(url, params):
    r = requests.get(url=url, auth=auth, params=params)
    return r


def build_ipam_post_request(url, data):
    r = requests.request(method='POST', url=url, auth=auth, data=data)
    return r


def get_prefix(vlan_id):
    payload = {"vid": vlan_id}
    url = BASE_URL + 'prefixes'
    r = build_ipam_get_request(url, payload)
    result = r.json()
    prefix_url = result['results'][0]['url']
    return prefix_url


def get_available_ips(vlan_id, request_length):
    prefix_url = get_prefix(vlan_id)
    url = prefix_url + 'available-ips'
    r = build_ipam_get_request(url, {})
    result = r.json()
    ips = [ip['address'] for ip in result]
    return ips[:request_length]


def create_ips(vlan_id, request_length):
    ips = get_available_ips(vlan_id, request_length)
    url = BASE_URL + 'ip-addresses/'
    ips_list = [str(IPv4Interface(ip).ip) for ip in ips]
    for ip in ips_list:
        data = {'address': ip}
        print(f'DATA: {data}')
        r = build_ipam_post_request(url, data)
        print(f'RESPONSE: {r.json()}')

    return ips_list
