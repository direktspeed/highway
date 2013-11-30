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
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.http import HttpResponse
from django.shortcuts import render_to_response, redirect
from django.contrib.auth.views import logout as auth_logout
from django.utils.translation import ugettext as _
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.conf import settings
from highway.forms import DomainForm
from highway.models import Domain
import string

def index(request):
    if request.user.is_authenticated():
        return redirect(reverse('manage'))
    ctx = {
        'domain': getattr(settings, 'R53_ZONE'),
    }
    return render_to_response('index.html', ctx,
            context_instance=RequestContext(request))

def logout(request):
    auth_logout(request)
    return redirect(reverse('index'))

@login_required
def manage(request):
    domains = Domain.objects.filter(user=request.user)
    ctx = {
        'domains': domains,
    }
    return render_to_response('manage.html', ctx,
            context_instance=RequestContext(request))

@login_required
def create(request):
    form = DomainForm()
    form.fields['target'].initial = request.META.get('REMOTE_ADDR')
    if request.method == 'POST':
        form = DomainForm(request.POST)
        target = form.data.get('target')
        if form.is_valid():
            domain = form.save()
            domain.user = request.user
            domain.source = request.META.get('REMOTE_ADDR')
            # check for record type
            is_a_record = True
            for c in target:
                if c not in string.digits and c != '.':
                    is_a_record = False
                    break
            if is_a_record:
                domain.record_type = 'a'
            else:
                domain.record_type = 'cname'
            domain.save()
            return redirect(reverse('manage'))
    ctx = {
        'form': form,
    }
    return render_to_response('create.html', ctx,
            context_instance=RequestContext(request))

@login_required
def delete(request, domain_id):
    try:
        domain = Domain.objects.get(id=domain_id, user=request.user)
        domain.delete()
    except Domain.DoesNotExist:
        messages.error(request, _('Invalid domain'))
    return redirect(reverse('manage'))
