TASK:
Atlan Collect has a variety of long-running tasks that require time and resources on the servers. As it stands now, once we have triggered off a long-running task, there is no way to tap into it and pause/stop/terminate the task, upon realizing that an erroneous request went through from one of the clients (mostly web or pipeline).

We want to offer an implementation through which the user can now stop the long-running task at any given point in time, and can choose to resume or terminate it. This will ensure that the resources like compute/memory/storage/time are used efficiently at our end, and do not go into processing tasks that have already been stopped (and then to roll back the work done post the stop-action)

Create Rest API endpoints where the problem mentioned in the above three examples can be solved and package the solution in a docker image that can be deployed on Kubernetes directly.

SOLUTION:
Uploading the data in chunks and maintaining the state of upload can enable the user to pause the task in between and resume/terminate it. After terminating a task, a rollback is intiated.

There are two long running tasks:

1. Inserting into database.
2. Exporting from database to a csv file.

API description:

1. Database insertion:

   1. POST: /insert (body: {userID: id})
   2. POST: /insert/pause
   3. POST: /insert/resume
   4. POST: /insert/terminate
   5. GET: /insert/progress

2. Exporting
   1. POST: /export (body: {userID: id})
   2. POST: /export/pause
   3. POST: /export/resume
   4. POST: /export/terminate
   5. GET: /export/download
