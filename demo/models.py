from django.db import models

class Student(models.Model):
    stuNumber = models.IntegerField(null=True)
    stuName = models.CharField(max_length=20,null=True)

class Kem(models.Model):
    kname = models.CharField(max_length=120)

class Term(models.Model):
    tname = models.CharField(max_length=50)

class Chj(models.Model):
    cj = models.CharField(max_length=50)
    sid = models.ForeignKey(Student,on_delete=models.CASCADE)
    kid = models.ForeignKey(Kem, on_delete=models.CASCADE)
    tid = models.ForeignKey(Term,on_delete=models.CASCADE)
