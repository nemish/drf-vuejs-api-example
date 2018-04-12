# -*- coding: utf-8 -*-
from rest_framework.permissions import BasePermission


class IsCreationOrIsAuthenticated(BasePermission):

    def has_permission(self, request, view):
        return request.user.is_authenticated or view.action == 'create'
