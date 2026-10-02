from django.shortcuts import render
from django.core.cache import cache
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Task
from .serializers import TaskSerializer

class TaskView(APIView):
    def get(self, request):
        tasks_data = cache.get("tasks")

        if tasks_data is not None:
            print("Взято из кэша")
            return Response(tasks_data)

        print("взят из базы данных кэшем")
        tasks = Task.objects.all()
        serializer = TaskSerializer(tasks,  many=True)
        tasks_data = serializer.data

        cache.set("tasks", tasks_data, 60)

        return Response(tasks_data)

        
        # data = TaskSerializer(Task.objects.all(), many=True).data
        # return Response(data)

    def post(self, request):
        serializer = TaskSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        cache.delete("tasks")

        return Response(serializer.data, status = status.HTTP_201_CREATED)

    