# -*- coding: utf-8 -*-
from __future__ import unicode_literals


from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import BasicAuthentication
from rest_framework.views import APIView
from rest_framework import generics, status
from rest_framework.response import Response

from rest_framework_simplejwt.tokens import RefreshToken


class ObtainTokenView(APIView):
    authentication_classes = (BasicAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        return self.post(request)

    def post(self, request):
        user = request.user
        refresh = RefreshToken.for_user(user)
        token = str(refresh.access_token)
        response = Response({"token": token}, status=status.HTTP_200_OK)
        response.set_cookie(key="token", value=token, httponly=False, max_age=60*60, secure=False, samesite="Strict")
        return response
