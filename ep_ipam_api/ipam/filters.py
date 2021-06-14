from django_filters import rest_framework as filters

from .models import ResourceIP


class BaseResourceIPFilter(filters.FilterSet):
    ips = filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = ResourceIP
        fields = ('id', 'vlan_id', 'is_active', 'ips')
