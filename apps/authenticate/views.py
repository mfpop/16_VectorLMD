from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Profile
from django.contrib.auth.views import (
    PasswordChangeView,
    PasswordResetView,
    PasswordResetConfirmView,
)
from django.urls import reverse_lazy


class CustomPasswordChangeView(PasswordChangeView):
    template_name = "authenticate/password_change.html"
    success_url = reverse_lazy("profile")

    def form_valid(self, form):
        messages.success(self.request, "Your password has been updated successfully!")
        return super().form_valid(form)


class CustomPasswordResetView(PasswordResetView):
    template_name = "authenticate/password_reset.html"
    email_template_name = "authenticate/password_reset_email.html"
    success_url = reverse_lazy("password_reset_done")

    def form_valid(self, form):
        messages.info(
            self.request, "Password reset instructions have been sent to your email."
        )
        return super().form_valid(form)


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = "authenticate/password_reset_confirm.html"
    success_url = reverse_lazy("password_reset_complete")

    def form_valid(self, form):
        messages.success(self.request, "Your password has been reset successfully!")
        return super().form_valid(form)


class UserUpdateForm(forms.ModelForm):
    """Form for updating user information"""

    class Meta:
        model = User
        fields = ["first_name", "last_name", "email"]
        widgets = {
            "first_name": forms.TextInput(
                attrs={
                    "class": "w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-400"
                }
            ),
            "last_name": forms.TextInput(
                attrs={
                    "class": "w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-400"
                }
            ),
            "email": forms.EmailInput(
                attrs={
                    "class": "w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-400"
                }
            ),
        }


class ProfileUpdateForm(forms.ModelForm):
    """Form for updating profile information, including avatar"""

    class Meta:
        model = Profile
        fields = ["avatar"]
        widgets = {
            "avatar": forms.FileInput(attrs={"class": "hidden", "id": "avatar-upload"}),
        }


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)

    class Meta:
        model = User
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add tailwind styling to form fields
        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = (
                "w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-400"
            )


def register_view(request):
    """
    Handle user registration
    """
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Auto-login after registration
            login(request, user)
            messages.success(
                request, f"Account created successfully! Welcome, {user.username}!"
            )
            return redirect("home")
    else:
        form = RegisterForm()

    return render(request, "authenticate/register.html", {"form": form})


def login_view(request):
    """
    Handle user login authentication
    """
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back, {username}!")
                # Redirect to homepage or next page
                next_url = request.GET.get("next", "home")
                return redirect(next_url)
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()

    return render(request, "authenticate/login.html", {"form": form})


def logout_view(request):
    """
    Handle user logout
    """
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect("login")


@login_required
def profile_view(request):
    """
    Handle user profile view and updates
    """
    # Ensure profile exists
    try:
        profile = request.user.authenticate_profile
    except:
        # Create profile if it doesn't exist
        from apps.authenticate.models import Profile

        profile = Profile.objects.create(user=request.user)

    if request.method == "POST":
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, "Your profile has been updated!")
            return redirect("profile")
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=profile)

    context = {"form": u_form, "p_form": p_form}
    return render(request, "authenticate/profile.html", context)
