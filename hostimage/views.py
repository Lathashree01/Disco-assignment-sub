from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView
from rest_framework import status, permissions, generics

from .serializers import ImageSerializer, ImageListSerializer
from .models import Image


@api_view(['GET'])
def host_image(request):
    return Response({"message": "Hello, Host your image here !!"})


# Image View class to handle image upload
class ImageView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        print("POST: Image received")
        # print(request.data)
        serializer = ImageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# List Image View class to handle listing images functionality
class ListImageView(generics.ListAPIView):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user_id = request.query_params.get('user')
        images = Image.objects.filter(user_id=user_id)
        serializer = ImageListSerializer(images, many=True)
        response_data = serializer.data       
        return Response(response_data)