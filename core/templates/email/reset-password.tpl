{% extends "mail_templated/base.tpl" %}

{% block subject %}
Activation
{% endblock %}

{% block html %}
<h1>Hello {{user}}</h1>

<p>Please click on the link below to set a new password</p>
<a href="{{link}}">Click Here</a>


{% endblock %}