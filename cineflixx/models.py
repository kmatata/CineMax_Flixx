from django.db import models
from PIL import Image

# Create your models here.
def poster_dir_path(instance, filename):
    imgageFile = filename.split('.')
    try:
        if (imgageFile[-1] == 'jpeg'):
            image_ext = '.jpeg'
        elif (imgageFile[-1] == 'png'):
            image_ext = '.png'
        elif (imgageFile[-1] == 'jpg'):
            image_ext = '.jpg'
        image_ext_name = 'posters/postImage{0}{1}'.format(instance.name,image_ext)
    except Exception as e:
        raise e
    
    return image_ext_name


class Movie(models.Model):
    name = models.CharField(max_length=100,unique=True)
    protagonists = models.CharField(max_length=100)    
    start_date = models.DateTimeField()
    status = models.CharField(max_length=20, choices=(
        ('coming-up', 'Coming Up'),
        ('starting', 'Starting'),
        ('running', 'Running'),
        ('finished', 'Finished')
    ), default='coming-up')
    ranking = models.IntegerField(default=0)
    poster = models.ImageField(upload_to=poster_dir_path,null=True,blank=True)
        
    def save(self,*args,**kwargs):        
        super().save(*args,**kwargs)        
        SIZE = 600,300
        if self.poster:
            img = Image.open(self.poster.path)
            img.thumbnail(size=(SIZE))
            img.save(self.poster.path,optimize=True,qulaity=90)

