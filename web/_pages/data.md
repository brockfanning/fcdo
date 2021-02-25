---
title: Countries by status of data
permalink: /data
layout: single
---
{% assign statuses = '' | split: '' %}
{% for country in site.data.countries %}
{% unless statuses contains country.info.data.status %}
    {% assign status = country.info.data.status | split: '|' %}
    {% assign statuses = statuses | concat: status %}
{% endunless %}
{% endfor %}

{% assign statuses = statuses | sort %}
{% for status in statuses %}
<h3>{{ status }}</h3>
<ul>
    {% for country in site.data.countries %}
        {% if country.info.data.status == status %}
        <li><a href="{{ site.baseurl }}/{{ country.slug }}">{{ country.name }}</a></li>
        {% endif %}
    {% endfor %}
</ul>
{% endfor %}
