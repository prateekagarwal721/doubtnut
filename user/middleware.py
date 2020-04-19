from django.utils import timezone

from .models import DUser


class UpdateLastActivityMiddleware(object):
    def process_view(self, request, view_func, view_args, view_kwargs):
        assert hasattr(request, 'user')
        if request.user.is_authenticated():
            DUser.objects.filter(id=request.user.id).update(last_activity=timezone.now())