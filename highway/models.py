from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

RECORD_TYPES = (
    ('a', 'A'),
    ('cname', 'CNAME'),
)
class Domain(models.Model):
    user = models.ForeignKey(User, null=True)
    prefix = models.CharField(max_length=64, null=True,
            help_text="Your custom part of the domain (i.e. demo)")
    target = models.CharField(max_length=64, null=True,
            help_text="Your IP or Hostname (i.e. 50.1.2.3 -- attempts to auto-detect your IP)")
    record_type = models.CharField(max_length=10, choices=RECORD_TYPES,
            null=True)
    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    source = models.CharField(max_length=20, blank=True, null=True)

    def __unicode__(self):
        return self.prefix

    def get_fqdn(self):
        return '{}.{}'.format(self.prefix, getattr(settings, 'BASE_DOMAIN'))
