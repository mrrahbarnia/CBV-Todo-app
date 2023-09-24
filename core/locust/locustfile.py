from locust import HttpUser, task

class QuickstartUser(HttpUser):
    
    def on_start(self):
        response = self.client.post('accounts/api/v1/jwt/create/',data={
            "username": "toktam75",
            "password": "To13431344"
        }).json()
        self.client.headers = {'Authorization':f"Bearer {response.get('access',None)}"}

    @task
    def task_list(self):
        self.client.get('api/v1/todo')