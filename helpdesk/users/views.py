from django.contrib.auth import login, authenticate
from django.contrib.auth import logout as logout_
from django.http import HttpResponse
from django.shortcuts import render, redirect

from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from users.forms import RegisterForm
from users.models import User

from users.api.serializers import UserSerializer


def register(request):
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = User(
                username=form.cleaned_data.get('username'),
                email=form.cleaned_data.get('email'),
            )
            user.set_password(form.cleaned_data.get('password'))
            user.save()
            login(request, user)
            return redirect('/')
    return render(request, 'users/register_page.html', {'form': form})


def logout(request):
    logout_(request)
    return redirect('/')


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, ]


class ObtainTokenView(APIView):
    http_method_names = ['post']
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        user = authenticate(request,
                            username=self.request.data.get('username'),
                            password=self.request.data.get('password'))
        if user is not None:
            return Response(str(Token.objects.get(user=user)), 200)
        else:
            return HttpResponse(status=401)
