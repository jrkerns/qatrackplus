from django.db import models
from django.contrib.auth.models import User, Group
# Create your models here.


class Category(models.Model):
    """A model used for categorizing Tasks"""

    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(
        max_length=255, unique=True,
        help_text=_("Unique identifier made of lowercase characters and underscores")
    )
    description = models.TextField(
        help_text=_("Give a brief description of what type of taks should be included in this grouping")
    )

    class Meta:
        verbose_name_plural = "categories"
        ordering = ("name",)

    #----------------------------------------------------------------------
    def __unicode__(self):
        """return display representation of object"""
        return self.name


