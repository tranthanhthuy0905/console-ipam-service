from .filters import BaseResourceIPFilter
from .models import ResourceIP


def resource_get_ipam_data(*, resource_ip: ResourceIP):
    return {
        'id': resource_ip.id,
        'vlan_id': resource_ip.vlan_id,
        'is_active': resource_ip.is_active,
        'ips': resource_ip.ips,
    }


def resource_ip_list(*, filters=None):
    filters = filters or {}

    qs = ResourceIP.objects.all()

    return BaseResourceIPFilter(filters, qs).qs
