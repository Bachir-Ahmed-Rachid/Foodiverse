from django.core.exceptions import ValidationError
import os
def allow_only_images(value):
    extension=os.path.splitext(value.name)[1]
    valid_extension=['.png','.jpg','.jpeg']
    if not extension.lower() in valid_extension:
        raise ValidationError('unsupported file extension')