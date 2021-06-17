from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm


def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)

        if form.is_valid():
            user = form.save()

            messages.success(request, "Twoje konto zostało utworzone.")

            if not user.is_active:
                messages.warning(
                    request,
                    "Konto jest nieaktywne i nie można się na nie zalogować. "
                    "W celu jego aktywacji skontaktuj się z administratorem.",
                )

            return redirect("login")
    else:
        form = UserRegisterForm()

    context = {"form": form}

    return render(request, "users/register.html", context)
