from django.shortcuts import reverse
from django.shortcuts import redirect
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect


class CheckManagerMixin:

    def dispatch(self, request, *args, **kwargs):
        if request.user.groups.filter(name='manager').exists():
            return super(
                CheckManagerMixin, self
                ).dispatch(
                    request, *args, **kwargs
                    )
        else:
            return redirect('home')
