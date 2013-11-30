# Copyright 2013 Evan Hazlett and contributors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from django import forms
from highway.models import Domain
from crispy_forms.helper import FormHelper
from crispy_forms.layout import (Layout, Fieldset, ButtonHolder, Submit,
        Button)
from crispy_forms.bootstrap import FieldWithButtons, StrictButton, FormActions
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _
import string

class DomainForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(DomainForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
                None,
                'prefix',
                'target',
            ),
            FormActions(
                Submit('save', _('Create'), css_class="btn btn-lg btn-success"),
                Button('cancel', _('Cancel'), css_class="btn btn-lg"),
            )
        )
        self.helper.form_id = 'form-create-domain'
        self.helper.form_class = 'form-horizontal'
        self.helper.form_action = reverse('highway.views.create')

    def clean_prefix(self):
        data = self.cleaned_data['prefix']
        allowed_chars = string.letters + string.digits + '-' + '_'
        for c in data:
            if c not in allowed_chars:
                raise forms.ValidationError(_('Only alphanumeric, -, and _ are allowed'))
        return data

    class Meta:
        model = Domain
        fields = ('prefix', 'target')

