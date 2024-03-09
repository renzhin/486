from django.db.models.signals import post_save
from django.dispatch import receiver

from cpus.models import Cpu


@receiver(post_save, sender=Cpu)
def update_catalog_number(sender, instance, created, **kwargs):
    if created:
        user = instance.user
        last_cpu = sender.objects.filter(user=user).order_by(
            '-catalog_number'
        ).first()

        if last_cpu is not None and last_cpu.catalog_number:
            last_catalog_number = int(last_cpu.catalog_number)
            new_catalog_number = str(last_catalog_number + 1).zfill(4)
        else:
            new_catalog_number = '0001'

        instance.catalog_number = new_catalog_number
        instance.save()
