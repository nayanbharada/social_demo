from django.shortcuts import render, redirect
from django.views.generic import *

from users.forms import LoginForm, CreateUserForm
from django.contrib.auth import authenticate, logout, login
from users.mixin import CustomActiveLoginRequiredMixin
from users.models import UserMaster
from django.contrib import messages


# Create your views here.


class UserCreateView(CreateView):
    template_name = "auth/register.html"
    form_class = CreateUserForm
    success_url = "register"

    def form_valid(self, form):
        form.save(commit=False)
        return super(UserCreateView, self).form_valid(form)

    def get_success_url(self):
        messages.success(self.request, "User Is Successfully Created.")
        return self.success_url


class LoginView(View):
    form_class = LoginForm
    template_name = "auth/login.html"

    def get(self, request):
        form = self.form_class()
        if request.user.is_authenticated:
            return redirect("users:user_dashboard")
        else:
            return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            user = authenticate(email=email, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    messages.success(request, "Login Successfully.")
                    return redirect("users:user_dashboard")
                else:
                    messages.error(request, "your account has been suspended.")
                    return render(request, self.template_name, {"form": form})
            else:
                messages.error(request, "email or password not correct")
                return render(request, self.template_name, {"form": form})
        else:
            return render(request, self.template_name, {"form": form})


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect("users:login")


class UserListView(CustomActiveLoginRequiredMixin, ListView):
    model = UserMaster
    template_name = "user/all_user.html"
    context_object_name = "all_user"
    paginate_by = 10

    def get_queryset(self):
        qs = UserMaster.objects.exclude(id=self.request.user.id).exclude(
            id__in=self.request.user.friends.all().values_list('id', flat=True))
        return qs


class UserSearchPage(UserListView):
    template_name = "user/search_user.html"

    def get_queryset(self):
        qs = UserMaster.objects.exclude(id=self.request.user.id)
        first_name = self.request.GET.get('first_name')
        if first_name:
            qs = qs.filter(first_name__contains=first_name)
        return qs


class UserFriendAdd(CustomActiveLoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        friend_id = self.request.POST.get('friend_id')
        user_obj = self.request.user
        user_obj.friends.add(*[friend_id])
        messages.success(request, "Friend Add Successfully.")
        return redirect("users:user_list")


class FriendsPageView(CustomActiveLoginRequiredMixin, DetailView):
    model = UserMaster
    template_name = "user/friends_page.html"
    context_object_name = 'user_obj'


class UserDashboard(CustomActiveLoginRequiredMixin, TemplateView):
    template_name = "dashboards/user_dashboard.html"




