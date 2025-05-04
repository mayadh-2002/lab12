from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=50, default='')
    author = models.CharField(max_length=50, default='')
    price = models.FloatField(default=0.0)
    edition = models.SmallIntegerField(default=1)
    
class Address(models.Model):
    city = models.CharField(max_length=100)


class Student(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    addresses = models.ManyToManyField(Address)


class Card(models.Model):
    card_number = models.IntegerField()



class Department(models.Model):
    name = models.CharField(max_length=100)

class Course(models.Model):
     title = models.CharField(max_length=100)
     code = models.IntegerField()

    

class Student1(models.Model):
    name = models.CharField(max_length=100)
    card = models.OneToOneField(Card, on_delete=models.PROTECT, null=True, blank=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True, blank=True)
    courses = models.ManyToManyField(Course)

class Profile(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='profiles/', blank=True, null=True)  # Store images in 'profiles/' directory
    bio = models.TextField()