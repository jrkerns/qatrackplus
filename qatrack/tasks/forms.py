from django import forms
from django.utils.translation import ugettext as _

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Field

from qatrack.tasks.models import Task


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task

    def __init__(self, *args, **kwargs):
        super(TaskForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'task-form'
        self.helper.form_method = 'post'
        self.helper.form_action = '.'
        self.helper.form_class = 'form-horizontal'

        self.helper.layout = Layout(
            Field('name', css_class='span6'),
            Field('category'),
            Field('description', rows="3", css_class='input-xlarge span6'),
            Field('unit'),
            Field('due_date'),
            Field('overdue_date'),
            Field('comment_for_reviewer', rows="3", css_class='input-xlarge span6'),
            Field('edit_users'),
            Field('edit_groups'),
            Field('perform_users'),
            Field('perform_groups'),
            Field('status'),
        )

        self.helper.add_input(Submit('submit', 'Submit task'))
        self.remove_holddown()

    def clean(self):
        """do some custom form validation"""
        cleaned_data = super(TaskForm, self).clean()

        edit_users = cleaned_data.get("edit_users")
        edit_groups = cleaned_data.get("edit_groups")
        perform_users = cleaned_data.get("perform_users")
        perform_groups = cleaned_data.get("perform_groups")

        if not edit_users and not edit_groups:
            self._errors["edit_users"] = self.error_class(["Specify at least one user or group who can edit this task"])
            self._errors["edit_groups"] = self.error_class(["Specify at least one user or group who can edit this task"])
        if not perform_users and not perform_groups:
            self._errors["perform_users"] = self.error_class(["Specify at least one user or group who can perform this task"])
            self._errors["perform_groups"] = self.error_class(["Specify at least one user or group who can perform this task"])
        return cleaned_data

    def remove_holddown(self):
        """This removes the unhelpful "Hold down the...." help texts for the
        specified fields for a form."""
        remove_message = unicode(_('Hold down "Control", or "Command" on a Mac, to select more than one.'))
        for key in self.fields:
            if self.fields[key].__class__.__name__ is 'ModelMultipleChoiceField':
                self.fields[key].help_text = self.fields[key].help_text.replace(remove_message, '').strip()






