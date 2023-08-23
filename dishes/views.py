from django.views import generic

from dishes.models import Dish


class DishListView(generic.ListView):
    model = Dish
    template_name = "dishes/dishes_list.html"
