from rest_framework import pagination


class CursorPagination(pagination.CursorPagination):
    cursor_query_param = 'created_at'
    ordering = '-created_at'


class ViewLimitOffsetPagination:
    paginator = pagination.LimitOffsetPagination()

    @classmethod
    def get_paginated_response(cls, request, queryset, serializer, context={}):
        paginated_queryset = cls.paginator.paginate_queryset(queryset=queryset, request=request)
        serializer_data = serializer(paginated_queryset, many=True, context=context).data

        return cls.paginator.get_paginated_response(serializer_data)
