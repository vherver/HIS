from datetime import datetime

from django.db import models


class TimeStampMixin(models.Model):
    class Meta:
        abstract = True

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    deleted = models.DateTimeField(default=None, blank=True, null=True)

    @property
    def soft_delete(self) -> None:
        self.deleted = datetime.now()
        self.save(update_fields=["deleted", "modified"])


class BasicName(models.Model):
    class Meta:
        abstract = True

    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
