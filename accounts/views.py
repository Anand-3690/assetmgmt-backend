from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from .serializers import MeSerializer
from django.views.decorators.cache import never_cache

@never_cache
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def me(request):
    return Response(MeSerializer(request.user).data)


@never_cache
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password(request):
    user = request.user
    old_password = request.data.get('old_password')
    new_password = request.data.get('new_password')

    if not user.check_password(old_password):
        raise ValidationError({'old_password': 'Incorrect current password.'})

    try:
        validate_password(new_password, user=user)
    except DjangoValidationError as e:
        raise ValidationError({'new_password': list(e.messages)})

    user.set_password(new_password)
    user.must_change_password = False
    user.save(update_fields=['password', 'must_change_password'])
    return Response({'detail': 'Password changed successfully.'})