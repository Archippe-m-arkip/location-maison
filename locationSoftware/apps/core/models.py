from django.db import models
from django.utils import timezone


class BaseModelManager(models.Manager):
    def get_queryset(self):
        # Retourne uniquement les objets non supprimés
        return super().get_queryset().filter(deleted_at__isnull=True)

    def deleted(self):
        # Retourne uniquement les objets supprimés
        return super().get_queryset().filter(deleted_at__isnull=False)


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    created_by = models.ForeignKey(
        "authuser.User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="related_%(class)s_set",
    )
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    objects = BaseModelManager()
    all_objects = models.Manager()

    class Meta:
        abstract = True

    def delete(self, using=None, keep_parents=False):
        self.deleted_at = timezone.now()
        self.save()

    @property
    def is_deleted(self):
        return self.deleted_at is not None

    @classmethod
    def get_queryset(cls):
        return cls.objects.filter(deleted_at__isnull=True)
