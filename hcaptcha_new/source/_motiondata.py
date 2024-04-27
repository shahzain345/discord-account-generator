import httpx


def get_data():
    task_id = httpx.get("http://localhost:5435/get_captcha").json()["taskId"]
    status = "PENDING"
    while status == "PENDING":
        resp = httpx.get(f"http://localhost:5435/get_captcha/resp/{task_id}").json()
        return resp["task"]["value"]


def get_submit():
    task_id = httpx.get("http://localhost:5435/submit_cap").json()["taskId"]
    status = "PENDING"
    while status == "PENDING":
        resp = httpx.get(f"http://localhost:5435/submit_cap/resp/{task_id}").json()
        return resp["task"]["value"]
