from Interface_TestPlatform.celery import app


@app.task
def hello_world():
    a = "sdf"
    return a
