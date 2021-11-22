from django.contrib.auth.mixins import AccessMixin


class SuperUserMixin(AccessMixin):
    """Verify that the current user is superuser."""

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)
