"""
Creating/ Deleting an IP address
"""

from typing import List

from .models import ResourceIP
from .ipam import create_ips, delete_ips


def resource_ip_create(
        *,
        vlan_id: str,
        is_active: bool = True,
        request_length: int
) -> ResourceIP:
    ips = create_ips(vlan_id, request_length)

    resource_ip = ResourceIP.objects.create_ip(
        ips=ips,
        vlan_id=vlan_id,
        is_active=is_active,
    )

    return resource_ip


def resource_ip_delete(
        *,
        id: int
) -> ResourceIP:
    resource_ip = ResourceIP.objects.get(id=id)

    ips = resource_ip.ips

    delete_ips(ips)

    resource_ip.delete()

    return resource_ip
