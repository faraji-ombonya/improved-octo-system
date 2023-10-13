from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.conf import settings
from .utils import file_management as fm
from .serializers import EnrollSerializer, RecognizeSerializer
from myuser.models import MyUser
from myuser.serializers import MyUserSerializer
import multiprocessing
import logging
from deepface import DeepFace

logger = logging.Logger("__name__")

@api_view(['POST'])
def enroll(request):
    """
    Enroll a user.
    """
    if request.method == 'POST':

        serializer = EnrollSerializer(data=request.data)        
        if serializer.is_valid():
            serializer.save()
            user_id = serializer.data.get('user_id')
            user = get_object_or_404(MyUser, pk=user_id)

            # get uuid
            uuid = user.id

            # set source
            image_name = serializer.data['image']
            source = f"{settings.BASE_DIR}{image_name}"

            # set destination
            file_name = image_name.replace('/mydeepface/uploads', '')
            destination = f"{settings.BASE_DIR}/mydeepface/user/database/{uuid}{file_name}"

            logger.info(f"Moving enrollment image from SOURCE: {source} to DESTINATION: {destination}")
            fm.move_image(source_path=source, destination_path=destination)

            # delete pickle file
            pickle_file_path = f"{settings.BASE_DIR}/mydeepface/user/database/representations_facenet512.pkl"
            
            bg_delete_pickle_file = multiprocessing.Process(
                target=fm.delete_file, args=(pickle_file_path,))
            bg_delete_pickle_file.start()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def recognize(request):
    if request.method == "POST":
        serializer = RecognizeSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            image_name = serializer.data.get("image")
            image_path = f"{settings.BASE_DIR}{image_name}"
            db_path = f"{settings.BASE_DIR}/mydeepface/user/database"

            print(f"DB_PATH: {db_path}")
            print(f"IMAGE_PATH: {image_path}")

            bg_delete_recognize_image = multiprocessing.Process(
                target=fm.delete_file, args=(image_path,))

            dfs = DeepFace.find(
                img_path=image_path,
                db_path=db_path,
                enforce_detection=False,
                model_name="Facenet512",
                distance_metric="euclidean")

            user_id = None

            for df in dfs:
                data = df.to_dict()
                identity = data.get("identity")
                if not len(identity):
                    bg_delete_recognize_image.start()
                    return Response(
                        {"detail": "no matching user found"},
                        status=status.HTTP_404_NOT_FOUND)

                user_id = fm.get_user_id_from_image_path(identity[0])
                print(f"USER_ID: {user_id}")

            if user_id:
                
                try:
                    user = MyUser.objects.get(pk=user_id)
                    serializer = MyUserSerializer(user)
                    bg_delete_recognize_image.start()
                    return Response(serializer.data)

                except MyUser.DoesNotExist:
                    bg_delete_recognize_image.start()
                    return Response(
                        {"detail": "User not found"},
                        status=status.HTTP_404_NOT_FOUND)
            else:
                bg_delete_recognize_image.start()
                return Response(
                    {"detail": "No matching user found"},
                    status=status.HTTP_404_NOT_FOUND)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
