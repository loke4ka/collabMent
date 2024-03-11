from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import requests
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth import login
from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from .models import Friendship , Profile
from rest_framework import generics
from .serializers import ProfileSerializer
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404




from stream_chat import StreamChat


from .models import CustomUser
from .serializers import CustomUserSerializer


@csrf_exempt
def options(request, *args, **kwargs):
    response = JsonResponse({'message': 'OPTIONS request received'})
    response['Access-Control-Allow-Origin'] = '*' 
    response['Access-Control-Allow-Methods'] = 'POST, GET, OPTIONS, PUT, DELETE'
    response['Access-Control-Allow-Headers'] = 'Content-Type'
    response['Access-Control-Max-Age'] = '86400'
    return response


@csrf_exempt
def user_list(request):
    if request.method == 'GET':
        users = CustomUser.objects.all()  # Fetch all users from the database
        user_list = [{'id': user.id, 'username': user.username, 'email': user.email} for user in users]
        return JsonResponse(user_list, safe=False)

    elif request.method == 'POST':
        return JsonResponse({'message': 'POST request received'})

    response = JsonResponse({'message': 'Method not allowed'})
    response.status_code = 405 
    return response

@csrf_exempt
def user_detail(request, pk):
    if request.method == 'GET':
        return JsonResponse({'message': 'GET request received'})
    elif request.method == 'PUT':
        return JsonResponse({'message': 'PUT request received'})
    elif request.method == 'DELETE':
        return JsonResponse({'message': 'DELETE request received'})
    
    response = JsonResponse({'message': 'Method not allowed'})
    response.status_code = 405 
    return response

