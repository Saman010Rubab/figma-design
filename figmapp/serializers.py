from rest_framework import serializers
from . import models
from django.contrib.auth import authenticate,login



#creating serializers.

class ProfileSerializer(serializers.ModelSerializer):
    user= serializers.ReadOnlyField(source='user.username')
    class Meta:
        model= models.Profile
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    # profile = ProfileSerializer(read_only=True)

    class Meta:
        model= models.User
        fields=["id","email","password" ,"username", "role"]
    def create(self, validated_data):
        user = models.User.objects.create_user(**validated_data)
        models.Profile.objects.create(user=user)
        if user.role == 2:
            models.Publisher.objects.create(user=user)
            models.Placement.objects.create(user=user)
        elif user.role == 3:
            models.Advertiser.objects.create(user=user)
            models.Ads.objects.create(user=user)
        return user

class UserLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model= models.User
        fields=["email", "password"]

class PubSerializer1(serializers.ModelSerializer):
    class Meta:
        model= models.Publisher
        fields = ['id','company', 'vertical', 'website', 'gender_split', 'description', 'available_ad_units', 'headline_copy_length', 'body_copy_length' ]

class PubSerializer2(serializers.ModelSerializer):
    class Meta:
        model= models.Placement
        fields = ['id','placement_types', 'email_service_provider', 'open_rate', 'CTR', 'expected_clicks', 'logo_required', 'image_size']
        # read_only_fields = ['user']

class PubSerializer3(serializers.ModelSerializer):
    class Meta:
        model= models.Publisher
        fields = ['id','accepts_cbd', 'cta_copy_length', 'editorial_copy_length', 'days_in_advance', 'average_age', 'hhi', 'audience_geo', 'mobile_vs_desktop', 'education_level']

class PubSerializer4(serializers.ModelSerializer):
    class Meta:
        model= models.Publisher
        fields = ['id','professional_level', 'media_kit', 'files' ]

class PubSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Publisher
        fields = '__all__'

class PlacementSerializer(serializers.ModelSerializer):
    user= serializers.ReadOnlyField(source='user.id')
    class Meta:
        model= models.Placement
        # fields = '__all__'
        exclude = ['available']
        read_only_fields = ['user']
    def create(self, validated_data):
        user= self.context['request'].user
        placement = models.Placement.objects.create(user=user, **validated_data)
        return placement

class AdvSerializer1(serializers.ModelSerializer):
    class Meta:
        model= models.Ad
        fields = ['id','ad_name', 'ad_title', 'landing_page', 'utm_structure', 'target_matrics', 'utm_parameters' ]
        # read_only_fields = ['user']

class AdvSerializer2(serializers.ModelSerializer):
    class Meta:
        model= models.Advertiser
        fields = ['id','email', 'invoicing_contact', 'invoicing_email', 'invoice_mailing_address', 'primary_contact','additional_contact','legal_disclaimer' ]

class AdvSerializer3(serializers.ModelSerializer):
    class Meta:
        model= models.Advertiser
        fields = ['id','promo_code', 'value_propositoins', 'apart_competitors', 'focus_product', 'barrier_purchase', 'not_mention', 'success_msg']

class AdvSerializer4(serializers.ModelSerializer):
    class Meta:
        model= models.Advertiser
        fields = ['id','high_reslution_logo', 'files']

class AdvSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Advertiser
        fields = '__all__'

class ImageSerializer(serializers.ModelSerializer):
    # campaign = CampaignSerializer(read_only=True)
    class Meta:
        model = models.Image
        fields = '__all__'
        read_only_fields = ['ad']

class AdsSerializer(serializers.ModelSerializer):
    image = ImageSerializer( required=False)
    user= serializers.ReadOnlyField(source='user.id')
    class Meta:
        model= models.Ad
        fields = ['id', 'user','ad_name','ad_title','landing_page','utm_structure','target_matrics','utm_parameters','placement_types','target_market','daily_budget','total_budget','description','ad_goal',"image"]
        # exclude = ['available']
        read_only_fields = ['user']
    def create(self, validated_data):
        images_data = validated_data.pop('image')
        user= self.context['request'].user
        ad = models.Ad.objects.create(user=user, **validated_data)
        # for image_data in images_data:
        models.Image.objects.create(ad=ad, **images_data)
        return ad
    def update(self, instance, validated_data):
        images_data = validated_data.pop('image')
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        # instance.title = validated_data.get('title', instance.title)
        # instance.description = validated_data.get('description', instance.description)
        # instance.save()

        # Update or create new images
        # for image_data in images_data:
        #     image_id = image_data.get('id', None)
        #     if image_id:
        #         image = models.Image.objects.get(id=image_id, ad=instance)
        #         image.image = image_data.get('image', image.image)
        #         # image.caption = image_data.get('caption', image.caption)
        #         image.save()
        #     else:
        models.Image.objects.filter(ad=instance).delete()
        models.Image.objects.create(ad=instance, **images_data)
        return instance
        
class CampaignSerializer(serializers.ModelSerializer):
    placement = PlacementSerializer()
    ad = AdsSerializer()
    class Meta:
        model= models.Campaign
        fields = '__all__'
    def __init__(self, *args, **kwargs):
        super(CampaignSerializer, self).__init__(*args, **kwargs)
        # Filter placements to show only available ones
        self.fields['placement'].queryset = models.Placement.objects.filter(available=True)
        # Filter ads to show only available ones
        self.fields['ad'].queryset = models.Ad.objects.filter(available=True)

    def create(self, validated_data):
        placement = validated_data['placement']
        ad = validated_data['ad']

        # Set available to False for selected placement and ad
        placement.available = False
        placement.save()
        ad.available = False
        ad.save()

        return super().create(validated_data)

class CampaignDetailSerializer(serializers.ModelSerializer):

    placement = PlacementSerializer()
    ad = AdsSerializer()
    class Meta:
        model = models.Campaign
        fields ='__all__'

class ShotsSerializer(serializers.ModelSerializer):
    # campaign = CampaignSerializer(read_only=True)
    class Meta:
        model = models.Screenshot
        fields = '__all__'
        read_only_fields = ['campaign']

class CampImageSerializer(serializers.ModelSerializer):
    # campaign = CampaignSerializer(read_only=True)
    class Meta:
        model = models.CampaignImage
        fields = '__all__'
        read_only_fields = ['campaign']

class CampVideoSerializer(serializers.ModelSerializer):
    # campaign = CampaignSerializer(read_only=True)
    class Meta:
        model = models.CampaignVideo
        fields = '__all__'
        read_only_fields = ['campaign']

class CampFileSerializer(serializers.ModelSerializer):
    # campaign = CampaignSerializer(read_only=True)
    class Meta:
        model = models.CampaignFile
        fields = '__all__'
        read_only_fields = ['campaign']

