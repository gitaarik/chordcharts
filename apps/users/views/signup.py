from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from core.helpers import form
from ..models import User
from ..forms import SignUpForm
from ..decorators import redirect_authenticated


@redirect_authenticated
def signup(request):
    """
    Where the user can sign up.
    """

    response = None
    signup_form = SignUpForm(request.POST)

    if request.method == 'POST':

        form_submitted = True

        if signup_form.is_valid():
            user = signup_form.signup()
        else:
            user = None

        if user:
            request.session['signup_email'] = user.email
            response = redirect('users:signup:validate_email')
        else:
            form.copy_global_error(signup_form, 'integrity', 'username')
            form.copy_global_error(signup_form, 'passwords_dont_match', 'password1')

    else:
        form_submitted = False

    if not response:

        field_info = form.field_info(signup_form, form_submitted)

        response = render(
            request,
            'users/signup/signup.html',
            {'fields': field_info}
        )

    return response


@redirect_authenticated
def resend_validation_email(request):
    """
    Asks the user if he wants to resend the validation email (to confirm
    his/her email address).
    """

    email = request.GET.get('email')

    if not email:
        response = redirect('users:login')
    else:

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            response = redirect('users:signup:signup')
        else:

            if user.validated:
                response = redirect('users:home')
            else:
                user.send_validation_email()
                response = render(
                    request,
                    'users/signup/resend-validation-email.html',
                    {'email': email}
                )

    return response


@redirect_authenticated
def validate_email(request):
    """
    The page after a successful sign up, where the user gets
    instructions about the validation email.
    """

    email = request.session.get('signup_email')

    return render(
        request,
        'users/signup/validate-email.html',
        {'email': email}
    )


@redirect_authenticated
def completed(request):
    """
    The page the user comes to from the "validate email address" email,
    where his/her email address gets validated.
    """

    user = authenticate(
        username=request.GET.get('email'),
        validation_token=request.GET.get('validation_token')
    )

    if user:
        login(request, user)
        success = True
    else:
        success = False

    return render(
        request,
        'users/signup/completed.html',
        {'success': success}
    )
