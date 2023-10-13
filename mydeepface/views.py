from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.conf import settings
from .utils import file_management as fm
from .serializers import EnrollSerializer
from myuser.models import MyUser
from myuser.serializers import MyUserSerializer
import multiprocessing
import logging

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


@api_view(['GET'])
def recognize(request):
    return Response(status=status.HTTP_200_OK)