from django.views import generic

from dishes.models import Dish, DishType


class DishListView(generic.ListView):
    model = Dish
    template_name = "dishes/dishes_list.html"


class DishTypeListView(generic.ListView):
    model = DishType
    context_object_name = "dish_type_list"
    template_name = "dishes/dish_types_list.html"
