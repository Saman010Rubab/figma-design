from . import serializers
from . import models
from .permissions import IsAdmin, IsPublisher, IsAdvertiser, IsOwner
from rest_framework import generics
from rest_framework.permissions import IsAdminUser, AllowAny, IsAuthenticated, OR
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate,login

# user signup
class UserList(generics.ListCreateAPIView):
    queryset = models.User.objects.all()
    serializer_class = serializers.UserSerializer
    permission_classes = [AllowAny]

class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.User.objects.all()
    serializer_class = serializers.UserSerializer
    permission_classes = [IsAuthenticated]

# user login
class UserLoginView(APIView):
    serializer_class = serializers.UserLoginSerializer
    permission_classes = (AllowAny, )
    def post(self, request):
        serializer = serializers.UserLoginSerializer(data=request.data)
        data = request.data
        # if serializer.is_valid(raise_exception=True):
        user = authenticate(request, email=data['email'], password=data['password'])
        if user:
            login(request, user)
            return Response( {'success': True,
                'message': 'User logged in successfully',
                'email': data['email'],
                },
                status=status.HTTP_200_OK)
        else:
            return Response({"error": "Wrong username/password"}, status=status.HTTP_401_UNAUTHORIZED)
    
class ProfileList(generics.ListAPIView):
    queryset = models.Profile.objects.all()
    serializer_class = serializers.ProfileSerializer
    permission_classes = [IsAuthenticated, IsAdmin]

class ProfileDetail(generics.RetrieveAPIView):
    queryset = models.Profile.objects.all()
    serializer_class = serializers.ProfileSerializer
    permission_classes = [IsAuthenticated, IsAdmin]

class ProfileUpdate(generics.RetrieveUpdateAPIView):
    queryset = models.Profile.objects.all()
    serializer_class = serializers.ProfileSerializer
    permission_classes = [IsAuthenticated, IsOwner]

class CampaignList(generics.ListAPIView):
    # queryset = models.Campaign.objects.all()
    serializer_class = serializers.CampaignSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user= self.request.user
        # Filter to only show available placements and ads
        if user.role == 2:
            return models.Campaign.objects.filter(
                placement__user=user
            )
        elif user.role == 3:
            return models.Campaign.objects.filter(
                ad__user=user
            )

class CampaignDetail(generics.RetrieveAPIView):
    queryset = models.Campaign.objects.all()
    serializer_class = serializers.CampaignDetailSerializer
    permission_classes = [IsAuthenticated]

# publisher features

class PubStep1(generics.RetrieveUpdateAPIView):
    queryset = models.Publisher.objects.all()
    serializer_class = serializers.PubSerializer1
    permission_classes = [AllowAny]

class PubStep2(generics.RetrieveUpdateAPIView):
    queryset = models.Placement.objects.all()
    serializer_class = serializers.PubSerializer2
    permission_classes = [AllowAny]

class PubStep3(generics.RetrieveUpdateAPIView):
    queryset = models.Publisher.objects.all()
    serializer_class = serializers.PubSerializer3
    permission_classes = [AllowAny]

class PubStep4(generics.RetrieveUpdateAPIView):
    queryset = models.Publisher.objects.all()
    serializer_class = serializers.PubSerializer4
    permission_classes = [AllowAny]
  
class PlacementsCreate(generics.ListCreateAPIView):
    serializer_class = serializers.PlacementSerializer
    permission_classes = [IsAuthenticated, IsPublisher]
    def get_queryset(self):
        user= self.request.user
        return models.Placement.objects.filter(user=user)

class PlacementsUpdate(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Placement.objects.all()
    serializer_class = serializers.PlacementSerializer
    permission_classes = [IsAuthenticated, IsOwner]

class ShotsView(generics.ListCreateAPIView):
    serializer_class = serializers.ShotsSerializer
    def get_queryset(self, *args, **kwargs):
        campaign = self.kwargs.get('campaign_id')
        return models.Screenshot.objects.filter(campaign=campaign)
    def perform_create(self, serializer):
        campaign_id = self.kwargs.get('campaign_id')
        campaign = models.Campaign.objects.get(pk=campaign_id)
        serializer.save(campaign=campaign)

# advertiser features
class AdvStep1(generics.RetrieveUpdateAPIView):
    queryset = models.Ads.objects.all()
    serializer_class = serializers.AdvSerializer1
    permission_classes = [AllowAny]

class AdvStep2(generics.RetrieveUpdateAPIView):
    queryset = models.Advertiser.objects.all()
    serializer_class = serializers.AdvSerializer2
    permission_classes = [AllowAny]

class AdvStep3(generics.RetrieveUpdateAPIView):
    queryset = models.Advertiser.objects.all()
    serializer_class = serializers.AdvSerializer3
    permission_classes = [AllowAny]

class AdvStep4(generics.RetrieveUpdateAPIView):
    queryset = models.Advertiser.objects.all()
    serializer_class = serializers.AdvSerializer4
    permission_classes = [AllowAny]

class AdsCreate(generics.ListCreateAPIView):
    serializer_class = serializers.AdsSerializer
    permission_classes = [IsAuthenticated,IsAdvertiser]
    def get_queryset(self):
        user= self.request.user
        return models.Ads.objects.filter(user=user)

class AdsUpdate(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Ads.objects.all()
    serializer_class = serializers.AdsSerializer
    permission_classes = [IsAuthenticated, IsOwner]

class ImageView(generics.ListCreateAPIView):
    serializer_class = serializers.ImageSerializer
    def get_queryset(self, *args, **kwargs):
        ad = self.kwargs.get('ad_id')
        return models.Image.objects.filter(ad=ad)
    def perform_create(self, serializer):
        ad_id = self.kwargs.get('ad_id')
        ad = models.Ads.objects.get(pk=ad_id)
        serializer.save(ad=ad)

# admin features

class PublisherList(generics.ListAPIView):
    queryset = models.Publisher.objects.all()
    serializer_class = serializers.PubSerializer
    permission_classes = [IsAuthenticated,IsAdmin ]

class PlacementsList(generics.ListAPIView):
    queryset = models.Placement.objects.all()
    serializer_class = serializers.PlacementSerializer
    permission_classes = [IsAuthenticated, IsAdmin]

class PlacementsDetail(generics.RetrieveAPIView):
    queryset = models.Placement.objects.all()
    serializer_class = serializers.PlacementSerializer
    permission_classes = [IsAuthenticated, IsAdmin]

class AdvertiserList(generics.ListAPIView):
    queryset = models.Advertiser.objects.all()
    serializer_class = serializers.AdvSerializer
    permission_classes = [IsAuthenticated, IsAdmin]
    
class AdsList(generics.ListAPIView):
    queryset = models.Ads.objects.all()
    serializer_class = serializers.AdsSerializer
    permission_classes = [IsAuthenticated,IsAdmin]

class AdsDetail(generics.RetrieveAPIView):
    queryset = models.Ads.objects.all()
    serializer_class = serializers.AdsSerializer
    permission_classes = [IsAuthenticated, IsAdmin]

class CampaignView(generics.ListCreateAPIView):
    queryset = models.Campaign.objects.all()
    serializer_class = serializers.CampaignSerializer
    permission_classes = [IsAuthenticated, IsAdmin]


