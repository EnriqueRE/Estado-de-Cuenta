import datetime
from django.http import HttpResponse
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
from Estado.AuthenticationUtils import search_for_user, authenticate_user, \
    RESPONSE_DICTIONARY
from models import MonederoUser, AccountStatement
from serializers import UserSerializer, AccountSerializer

import base64

from functools import wraps

from django.http import HttpResponse
from django.contrib.auth import authenticate, login

# Create your views here.


# Filters
class StatementFilter(django_filters.FilterSet):
    max_date = django_filters.DateTimeFilter(name='statement_date',
                                             lookup_type='lte')
    min_date = django_filters.DateTimeFilter(name='statement_date',
                                             lookup_type='gte')
    username = django_filters.CharFilter(name='statement_student',
                                         lookup_type='student_id')

    class Meta:
        model = AccountStatement
        fields = ['statement_student', 'statement_id']


# ViewSets
class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows monederoUsers to be viewed or edited
    """
    queryset = MonederoUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class StatementViewSet(viewsets.ModelViewSet):
    queryset = AccountStatement.objects.all()
    serializer_class = AccountSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class StatementSearch(generics.ListCreateAPIView):
    queryset = AccountStatement.objects.all()
    filter_class = StatementFilter
    serializer_class = AccountSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


def checkUserInLdap (request):
    
    if request.META.has_key('HTTP_AUTHORIZATION'):
        authmeth, auth = request.META['HTTP_AUTHORIZATION'].split(' ', 1)
        if authmeth.lower() == 'basic':
            auth = auth.strip().decode('base64')
            username, password = auth.split(':', 1)

            print("%s %s") % (username, password)

    # Check if user exists
    message = ""
    user_email = username + '@itesm.mx'
    user_dn = search_for_user(user_email)
    response_from_ldap = []
    response_code = 0

    if user_dn.__len__() > 0:
        response_from_ldap = authenticate_user(user_email, user_dn, password)
        if response_from_ldap[0] == 1:
            response_code = response_from_ldap[0]
            message = response_from_ldap[1]
        else:
            response_code = response_from_ldap[0]
            message = response_from_ldap[1]
    else:
        response_code = 3
        message = [3, RESPONSE_DICTIONARY.get(3)]

    html = '{"code":%d,"message":"%s"}' % (response_code, message)
    return HttpResponse(html)