import uuid

from django.contrib.postgres.fields import ArrayField
from django.db import models

from ..common.models import BaseModel


class BaseResourceIPManager(models.Manager):
    def create_ip(self, ips, vlan_id, is_active=True):
        if not ips:
            raise ValueError('IP must not be None')

        resource_ips = self.model(
            ips=ips,
            is_active=is_active,
            vlan_id=vlan_id
        )

        resource_ips.full_clean()
        resource_ips.save(using=self._db)

        return resource_ips


class ResourceIP(BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    vlan_id = models.CharField(blank=True, null=True, max_length=255)
    is_active = models.BooleanField(default=True)
    ips = ArrayField(models.CharField(max_length=255), unique=True)

    objects = BaseResourceIPManager()

    def __str__(self):
        return "[{0}] Resource has the following IP: {1}".format(self.id, self.ips)
