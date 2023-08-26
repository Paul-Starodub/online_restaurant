from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, HttpRequest
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views import generic

from dishes.models import Dish, DishType
from users.models import User


class DishListView(LoginRequiredMixin, generic.ListView):
    template_name = "dishes/dishes_list.html"
    queryset = Dish.objects.select_related("dish_type")
    paginate_by = 5


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
