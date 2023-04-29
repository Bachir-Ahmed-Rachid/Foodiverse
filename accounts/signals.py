from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User,UserProfile
@receiver(post_save,sender=User)
def post_save_create_profile_receiver(sender,instance,created,**kwargs):   #The post_save_create_profile_receiver function accepts sender, instance, and created arguments because those arguments are passed automatically by the Django signal framework when the signal is triggered
    if created:
        #if we create a new instance of User model we have to create user profile automatically and give it the instance
        UserProfile.objects.create(user=instance)
    else:
        try:
            profile=UserProfile.objects.get(user=instance)
            profile.save()
        except:
            UserProfile.objects.create(user=instance)
            print('user was not found but created one')