@csrf_exempt
@api_view(['POST'])
def login_user(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(request, username=username, password=password)

    if user is not None:
        login(request, user)  

        # Получаем токен пользователя из модели
        token = user.chat_token

        return Response({
            'message': 'Authentication successful',
            'token': token,
            'user_id': user.id,
        }, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)



User = get_user_model()

api_key = '5E8C08782F3DBC157E2A2E9802D629F20A16F2793D69311F8F64F4767072F5AE19BD6E0B614E9857FBF8B56744571859'
subject = 'Test Email'
body = 'This is a test email.'
to = ''

@api_view(['POST'])
@csrf_exempt
@permission_classes([AllowAny])
def register_user(request):
    serializer = CustomUserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()

        # Инициализация клиента Stream Chat
        chat_client = StreamChat(api_key="4s4gsvyuueje", api_secret="74ejb8d7sv4uj2z32ze7s4kc3acvwn6m5e2ns2vmrwc8jwyswju5z3phr5s9mpm3")

        # Добавление пользователя
        chat_client.update_user({"id": user.username, "name": user.username})

        # Создание токена для пользователя
        token = chat_client.create_token(user.username)

        # Сохраняем токен в модели пользователя
        user.chat_token = token
        user.save()

        profile = Profile.objects.create(user=user)

        response_data = {
            'username': user.username,
            'email': user.email,
            'phone_number': user.phone_number,
            'token': token,  # Возвращаем токен в ответе на успешную регистрацию
        }

        # if send_email(api_key, subject, body, user.email):
        #     print('Email was sent successfully.')
        # else:
        #     print('Email sending failed.')
        
        return Response(response_data, status=status.HTTP_201_CREATED)
    print(serializer.errors)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




def send_email(api_key, subject, body, to):
    response = requests.post(
        'https://api.elasticemail.com/v2/email/send',
        data={
            'apikey': api_key,
            'subject': subject,
            'from': 'nitr1248@gmail.com',
            'fromName': 'Test2',
            'to': to,
            'bodyHtml': body,
        }
    )

    if response.status_code == 200:
        return True
    else:
        return False
    

@api_view(['POST'])
def add_friend(request, friend_id):
    try:
        friend = User.objects.get(pk=friend_id)
    except User.DoesNotExist:
        return Response({'error': 'Friend does not exist'}, status=status.HTTP_404_NOT_FOUND)
    
    user = request.user

    if user == friend:
        return Response({'error': 'Cannot add yourself as a friend'}, status=status.HTTP_400_BAD_REQUEST)

    if Friendship.objects.filter(user=user, friend=friend).exists():
        return Response({'error': 'Friendship already exists'}, status=status.HTTP_400_BAD_REQUEST)

    friendship1 = Friendship(user=user, friend=friend)
    friendship1.save()
    friendship2 = Friendship(user=friend, friend=user)
    friendship2.save()

    return Response({'message': 'Friend added successfully'}, status=status.HTTP_201_CREATED)

@api_view(['POST'])
def remove_friend(request, friend_id):
    try:
        friend = User.objects.get(pk=friend_id)
    except User.DoesNotExist:
        return Response({'error': 'Friend does not exist'}, status=status.HTTP_404_NOT_FOUND)
    
    user = request.user

    if user == friend:
        return Response({'error': 'Cannot remove yourself from friends'}, status=status.HTTP_400_BAD_REQUEST)

    Friendship.objects.filter(user=user, friend=friend).delete()
    Friendship.objects.filter(user=friend, friend=user).delete()

    return Response({'message': 'Friend removed successfully'}, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def user_friends(request, user_id):
    try:
        user = CustomUser.objects.get(id=user_id)
        friends = Friendship.objects.filter(user=user)
        friend_ids = [friend.friend.id for friend in friends]
        friend_users = CustomUser.objects.filter(id__in=friend_ids)
        serializer = CustomUserSerializer(friend_users, many=True)
        return Response(serializer.data)
    except CustomUser.DoesNotExist:
        return Response(status=404)

@api_view(['GET'])
def all_users(request):
    users = CustomUser.objects.all()
    serializer = CustomUserSerializer(users, many=True)
    return Response(serializer.data)


class MyProfileUpdateAPIView(generics.UpdateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

    def get_object(self):
        return self.request.user.profile

class PersonalInfoUpdateAPIView(generics.UpdateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


class UserProfileAPIView(APIView):
    def get(self, request):
        username = request.query_params.get('username')

        try:
            profile = Profile.objects.get(user__username=username)
        except Profile.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = ProfileSerializer(profile)

        return Response(serializer.data, status=status.HTTP_200_OK)


class UserProfileView(generics.RetrieveAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = CustomUserSerializer

    def get_object(self):
        username = self.kwargs.get('username')
        return self.queryset.get(username=username)
    
# class UserProfileView(generics.RetrieveAPIView):
#     queryset = get_user_model().objects.all()
#     serializer_class = ProfileSerializer

#     def get_object(self):
#         username = self.kwargs.get('username')
#         return self.queryset.get(username=username)
    
from django.http import Http404
from rest_framework.generics import RetrieveUpdateAPIView
from django.http import QueryDict


class UserProfileUpdateAPIView(generics.RetrieveUpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

    def get_object(self):
        username = self.kwargs.get('username')
        try:
            user = CustomUser.objects.get(username=username)
            return user
        except CustomUser.DoesNotExist:
            raise Http404("User not found.")

    def patch(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        serializer = self.get_serializer(instance, data=request.data, partial=True)  # Установка partial=True
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileUpdateAPIView(generics.RetrieveUpdateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

    def get_object(self):
        username = self.kwargs.get('username')
        print(username)
        try:
            profile = Profile.objects.get(user__username=username)
            print(profile)
            return profile
        except Profile.DoesNotExist:
            raise Http404("Profile not found.")

    def patch(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        serializer = self.get_serializer(instance, data=request.data, partial=True) 
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
from .models import Post
from .serializers import PostSerializer

class PostCreateAPIView(generics.CreateAPIView):
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        username = self.kwargs.get('username')
        author = User.objects.get(username=username)
        # Получаем профиль пользователя
        profile = author.profile
        serializer.save(author=author, profile=profile)

    

from rest_framework import generics, pagination

class StandardResultsSetPagination(pagination.PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class PostListAPIView(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    pagination_class = StandardResultsSetPagination
        
class UserPostListAPIView(generics.ListAPIView):
    serializer_class = PostSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        username = self.kwargs.get('username')
        return Post.objects.filter(author__username=username)


