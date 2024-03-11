from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Profile, Post

class CustomUserSerializer(serializers.ModelSerializer):
    friends = serializers.SerializerMethodField()

    class Meta:
        model = get_user_model()
        fields = ('id', 'username', 'email', 'password', 'phone_number', 'friends', 'birthday', 'gender', 'user_type', 'first_name', 'last_name')
        extra_kwargs = {'password': {'write_only': True, 'required': False}}

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = get_user_model().objects.create_user(**validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user

    def get_friends(self, obj):
        friends = obj.friends.all()
        if friends:
            serializer = self.__class__(friends, many=True)
            return serializer.data
        return []



class ProfileSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer()

    class Meta:
        model = Profile
        fields = ['user', 'professional_field', 'education', 'current_job', 'experience', 'location', 'personal_qualities', 'certificates', 'resume', 'profile_photo' , 'education_date' , 'name_institution', 'desired_position' , 'type_of_work', 'operating_mode' , 'name_organization', 'position', 'experience_name', 'citizenship', 'city' , 'passage_time' ] 

    def get_username(self, obj):
        return obj.user.username

class PostSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()
    profile = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = '__all__'

    def get_author(self, obj):
        # Получаем данные автора поста
        author = obj.author
        return {
            'id': author.id,
            'username': author.username,
            'email': author.email,
            'phone_number': author.phone_number,
            'first_name': author.first_name,
            'last_name': author.last_name,
            'user_type': author.user_type
            }

    def get_profile(self, obj):
        # Получаем данные профиля автора поста
        profile = obj.author.profile
        serializer = ProfileSerializer(profile)
        return serializer.data
        