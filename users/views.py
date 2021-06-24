from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils.translation import ugettext as _

from .forms import UserRegisterForm


def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)

        if form.is_valid():
            user = form.save()

            messages.success(request, _("Your account has been created."))

            if not user.is_active:
                messages.warning(
                    request,
                    " ".join(
                        [
                            _("The account is inactive and you cannot log into it."),
                            _("Please contact the administrator to activate it."),
                        ]
                    ),
                )

            return redirect("login")
    else:
        form = UserRegisterForm()

    context = {"form": form}

    return render(request, "users/register.html", context)
