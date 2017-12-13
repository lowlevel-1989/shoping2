from django.views.generic.edit import CreateView
from django.urls import reverse
from .tasks import task_sendgrid_mail
from .forms import UserCreationForm


class CreateUserView(CreateView):
    template_name = 'registration/register.html'
    form_class = UserCreationForm
    success_url = '/'
    http_method_names = ('get', 'post', )

    def form_valid(self, form):
        response = super().form_valid(form)
        next_url = self.request.build_absolute_uri(
            reverse('login')
        )
        task_sendgrid_mail.delay('register',
            self.object.pk, next_url=next_url)
        return response


