from django.core.validators import validate_email as django_validate_email
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login

from core.helpers.form_errors import copy_global_error
from ..models import User
from ..forms import ResetPasswordRequestForm, ResetPasswordConfirmForm
from ..decorators import redirect_authenticated


@redirect_authenticated
def request(request):
    """
    The user requests a password reset.
    """

    response = None
    context = {}
    reset_password_request_form = ResetPasswordRequestForm(request.POST)

    if request.method == 'POST':

        user = reset_password_request_form.reset_password_request()

        if user:
            response = redirect('users:reset_password:requested')
            request.session['reset_password_email'] = user.email
        else:
            context.update({
                'data': reset_password_request_form.data,
                'errors': reset_password_request_form.errors
            })

    if not response:

        context['fields'] = reset_password_request_form.fields

        response = render(
            request,
            'users/reset-password/request.html',
            context
        )

    return response

@redirect_authenticated
def requested(request):
    """
    The page after a successful password reset request, where the user
    get's instructed to check his email for further instructions.
    """

    email = request.session.get('reset_password_email')

    return render(
        request,
        'users/reset-password/requested.html',
        {'email': email}
    )

@redirect_authenticated
def confirm(request):
    """
    The page a user comes to from the password reset email.
    """

    user = authenticate(
        username=request.GET.get('email'),
        validation_token=request.GET.get('validation_token')
    )

    if user:
        response = confirm_valid(request, user)
    else:
        response = render(
            request,
            'users/reset-password/invalid-token.html'
        )

    return response

@redirect_authenticated
def confirm_valid(request, user):
    """
    The page a validated user comes to from the password reset email.
    """

    response = None
    context = {}
    reset_password_confirm_form = (
        ResetPasswordConfirmForm(request.POST, user)
    )

    if request.method == 'POST':

        if reset_password_confirm_form.reset_password():
            login(request, user)
            response = redirect('users:reset_password:completed')
        else:

            copy_global_error(
                reset_password_confirm_form,
                'passwords_mismatch',
                'new_password1'
            )

            context.update({
                'data': reset_password_confirm_form.data,
                'errors': reset_password_confirm_form.errors
            })

    if not response:

        context['fields'] = reset_password_confirm_form.fields

        response = render(
            request,
            'users/reset-password/confirm.html',
            context
        )

    return response

def completed(request):
    """
    The page the user sees when the password reset has been completed.
    """

    return render(
        request,
        'users/reset-password/completed.html',
    )
