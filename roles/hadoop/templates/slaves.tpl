{% for node in slaves %}
{{ hostvars[node].hostname }}
{% endfor %}