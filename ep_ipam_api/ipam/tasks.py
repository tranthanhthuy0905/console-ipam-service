# from __future__ import absolute_import, unicode_literals
#
# from celery import shared_task
# from celery.utils.log import get_task_logger
# from .models import IPAddress
# from .ipam import ipam_api, get_available_ips
#
# logger = get_task_logger(__name__)
#
#
# @shared_task(bind=True, track_started=True)
# def c_get_ips(self, uid, tweet_ids):
#     api = ipam_api()
#     return