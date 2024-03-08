import uuid

from celery.result import AsyncResult

import app.tasks as task

input_token = "9762"

task_id = str(uuid.uuid4())
results = task.push_notification.apply_async(
    (input_token,),
    task_id=task_id,
)

t = task.push_notification.AsyncResult(task_id)
print(t.state)
print(t.id)
print(t.result)

print("########")
print(t.state)
print(t.id)
print(t.result)

print("########")
print(t.state)
print(t.id)
print(t.result)


print("########")
print(t.state)
print(t.id)
print(t.result)


print("########")
print(t.state)
print(t.id)
print(t.result)


print("########")
print(t.state)
print(t.id)
print(t.result)


print("########")
print(t.state)
print(t.id)
print(t.result)


print("########")
print(t.state)
print(t.id)
print(t.result)
