{% extends "mail_templated/base.tpl" %}

{% block subject %}
Activation
{% endblock %}

{% block html %}
<h1>Hello {{user}}</h1>
http://127.0.0.1:8000/accounts/api/v1/reset-password/{{token}}
{% endblock %}