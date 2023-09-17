{% extends "mail_templated/base.tpl" %}

{% block subject %}
Activation
{% endblock %}

{% block html %}
<h1>Hello {{user}}</h1>

<a href="{{current_site}}">Click Here</a>


{% endblock %}