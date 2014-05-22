from macerrors import requiredFlagsDontMatch
from django.db import models

# Create your models here.

class AccountStatement (models.Model):
     class Meta:
          ordering = ['-statement_date', 'statement_student']
          # get_latest_by = 'statement_student'

     statement_id = models.AutoField (primary_key=True)
     statement_date = models.DateField ()
     statement_student = models.ForeignKey ('MonederoUser')
     statement_tuition = models.FloatField ()
     statement_positive_balance = models.FloatField ()
     statement_insurance = models.FloatField ()
     statement_diverse_services = models.FloatField ()


class MonederoUser (models.Model):
     student_id = models.CharField (primary_key=True, max_length=10)
     student_name = models.CharField (max_length=200)
     student_middle_name = models.CharField (max_length=200, blank=True)
     student_lastname = models.CharField (max_length=200)
     student_second_lastname = models.CharField (max_length=200, blank=True)
     student_badge_id = models.CharField (max_length=10, blank=True)
     student_email = models.CharField (max_length=200, blank=True)

     def __unicode__ (self):
          return self.student_id
