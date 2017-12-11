from django.views.generic.edit import CreateView
from .tasks import task_mail_register
from .forms import UserCreationForm


class CreateUserView(CreateView):
    template_name = 'registration/register.html'
    form_class = UserCreationForm
    success_url = '/'
    http_method_names = ('get', 'post', )

    def form_valid(self, form):
        response = super().form_valid(form)
        task_mail_register.delay(self.object.pk)
        return response


