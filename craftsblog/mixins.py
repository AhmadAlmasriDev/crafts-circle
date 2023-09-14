from django.shortcuts import reverse
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect

class CheckManagerMixin:

    def dispatch(self, request, *args, **kwargs):
        if request.user.groups.filter(name='manager').exists():
            return True
        else:
            return HttpResponseRedirect(reverse('home'))