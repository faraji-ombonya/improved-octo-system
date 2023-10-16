from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.conf import settings
from myuser.models import MyUser
from myuser.serializers import MyUserSerializer
from .serializers import EnrollSerializer, RecognizeSerializer
import myamazonrekognition.utils.amazon_rekognition as ar
import utils.file_management as fm
import multiprocessing

@api_view(['GET'])
def enroll(request):
    serializer = EnrollSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()

        # get image
        image_name = serializer.data.get("image")
        image_path = f"{settings.BASE_DIR}{image_name}"
        bg_delete_enroll_image = multiprocessing.Process(
            target=fm.delete_file, args=(image_path,))

        # get user
        user_id = serializer.data.get("user_id")
        try:
            user = MyUser.objects.get(pk=user_id)
        except:
            bg_delete_enroll_image.start()
            return Response(
                {"detail": "User not found"},
                status=status.HTTP_404_NOT_FOUND)
        uuid = user.id

        # index face
        result = ar.index_face(
            image_file_name=image_path,
            image_name=image_name)
        
        print(f"INDEX FACE RESULTS: {result}")
        if not result:
            return Response(
                {"detail":"failed to index face"}, 
                status=status.HTTP_400_BAD_REQUEST)
        
        # associate face with user in the collection
        face_ids = []
        face_id = result.get("face_id")
        face_ids.append(face_id)
        response = ar.associate_faces(
            collection_id=settings.AWS_REKOGNITION_COLLECTION_ID,
            user_id=user_id,
            face_ids=face_ids)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['GET'])
def recognize(request):
    serializer = RecognizeSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()

        # image
        image_name = serializer.data.get("image")
        image_path = f"{settings.BASE_DIR}{image_name}"
        bg_delete_recognize_image = multiprocessing.Process(
                target=fm.delete_file, args=(image_path,))
        
        # get face id
        face_id = ar.search_face(
            image_path=image_path,
            image_name=image_name)
            
        if not face_id:
            bg_delete_recognize_image.start()
            return Response(
                {"detail":"face matching face id not found"}, 
                status=status.HTTP_404_NOT_FOUND)

        # search user by face id
        result = ar.search_users_by_face_id(
            collection_id=settings.AWS_REKOGNITION_COLLECTION_ID,
            face_id=face_id)

        if result is None:
            bg_delete_recognize_image.start()
            return Response(
                {"detail":"user not found"},
                status=status.HTTP_404_NOT_FOUND)
        
        # get matched users
        user_matches = result.get("UserMatches")
        if not len(user_matches):
            bg_delete_recognize_image.start()
            return Response(
                {"detail":"user not found"},
                status=status.HTTP_404_NOT_FOUND)

        # get user
        user_id = result['UserMatches'][0]['User']['UserId']
        try:
            user = MyUser.objects.get(pk=user_id)
        except MyUser.DoesNotExist:
            bg_delete_recognize_image.start()
            return Response(
                {"detail":"user not found"},
                status=status.HTTP_404_NOT_FOUND)

        serializer = MyUserSerializer(user)
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
