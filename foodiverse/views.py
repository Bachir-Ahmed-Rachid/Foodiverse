from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.db.models.functions import Distance #used to calculate distance
from django.contrib.gis.measure import D
from vendors.models import Vendor


def get_or_set_lat_long(request):
      if 'lat' in request.session:
          lat=request.session['lat']
          long=request.session['long']
          return long,lat
      elif 'lat' in request.GET:
          lat=request.GET['lat']
          long=request.GET['long'] 
          request.session['long']=long
          request.session['lat']=lat
          return long,lat     
      else:
           return None
          
def home(request):
     if get_or_set_lat_long(request) is not None:
          long,lat=get_or_set_lat_long(request)
           # Define the reference point with latitude and longitude
          reference_point = GEOSGeometry(f'POINT({long} {lat})')  # Example reference point (New York City coordinates)
            # Perform the radius filter on your model 
          vendors=Vendor.objects.filter(is_approved=True,user__is_active=True,
            #in annotate we dd a new field called distance that use Distance function to calculate the distance between reference point and the location of vendor
          user_profile__location__distance_lte=(reference_point,D(km=1000))).annotate(distance=Distance(reference_point,'user_profile__location')).order_by('distance')
     else:
          vendors=Vendor.objects.filter(user__is_active=True,is_approved=True)[:8]
     context={
          'vendors':vendors
     }
     return render(request,'home.html',context)
def test_map(request):
     return render(request,'test_map.html')
