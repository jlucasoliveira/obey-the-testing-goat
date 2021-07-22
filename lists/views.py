from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


def home_page(request: HttpRequest) -> HttpResponse:
    # if request.method == "POST":
    #     return HttpResponse(request.POST["item_text"])
    return render(request, "lists/home.html", {"new_item_text": request.POST.get("item_text", "")})
