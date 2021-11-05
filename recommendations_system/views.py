from django.http import JsonResponse
from django.shortcuts import render
from api.recommendations import get_response
from api import dataset


def main_page(request):
    return render(request, "recommendations_system/index.html")


def get_recommendations(request):

    print(type(dataset))
    user_id = request.GET.get('user_id', 0)
    print(request.GET)
    return JsonResponse(get_response(int(user_id), dataset))
# Create your views here.


dataset.load('api/dataset/')