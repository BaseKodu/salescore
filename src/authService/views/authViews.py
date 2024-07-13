from django.shortcuts import render, redirect
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
import json


from accounts.serializers import UserSerializer
from .models import User
from .forms import EmailAuthenticationForm, UserForm



'''
Create class based views for your rest data
'''


'''

@method_decorator(csrf_exempt, name='dispatch')
class RegistrationView(APIView):

    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [AllowAny]

    def post(self, request, format=None):
        print("Inside Post")
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        form = EmailAuthenticationForm(data=request.data)  # Pass only the request data
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            # Ensure CSRF token is sent to the client
            csrf_token = get_token(request)
            return Response({"detail": "Successfully logged in", "csrf_token": csrf_token}, status=status.HTTP_200_OK)
        return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        logout(request)
        return Response({"detail": "Successfully logged out"}, status=status.HTTP_200_OK)


class WhoAmIView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            user_serializer = UserSerializer(request.user)
            return Response(user_serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "No user is logged in."}, status=status.HTTP_200_OK)
'''


@method_decorator(csrf_exempt, name='dispatch')
class RegistrationView(View):

    def get(self, request):
        form = UserForm()
        return render(request, 'accounts/register.html', {'form': form})

    def post(self, request):
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('accounts:login')  # Replace with your success URL
        return render(request, 'accounts/register.html', {'form': form})





class LoginView(View):
    def get(self, request):
        form = EmailAuthenticationForm()
        return render(request, 'accounts/login.html', {'form': form})

    def post(self, request):
        form = EmailAuthenticationForm(request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')  # Replace with your home URL or success URL
        return render(request, 'accounts/login.html', {'form': form})



    def form_valid(self, form):
        redirect_to = self.get_redirect_url()
        return redirect(redirect_to or self.get_success_url())

    def get_redirect_url(self):
        redirect_to = self.request.POST.get(self.redirect_field_name, '')
        if redirect_to:
            return redirect_to
        return super().get_redirect_url()


@login_required
def LogoutView(request):
    logout(request)
    return redirect('landing')
