from django.contrib import admin
from models import MonederoUser, AccountStatement

# Register your models here.

# admin.site.register (MonederoUser)

class MonederoUserAdmin (admin.ModelAdmin):
     fields = [
          'student_id',
          'student_name',
          'student_middle_name',
          'student_lastname',
          'student_second_lastname',
          'student_badge_id',
          'student_email'
     ]
     list_display = ('student_id', 'student_name', 'student_lastname', 'student_email')


class StatementAdmin (admin.ModelAdmin):
     fields = [
          # 'statement_id',
          'statement_date',
          'statement_student',
          'statement_tuition',
	  'statement_interests',
          'statement_positive_balance',
          'statement_insurance',
          'statement_diverse_services',
     ]
     list_display = ('statement_date','statement_student')
     list_filter = ['statement_date']


admin.site.register (MonederoUser, MonederoUserAdmin)
admin.site.register (AccountStatement, StatementAdmin)
