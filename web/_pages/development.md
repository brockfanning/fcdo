---
title: Countries by status of development
permalink: /development
layout: single
---
{% assign statuses = '' | split: '' %}
{% for country in site.data.countries %}
{% unless statuses contains country.info.platform.status %}
    {% assign status = country.info.platform.status | split: '|' %}
    {% assign statuses = statuses | concat: status %}
{% endunless %}
{% endfor %}

{% assign statuses = statuses | sort %}
{% for status in statuses %}
<h3>{{ status }}</h3>
<ul>
    {% for country in site.data.countries %}
        {% if country.info.platform.status == status %}
        <li><a href="{{ site.baseurl }}/{{ country.slug }}">{{ country.name }}</a></li>
        {% endif %}
    {% endfor %}
</ul>
{% endfor %}
