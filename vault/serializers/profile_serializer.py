
from rest_framework import serializers 
from ..model.user_model import Profile

class ProfileSerializer(serializers.ModelSerializer):

    username = serializers.CharField(
        source='user.username',
        read_only=True
    )

    email = serializers.EmailField(
        source='user.email'
    )

    class Meta:
        model = Profile

        fields = [
            'username',
            'email',
            'full_name',
            'bio',
            'profile_image',
            'phone_number',
            'location',
            'website',
            'profile_completed',
            'two_factor_enabled',
            'security_score',
            'weak_password_count',
            'reused_password_count',
            'created_at'
        ]

        read_only_fields = [
            'security_score',
            'weak_password_count',
            'reused_password_count',
            'created_at'
        ]

    def update(self, instance, validated_data):

        user_data = validated_data.pop('user', {})

        user = instance.user

        user.email = user_data.get(
            'email',
            user.email
        )

        user.save()

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        # AUTO PROFILE COMPLETION
        required_fields = [
            instance.full_name,
            instance.bio
        ]

        instance.profile_completed = all(required_fields)

        instance.save()

        return instance