from email.errors import MessageError

from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view, action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.tokens import RefreshToken

from api_yamdb import settings
from auth_user.permissions import IsOwnerProfileOrReadOnly
from .models import User
from .serializers import UserProfileSerializer


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
    lookup_field = 'username'

    def get_permissions(self):
        if self.action in (
                'get_user_info', 'update_user_info', 'destroy_user_info'):
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsOwnerProfileOrReadOnly]
        return [permission() for permission in permission_classes]

    @action(detail=True, methods=['get'], name='Detail info')
    def get_user_info(self, request):
        if request.method == 'DELETE':
            response = {
                'message': 'Delete function is not offered in this path.'}
            return Response(response, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        user = request.data
        serializer = UserProfileSerializer(request.user, data=user,
                                           partial=True)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data)


@csrf_exempt
@api_view(['POST'])
def get_confirmation(request):
    email = request.POST.get('email')
    username = request.POST.get('username')
    if email is None:
        return Response(
            "'email' and/or 'confirmation_code' are not provided",
            status=400)
    try:
        user = User.objects.get(email=email)

    except User.DoesNotExist:
        user = User()
        user.email = email
    if username is not None:
        user.username = username

    confirmation_code = default_token_generator.make_token(user)
    user.confirmation_code = confirmation_code
    user.save()

    try:
        send_mail(
            subject='Authentification',
            message=f'Your confirmation code {confirmation_code}',
            from_email=settings.SEND_FROM_EMAIL,
            recipient_list=[user.email],
        )
    except MessageError:
        return Response(f"Error while send email", status=400)
    return Response(status=201)


@csrf_exempt
@api_view(['POST'])
def obtain_token(request):
    email = request.POST.get('email')
    confirmation_code = request.POST.get('confirmation_code')

    if email is None and confirmation_code is None:
        return Response(
            "'email' and/or 'confirmation_code' are not provided", status=400)
    user = get_object_or_404(User, email=email,
                             confirmation_code=confirmation_code)
    token = RefreshToken.for_user(user)
    return Response(token.access_token)
