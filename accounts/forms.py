from django import forms
from .models import User,UserProfile
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from .validation import allow_only_images
class UserForm(forms.ModelForm):
    password=forms.CharField(max_length=50, widget=forms.PasswordInput)
    confirm_password=forms.CharField(max_length=50, widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['first_name','last_name','username','phone_number','email']


        #clean method is used to validate and clean the form data.
        # It is called after the form is submitted and before the data is saved.
        # The clean() method takes no arguments and returns a dictionary of cleaned data
    def clean(self):
        cleaned_data=super().clean()

        # print('cleaned_data:',cleaned_data)
        # cleaned_data:
        #         {
        #     'first_name': 'Ahmed Rachid',
        #      'last_name': 'BACHIR',
        #      'username': 'ahmed',
        #      'phone_number': '659054196',
        #      'email': 'a_bachir@enst.dz',
        #      'password': 'd',
        #      'confirm_password': 'd'
        #        }

        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError(
                "Passwords do not match"
            )

class UserProfileForm(forms.ModelForm):
    profile_picture=forms.FileField(validators=[allow_only_images],widget=forms.FileInput(attrs={'class': 'btn btn-info'},))
    cover_picture=forms.FileField(validators=[allow_only_images],widget=forms.FileInput(attrs={'class': 'btn btn-info'},))
    latitude=forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly'},))
    longitude=forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly'},))
    class Meta:
        model = UserProfile
        exclude = ['user']




        





        