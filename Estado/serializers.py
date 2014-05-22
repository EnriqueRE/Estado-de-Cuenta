__author__ = 'enriqueramirez'
from rest_framework import serializers
from models import MonederoUser, AccountStatement


class AccountSerializer (serializers.ModelSerializer):
     class Meta:
          model = AccountStatement
          fields = ('statement_id', 'statement_student', 'statement_date', 'statement_tuition',
                    'statement_insurance', 'statement_diverse_services')


class UserSerializer (serializers.ModelSerializer):
     class Meta:
          model = MonederoUser
          fields = ('student_id', 'student_name', 'student_middle_name', 'student_lastname',
                    'student_second_lastname', 'student_badge_id', 'student_email')
