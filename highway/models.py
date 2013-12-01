from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from django.conf import settings
import boto

RECORD_TYPES = (
    ('a', 'A'),
    ('cname', 'CNAME'),
)

def get_r53_conn():
    aws_id = getattr(settings, 'AWS_ACCESS_KEY_ID')
    aws_key = getattr(settings, 'AWS_SECRET_ACCESS_KEY')
    return boto.connect_route53(aws_id, aws_key)

class Domain(models.Model):
    user = models.ForeignKey(User, null=True)
    prefix = models.CharField(max_length=64, null=True, unique=True,
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

@receiver(post_save, sender=Domain)
def create_r53_record(sender, **kwargs):
    domain = kwargs.get('instance')
    ttl = getattr(settings, 'RECORD_TTL')
    comment = 'created by highway'
    # update r53
    record = '*.{}'.format(domain.get_fqdn())
    r53 = get_r53_conn()
    zone = r53.get_zone(getattr(settings, 'R53_ZONE'))
    if domain.record_type == 'a':
        zone.add_a(record, domain.target, ttl=ttl, comment=comment)
    elif domain.record_type == 'cname':
        zone.add_cname(record, domain.target, ttl=ttl, comment=comment)

@receiver(pre_delete, sender=Domain)
def delete_r53_record(sender, **kwargs):
    domain = kwargs.get('instance')
    r53_record = '\\052.{}.'.format(domain.get_fqdn())
    r53 = get_r53_conn()
    zone = r53.get_zone(getattr(settings, 'R53_ZONE'))
    record = None
    try:
        if domain.record_type == 'a':
            record = zone.get_a(r53_record)
        else:
            record = zone.get_cname(r53_record)
        if record:
            zone.delete_record(record)
    except Exception, e:
        print(e)
        pass
