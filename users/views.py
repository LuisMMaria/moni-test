from django.views.generic import CreateView, ListView, DeleteView, UpdateView
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect

# Import User model
from .models import User
# Import User form
from .forms import UserForm


# View to create new user
class CreateUser(SuccessMessageMixin, CreateView):
    model = User
    form_class = UserForm
    template_name = 'users/create_user.html'
    success_url = reverse_lazy('login')
    success_message = "Usuario %(username)s creado correctamente"


# View for list users
class ListUser(ListView):
    template_name = 'users/list_users.html'
    context_object_name = 'users'
    queryset = User.objects.filter(is_active=True)


# View for logical deletion of user
class DeleteUser(DeleteView):
    model = User
    success_url = reverse_lazy('users:list_user')

    # Override POST method to do logic delete
    def post(self, request, pk, *args, **kwargs):
        object = User.objects.get(id=pk)
        object.is_active = False
        object.save()
        return redirect('users:list_user')


# View for update user
class UpdateUser(UpdateView):
    model = User
    form_class = UserForm
    template_name = 'users/create_user.html'
    success_url = reverse_lazy('users:list_user')
