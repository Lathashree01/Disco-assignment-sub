from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from .models import Image, Customer, Plan
from rest_framework import serializers

from PIL import Image as pilimg
from io import BytesIO

# Serializer for Customer model
class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ('plan', 'user')


# Serializer for Plan modelß
class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = ('thumbnail1_height', 'thumbnail2_height', 'original_link', 'expiring_link')


# Serializer for Image upload model
class ImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(max_length=None, allow_empty_file=False, use_url=True)
    user = serializers.PrimaryKeyRelatedField(queryset=Customer.objects.all())

    class Meta:
        model = Image
        fields = ('id', 'uploaded_time', 'title', 'user', 'image','thumbnail1','thumbnail2', 'original_link')
    
    
    def create(self, validated_data):
        u_id = validated_data['user'].user_id
        plan = Customer.objects.get(user_id=u_id).plan

        # Modify the validated data to add thumbnail1, thumbnail2, original_link
        if validated_data['image']:
            validated_data = self.validate_thumbnail(validated_data, plan,u_id)
        return super().create(validated_data)
    
    def create_image_file(self, height, original_image, filename):

        # Resize the image to a particular height
        img = pilimg.open(original_image).convert('RGB')
        width, height = img.size
        ratio = height / height
        new_width = int(width * ratio)
        img = img.resize((new_width, height), pilimg.ANTIALIAS)
        output = BytesIO()
        img.save(output, format='JPEG', quality=75)
        output.seek(0)
        thumbnail1_file = ContentFile(output.read(), name=filename)

        # Save the content file to a file path using default_storage
        path = default_storage.save(filename, thumbnail1_file)
        return path

    def validate_thumbnail(self, val_data, plan, user_id):
        """
        Resize the thumbnail to a particular height and add original link as per plan information.

        TODO: Expiration link top be added

        """
        original_image = val_data['image']
        if(val_data['image']):
            if(plan.thumbnail1_height>0):
                height = plan.thumbnail1_height
                filename = str(user_id)+'/'+str(height)+'/'+val_data['image'].name
                path = self.create_image_file(height, original_image, filename)
                val_data['thumbnail1'] = path
            if(plan.thumbnail2_height>0):
                height = plan.thumbnail2_height
                filename = str(user_id)+'/'+str(height)+'/'+val_data['image'].name
                path = self.create_image_file(height, original_image, filename)
                val_data['thumbnail2'] = path
            if(plan.original_link):
                val_data['original_link'] = original_image.name
        return val_data

    # Modify the data here for representation purpose
    def to_representation(self, instance):
        data = super().to_representation(instance)
        del data['image']
        return data


# Serializer for Image list model
class ImageListSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=Customer.objects.all())

    class Meta:
        model = Image
        fields = ('id', 'uploaded_time', 'title', 'user', 'original_link', 'thumbnail2','thumbnail1')
        queryset = Image.objects.all()
    
    
   