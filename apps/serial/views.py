from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.pagination import PageNumberPagination

from .models import Task
from .serializers import TaskSerializer


class TaskView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request):
        tasks = Task.objects.all()

        # Фильтрация по title
        title = request.query_params.get('title')
        if title:
            tasks = tasks.filter(title__icontains=title)

        # Поиск по title и description
        search = request.query_params.get('search')
        if search:
            from django.db.models import Q

            tasks = tasks.filter(
                Q(title__icontains=search) |
                Q(description__icontains=search)
            )

        # Пагинация
        paginator = PageNumberPagination()
        paginator.page_size = 5

        page = paginator.paginate_queryset(tasks, request)

        serializer = TaskSerializer(page, many=True)

        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        serializer = TaskSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )
    