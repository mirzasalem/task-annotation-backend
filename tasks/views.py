from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Task
from .serializers import TaskSerializer


class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer

    def get_queryset(self):
        queryset = Task.objects.filter(user=self.request.user)
        scheduled_date = self.request.query_params.get("scheduled_date")
        if scheduled_date:
            queryset = queryset.filter(scheduled_date=scheduled_date)
        return queryset

    @action(detail=False, methods=["post"])
    def reorder(self, request):
        """Bulk update task status and order after drag-and-drop."""
        items = request.data.get("items", [])
        if not isinstance(items, list):
            return Response(
                {"error": "items must be a list"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        task_ids = [item.get("id") for item in items if item.get("id")]
        tasks = {
            t.id: t
            for t in Task.objects.filter(user=request.user, id__in=task_ids)
        }

        updated = []
        for item in items:
            task_id = item.get("id")
            if task_id not in tasks:
                continue
            task = tasks[task_id]
            task.status = item.get("status", task.status)
            task.order = item.get("order", task.order)
            task.save(update_fields=["status", "order", "updated_at"])
            updated.append(task)

        serializer = TaskSerializer(updated, many=True)
        return Response(serializer.data)
