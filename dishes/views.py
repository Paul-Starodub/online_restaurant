import os

from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views import generic

from dishes.forms import DishCustomizeForm, NameSearchForm
from dishes.models import Basket, Dish, DishType


def is_admin(user) -> bool:
    return user.is_authenticated and user.is_staff


decorators = [login_required, user_passes_test(is_admin)]


class IndexView(LoginRequiredMixin, generic.TemplateView):
    template_name = "dishes/index.html"

    def get_context_data(self, **kwargs: dict) -> dict:
        context = super().get_context_data(**kwargs)
        self.request.session["num_visits"] = (
            self.request.session.get("num_visits", 0) + 1
        )
        context["num_visits"] = self.request.session.get("num_visits", 1)
        context["count_dishes"] = Dish.objects.count()
        context["count_dish_types"] = DishType.objects.count()
        context["contact"] = os.getenv("CONTACT")

        return context


class DishListView(LoginRequiredMixin, generic.ListView):
    template_name = "dishes/dishes_list.html"
    paginate_by = 5

    def get_context_data(
        self, *, object_list: list = None, **kwargs: dict
    ) -> dict:
        context = super().get_context_data()
        name = self.request.GET.get("name", "")
        context["search_form"] = NameSearchForm(initial={"name": name})
        context["user"] = self.request.user

        return context

    def get_queryset(self) -> QuerySet:
        form = NameSearchForm(self.request.GET)
        queryset = Dish.objects.select_related("dish_type")

        if form.is_valid():
            return queryset.filter(name__icontains=form.cleaned_data["name"])

        return queryset


class DishDetailView(LoginRequiredMixin, generic.DetailView):
    queryset = Dish.objects.prefetch_related(
        "posts__commentaries", "likes"
    ).select_related("dish_type")

    def get_context_data(self, **kwargs: dict) -> dict:
        context = super().get_context_data(**kwargs)
        context["user"] = self.request.user

        return context


@method_decorator(decorators, name="dispatch")
class DishCreateView(generic.CreateView):
    model = Dish
    form_class = DishCustomizeForm
    success_url = reverse_lazy("cuisine:dish-list")


@method_decorator(decorators, name="dispatch")
class DishUpdateView(generic.UpdateView):
    model = Dish
    form_class = DishCustomizeForm
    success_url = reverse_lazy("cuisine:dish-list")


@method_decorator(decorators, name="dispatch")
class DishDeleteView(generic.DeleteView):
    model = Dish
    success_url = reverse_lazy("cuisine:dish-list")


class DishTypeListView(LoginRequiredMixin, generic.ListView):
    model = DishType
    context_object_name = "dish_type_list"
    template_name = "dishes/dish_types_list.html"
    paginate_by = 5


class DishTypeDetailView(LoginRequiredMixin, generic.DetailView):
    model = DishType
    template_name = "dishes/dish_type_detail.html"


@method_decorator(decorators, name="dispatch")
class DishTypeCreateView(generic.CreateView):
    model = DishType
    fields = "__all__"
    template_name = "dishes/dish_type_form.html"
    success_url = reverse_lazy("cuisine:dish_type-list")


@method_decorator(decorators, name="dispatch")
class DishTypeUpdateView(generic.UpdateView):
    model = DishType
    fields = "__all__"
    template_name = "dishes/dish_type_form.html"
    success_url = reverse_lazy("cuisine:dish_type-list")


@method_decorator(decorators, name="dispatch")
class DishTypeDeleteView(generic.DeleteView):
    model = DishType
    template_name = "dishes/dish_type_confirm_delete.html"
    success_url = reverse_lazy("cuisine:dish_type-list")


class UpdateLikeView(generic.DetailView):
    model = Dish
    fields = "__all__"

    def get(
        self, request: HttpRequest, *args: tuple, **kwargs: dict
    ) -> HttpResponseRedirect:
        dish = get_object_or_404(Dish, pk=self.kwargs["pk"])
        user = get_object_or_404(get_user_model(), pk=self.request.user.pk)
        if user not in dish.likes.all():
            dish.likes.add(user)
        else:
            dish.likes.remove(user)
        return HttpResponseRedirect(
            reverse("cuisine:dish-detail", kwargs={"pk": self.kwargs["pk"]})
        )


@login_required
def basket_add(request: HttpRequest, dish_id: int) -> HttpResponseRedirect:
    dish = get_object_or_404(Dish, pk=dish_id)
    baskets = Basket.objects.filter(user=request.user, dish=dish)

    if not baskets.exists():
        Basket.objects.create(user=request.user, dish=dish, quantity=1)
    else:
        basket = baskets.first()
        basket.quantity += 1
        basket.save()

    return HttpResponseRedirect(request.META["HTTP_REFERER"])


@login_required
def basket_remove(
    request: HttpRequest, basket_id: int
) -> HttpResponseRedirect:
    basket = get_object_or_404(Basket, id=basket_id)
    basket.delete()

    return HttpResponseRedirect(request.META["HTTP_REFERER"])
