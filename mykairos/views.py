from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import EnrollSerializer, RecognizeSerializer
from myuser.serializers import MyUserSerializer
from myuser.models import MyUser
from django.conf import settings
import mykairos.utils.kairos as k
import utils.file_management as fm
import multiprocessing


kairos = k.Kairos()

@api_view(['POST'])
def enroll(request):
    if request.method == "POST":
        serializer = EnrollSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            # get image
            image_name = serializer.data.get("image")
            image_path = f"{settings.BASE_DIR}{image_name}"

            bg_delete_enroll_image = multiprocessing.Process(
                target=fm.delete_file, args=(image_path,))

            user_id = serializer.data.get('user_id')

            try:
                user = MyUser.objects.get(pk=user_id)
            except MyUser.DoesNotExist:
                bg_delete_enroll_image.start()
                return Response(
                    {"detail": "User not found"},
                    status=status.HTTP_404_NOT_FOUND)

            # get uuid
            uuid = user.id
            kairos.enroll(image_file_path=image_path, subject_id=uuid)
            bg_delete_enroll_image.start()

            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def recognize(request):
    if request.method == "POST":
        serializer = RecognizeSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            image_name = serializer.data['image']
            base_dir = settings.BASE_DIR
            image_path = f"{base_dir}{image_name}"

            bg_delete_recognize_image = multiprocessing.Process(
                target=fm.delete_file, args=(image_path,))

            subject_id = kairos.recognize(image_file_path=image_path)
    
            if not subject_id:
                bg_delete_recognize_image.start()
                return Response(
                    {"detail":"face matching face id not found"},
                    status=status.HTTP_404_NOT_FOUND)
            
            try:
                user = MyUser.objects.get(pk=subject_id)
                serializer = MyUserSerializer(user)
                bg_delete_recognize_image.start()
                return Response(serializer.data)
            
            except MyUser.DoesNotExist:
                bg_delete_recognize_image.start()
                return Response(
                    {"detail": "User not found"},
                    status=status.HTTP_404_NOT_FOUND)
    
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
