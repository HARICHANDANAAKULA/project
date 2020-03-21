from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponseBadRequest, HttpResponse
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages
# from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode
from .tokens import account_activation_token
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponseBadRequest, HttpResponse
from .forms import CreateUserForm
from django.conf import settings

def index_view(request):
	return render(request, 'registration/index.html')


@login_required
def dashboard_view(request):
	return render(request, 'registration/dashboard.html')


def activation_sent_view(request):
	return render(request, 'registration/acc_active_emailsent.html')
def activate(request, uidb64, token):
	try:
		uid = force_text(urlsafe_base64_decode(uidb64))
		user = User.objects.get(pk=uid)
	except (TypeError, ValueError, OverflowError, User.DoesNotExist):
			user = None
	if user is not None and account_activation_token.check_token(user, token):
		user.is_active = True
		# user.profile.signup_confirmation = True
		user.profile.email_confirmation = True
		user.save()
		messages.add_message(request,messages.SUCCESS,'ACCOUNT ACTIVATED SUCCESSFULLY')
		login(request, user)
		return redirect('login_url')
	# else:
	# 	return render(request, 'registration/acc_activation_invalid.html')
	return render(request, 'registration/acc_activation_invalid.html',status=401)
def register_view(request):
	form = CreateUserForm()
	if request.method == "POST":
		form = CreateUserForm(request.POST)
		if form.is_valid():
			user = form.save(commit=False)
			user.refresh_from_db()
			user.profile.first_name = form.cleaned_data.get('first_name')
			user.profile.last_name = form.cleaned_data.get('last_name')
			user.profile.email = form.cleaned_data.get('email')
			user.is_active = False
			user.save()
			# raw_password = form.cleaned_data.get('password1')
			# user = authenticate(username=user.username, password=raw_password)
			# login(request, user)
			current_site = get_current_site(request)
			subject = 'Please Activate Your Account'
			message = render_to_string('registration/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
			email_message = EmailMessage(
				subject,
				message,
				to=[user.profile.email]
			)
			email_message.send()
			# user.email_user(subject, message)
			messages.success(request, "your account has been created. you are now able to log in")
			return redirect('activation_sent')
			# return redirect('registration:activation_sent')
			# return redirect('login_url')
	return render(request, 'registration/register.html', {'form': form})


def login_view(request):
	if request.method == 'POST':
		try:
			username, password = request.POST.get('username'), request.POST.get('password')
		except:
			return HttpResponseBadRequest()
		user = authenticate(request, username=username, password=password)
		if not user:
			return HttpResponse('Unable to login.')
		auth_login(request, user)
		return redirect('dashboard')
