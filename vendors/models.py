from django.db import models
from accounts.models import User,UserProfile
from accounts.utils import send_approval_notification
# Create your models here.
class Vendor(models.Model):
    user=models.OneToOneField(User,related_name='user', on_delete=models.CASCADE)
    user_profile=models.OneToOneField(UserProfile,related_name='user_profile', on_delete=models.CASCADE)
    vendor_name=models.CharField(max_length=50,unique=True)
    vendor_licence=models.ImageField(upload_to='vendor/licences')
    is_approved=models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.vendor_name
    
    ##save method is triggered every time we save our model

    def save(self,*args, **kwargs):
        ## verify if an instance of the vendor model exist or no?
        if self.pk is not None:##(this vendor exist already)
            ## we have to find the original "is_approved" state and see if it has been changed or no
            original_state=Vendor.objects.get(pk=self.pk)
            if original_state.is_approved != self.is_approved :
                #We have 2 case here(the originale was false and the new is true or the opposite)
                mail_template='accounts/emails/admin_approval_email.html'
                mail_subject='Update of your restaurant approval state'
                context={
                    'user':self.user,
                    'is_approved':self.is_approved
                }
                if self.is_approved == True:
                    send_approval_notification(mail_subject,mail_template,context)
                else:
                    send_approval_notification(mail_subject,mail_template,context)
        return super(Vendor,self).save(*args, **kwargs)
                
                

