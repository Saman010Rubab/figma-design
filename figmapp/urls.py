from django.urls import path
from . import views


urlpatterns=[
    # path("", views.UserList.as_view(), name = "user"),
    path('user/', views.UserList.as_view(), name = "user"),
    path("user/<int:pk>/", views.UserDetail.as_view(), name = "userdetail"),
    path("login/", views.UserLoginView.as_view(), name = "login"),
    path("profile/", views.ProfileList.as_view(), name = "profile"),
    path("profile/<int:pk>/", views.ProfileDetail.as_view(), name = "profiledetail"),
    path("profileupdate/<int:pk>/", views.ProfileUpdate.as_view(), name = "profileupdate"),
    path("campaigns/", views.CampaignList.as_view(), name = "campaigns"),
    path("campaigns/<int:pk>/", views.CampaignDetail.as_view(), name = "campaignsdetail"),



#  publisher
    path('pubstep1/<int:pk>/', views.PubStep1.as_view(), name='PubStep1'),
    path('pubstep2/<int:pk>/', views.PubStep2.as_view(), name='PubStep2'),
    path('pubstep3/<int:pk>/', views.PubStep3.as_view(), name='PubStep3'),
    path('pubstep4/<int:pk>/', views.PubStep4.as_view(), name='PubStep4'),
    path("placements/", views.PlacementsCreate.as_view(), name = "placements"),
    path("placements/<int:pk>/", views.PlacementsUpdate.as_view(), name = "placementsupdate"),
    path("campaigns/<int:campaign_id>/screenshot/", views.ShotsView.as_view(), name = "screenshot"),



#  advertiser
    path('advstep1/<int:pk>/', views.AdvStep1.as_view(), name='AdvStep1'),
    path('advstep2/<int:pk>/', views.AdvStep2.as_view(), name='AdvStep2'),
    path('advstep3/<int:pk>/', views.AdvStep3.as_view(), name='AdvStep3'),
    path('advstep4/<int:pk>/', views.AdvStep4.as_view(), name='AdvStep4'),
    path("ads/", views.AdsCreate.as_view(), name = "ads"),
    path("ads/<int:pk>/", views.AdsUpdate.as_view(), name = "adsupdate"),
    path("ads/<int:ad_id>/image/", views.ImageView.as_view(), name = "images"),




# admin
    path("publishers/", views.PublisherList.as_view(), name = "publishers"),
    path("placementsdetail/", views.PlacementsList.as_view(), name = "placementsdetail"),
    path("placementsdetail/<int:pk>/", views.PlacementsDetail.as_view(), name = "placementdetail"),



    path("advertisers/", views.AdvertiserList.as_view(), name = "advertisers"),
    path("adsdetail/", views.AdsList.as_view(), name = "adsdetail"),
    path("adsdetail/<int:pk>/", views.AdsDetail.as_view(), name = "addetail"),


    path("newcampaign/", views.CampaignView.as_view(), name = "newcampaign"),








]