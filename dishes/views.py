from django.shortcuts import render
from django.views import generic

from dishes.models import Dish


class DishListView(generic.ListView):
    class_name = Dish
