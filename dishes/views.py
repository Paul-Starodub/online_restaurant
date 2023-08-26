from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import QuerySet
from django.http import HttpResponseRedirect, HttpRequest
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views import generic

from dishes.forms import NameSearchForm
from dishes.models import Dish, DishType
from users.models import User


class DishListView(LoginRequiredMixin, generic.ListView):
    template_name = "dishes/dishes_list.html"
    queryset = Dish.objects.select_related("dish_type")
    paginate_by = 5

    def get_context_data(self, **kwargs: dict) -> dict:
        context = super().get_context_data(**kwargs)

        self.request.session["num_visits"] = (
            self.request.session.get("num_visits", 0) + 1
        )
        context["num_visits"] = self.request.session.get("num_visits", 1)

        name = self.request.GET.get("name", "")
        context["search_form"] = NameSearchForm(
            initial={
                "name": name
            }
        )

        return context

    def get_queryset(self) -> QuerySet:
        form = NameSearchForm(self.request.GET)
        queryset = Dish.objects.select_related("dish_type")

        if form.is_valid():
            return queryset.filter(
                name__icontains=form.cleaned_data["name"]
            )

        return queryset


class DishDetailView(LoginRequiredMixin, generic.DetailView):
    model = Dish
    template_name = "dishes/dish-detail.html"


class DishTypeListView(LoginRequiredMixin, generic.ListView):
    model = DishType
    context_object_name = "dish_type_list"
    template_name = "dishes/dish_types-list.html"
    paginate_by = 5


class UpdateLikeView(generic.DetailView):
    model = Dish
    fields = "__all__"
    success_url = reverse_lazy("cuisine:dish-detail")

    def get(
        self, request: HttpRequest, *args: tuple, **kwargs: dict
    ) -> HttpResponseRedirect:
        dish = get_object_or_404(Dish, pk=self.kwargs["pk"])
        user = get_object_or_404(User, pk=self.request.user.pk)
        if user not in dish.likes.all():
            dish.likes.add(user)
        else:
            dish.likes.remove(user)
        return HttpResponseRedirect(
            reverse("cuisine:dish-detail", kwargs={"pk": self.kwargs["pk"]})
        )
