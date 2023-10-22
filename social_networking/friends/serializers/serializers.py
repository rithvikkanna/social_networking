from rest_framework import serializers
from friends.constants.enums import FriendRequestAction


class UserSignupSerializer(serializers.Serializer):
    email_id = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    name = serializers.CharField()


class UserLoginSerializer(serializers.Serializer):
    email_id = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    # class Meta:
    #     fields = '__all__'


class SearchQuerySerializer(serializers.Serializer):
    search_key = serializers.CharField(max_length=255)
    limit = serializers.IntegerField(min_value=1, required=False)
    offset = serializers.IntegerField(min_value=0, required=False)

    # class Meta:
    #     fields = '__all__'


class FriendRequestSerializer(serializers.Serializer):
    action = serializers.ChoiceField(
        [FriendRequestAction.REJECT_REQUEST.value, FriendRequestAction.ACCEPT_REQUEST.value,
         FriendRequestAction.SEND_REQUEST.value])
    sender_user_id = serializers.CharField(max_length=255)
    receiver_user_id = serializers.CharField(max_length=255)
