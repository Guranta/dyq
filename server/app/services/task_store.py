from app.models.generate import TaskRecord


class TaskStore:
    def __init__(self) -> None:
        self._tasks: dict[str, TaskRecord] = {}

    def save(self, task: TaskRecord) -> None:
        self._tasks[task.id] = task

    def get(self, task_id: str) -> TaskRecord | None:
        return self._tasks.get(task_id)


task_store = TaskStore()
