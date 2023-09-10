from django.contrib.auth import login
from django.http import HttpResponseRedirect, HttpRequest, HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.views import generic

from users.forms import CustomerCreationForm
from users.models import User


class CustomerCreateView(generic.CreateView):

    model = User
    form_class = CustomerCreationForm

    def post(
        self, request: HttpRequest, *args: tuple, **kwargs: dict
    ) -> HttpResponseRedirect | HttpResponse:
        form = self.get_form_class()(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return HttpResponseRedirect(reverse("cuisine:dish-list"))

        else:
            form = self.get_form_class()()

        return render(request, "users/user_form.html", {"form": form})
