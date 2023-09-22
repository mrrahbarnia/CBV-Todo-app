from django.contrib.auth.models import User
from django.urls import reverse

from rest_framework.test import APIClient

import pytest


@pytest.fixture
def client():
    client = APIClient()
    return client


@pytest.fixture
def custom_user():
    user = User.objects.create(username="test", password="T13431344")
    return user


@pytest.mark.django_db
class TestTodoApi:
    def test_get_todo_response_200(self, client):
        url = reverse("todo-api:todo-list")
        response = client.get(url)
        assert response.status_code == 200

    def test_post_todo_unauthorized_response_401(self, client):
        url = reverse("todo-api:todo-list")
        response = client.post(url, data={"title": "test"})
        assert response.status_code == 401

    def test_post_todo_logedin_response_200(self, client, custom_user):
        url = reverse("todo-api:todo-list")
        client.force_authenticate(user=custom_user)
        response = client.post(url, data={"task": "test"})
        assert response.status_code == 201

    def test_post_todo_logein_invalid_data_response_400(self, client, custom_user):
        url = reverse("todo-api:todo-list")
        client.force_authenticate(user=custom_user)
        response = client.post(url, data={"task": ""})
        assert response.status_code == 400
