from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet
from rest_framework import serializers, status
from rest_framework.response import Response

from ..common.errors import ApiErrorsMixin
from ..common.pagination import get_paginated_response, LimitOffsetPagination

from .selectors import resource_ip_list
from .services import resource_ip_create, resource_ip_delete
from .models import ResourceIP


class ResourceIPViewSet(ApiErrorsMixin, ViewSet):
    class Pagination(LimitOffsetPagination):
        default_limit = 50

    class FilterSerializer(serializers.Serializer):
        id = serializers.UUIDField(required=False)
        # Important: If we use BooleanField, it will default to False
        is_active = serializers.NullBooleanField(required=False)
        vlan_id = serializers.CharField(required=False)
        ips = serializers.CharField(required=False)

    class OutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = ResourceIP
            fields = (
                'id',
                'vlan_id',
                'ips',
                'is_active',
                'created_at',
                'updated_at'
            )

    def list(self, request):
        # Make sure the filters are valid, if passed
        filters_serializer = self.FilterSerializer(data=request.query_params)
        filters_serializer.is_valid(raise_exception=True)

        resource_ip = resource_ip_list(filters=filters_serializer.validated_data)

        return get_paginated_response(
            pagination_class=self.Pagination,
            serializer_class=self.OutputSerializer,
            queryset=resource_ip,
            request=request,
            view=self
        )

    class InputSerializer(serializers.Serializer):
        vlan_id = serializers.CharField(max_length=255)
        request_length = serializers.IntegerField()

    def create(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        resource_ip_create(**serializer.validated_data)

        return Response(status=status.HTTP_201_CREATED)

    def destroy(self, request, pk=None):
        resource_ip_delete(id=pk)

        return Response(status=status.HTTP_204_NO_CONTENT)
