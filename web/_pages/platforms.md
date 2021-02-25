---
title: Countries by platform
permalink: /platforms
layout: single
---
{% assign platforms = '' | split: '' %}
{% for country in site.data.countries %}
{% unless platforms contains country.info.platform.system %}
    {% assign platform = country.info.platform.system | split: '|' %}
    {% assign platforms = platforms | concat: platform %}
{% endunless %}
{% endfor %}

{% assign platforms = platforms | sort %}
{% for platform in platforms %}
<h3>{{ platform }}</h3>
<ul>
    {% for country in site.data.countries %}
        {% if country.info.platform.system == platform %}
        <li><a href="{{ site.baseurl }}/{{ country.slug }}">{{ country.name }}</a></li>
        {% endif %}
    {% endfor %}
</ul>
{% endfor %}
