from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class ShipmentsPagination(PageNumberPagination):

    def get_paginated_response(self, data):
        return Response({
            'pager': {
                'next': self.page.next_page_number() if self.page.has_next() else None,
                'previous': self.page.previous_page_number() if self.page.has_previous() else None
            },
            'count': self.page.paginator.count,
            'results': data
        })

    def paginate_queryset(self, queryset, request, *args, **kwargs):
        if 'no_page' in request.query_params:
            return None
        return super().paginate_queryset(queryset, request, *args, **kwargs)