from django.db import models
from django.contrib.auth.models import User, Group
from django.utils.translation import ugettext as _
from django.core.validators import MinLengthValidator
# Create your models here.


class Category(models.Model):
    """A model used for categorizing Tasks"""

    name = models.CharField(verbose_name=_("Name"), max_length=255, unique=True)
    slug = models.SlugField(
        verbose_name=_("Slug"), max_length=255, unique=True,
        help_text=_("Unique identifier made of lowercase characters and underscores")
    )
    description = models.TextField(verbose_name=_("Description"),
        help_text=_("Give a brief description of what type of taks should be included in this grouping")
    )

    class Meta:
        verbose_name_plural = "categories"
        ordering = ("name",)

    #----------------------------------------------------------------------
    def __unicode__(self):
        """return display representation of object"""
        return self.name


class Task(models.Model):
    NOT_DONE = "not_done"
    DONE = "done"
    REVIEWED = "reviewed"

    status_choices = (
        (NOT_DONE, _("Not done")),
        (DONE, _("Done")),
        (REVIEWED, _("Reviewed")),
    )

    name = models.CharField(verbose_name=_("Name"), max_length=100)
    description = models.TextField(verbose_name=_("Description"), validators=[MinLengthValidator(100)],
                                   help_text=_("Describe the meaning of the task and what should be done"))
    due_date = models.DateField(verbose_name=_("Due date"), help_text=_("Set due date"))
    overdue_date = models.DateField(verbose_name=_("Overdue date"), help_text=_("Set overdue date"))
    comment_for_reviewer = models.TextField(verbose_name=_("Comment for reviewer"),
                                            help_text=_("Give a comment for the reviewer, describe what is done"),
                                            null=True, blank=True)
    edit_users = models.ManyToManyField(User, verbose_name=_("Users edit"), help_text=_("Users who can edit this task"),
                                        null=True, blank=True, related_name="users edit")
    edit_status_groups = models.ManyToManyField(Group, verbose_name=_("Groups edit"),
                                                help_text=_("Groups who can edit this task"),
                                                null=True, blank=True, related_name="groups edit")
    perform_users = models.ManyToManyField(User, verbose_name=_("User performs"),
                                           help_text=_("Users who can perform this task"),
                                           null=True, blank=True, related_name="users perform")
    perform_groups = models.ManyToManyField(Group, verbose_name=_("Groups peform"),
                                            help_text=_("Groups who can perform this task"),
                                            null=True, blank=True, related_name="groups perform")
    date_modified = models.DateTimeField(verbose_name=_("Date modified"), auto_now=True, editable=False)
    status = models.CharField(verbose_name=_("Status"), max_length=15, choices=status_choices)

    class Meta:
        ordering = ("date_modified",)
