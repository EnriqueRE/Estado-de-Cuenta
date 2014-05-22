import django_filters
from django.contrib.auth.models import User
from rest_framework import filters
from rest_framework import renderers
from rest_framework import permissions
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from rest_framework import viewsets
from django.views.generic import TemplateView
from django.shortcuts import render
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from models import MonederoUser, AccountStatement
from serializers import UserSerializer, AccountSerializer

# Create your views here.


#Filters
class StatementFilter (django_filters.FilterSet):
     max_date = django_filters.DateTimeFilter (name='statement_date', lookup_type='lte')
     min_date = django_filters.DateTimeFilter (name='statement_date', lookup_type='gte')
     username = django_filters.CharFilter (name='statement_student',
                                           lookup_type='student_id')

     class Meta:
          model = AccountStatement
          fields = ['statement_student', 'statement_id']


#ViewSets
class UserViewSet (viewsets.ModelViewSet):
     """
     API endpoint that allows monederoUsers to be viewed or edited
     """
     queryset = MonederoUser.objects.all ()
     serializer_class = UserSerializer
     permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class StatementViewSet (viewsets.ModelViewSet):
     queryset = AccountStatement.objects.all ()
     serializer_class = AccountSerializer
     permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class StatementSearch (generics.ListCreateAPIView):
     queryset = AccountStatement.objects.all ()
     filter_class = StatementFilter
     serializer_class = AccountSerializer
     permission_classes = (permissions.IsAuthenticatedOrReadOnly,)