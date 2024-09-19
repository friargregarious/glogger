# {{ title }}

VERSION: {{ version_number }} [{{ build_number }}]
DATE: {{ date }}
CONTRIBUTORS:

{% for contributor in contributors %} * {{ contributor }} {% endfor %}

{% for artifact_type, artifacts in changes %}

## {{ artifact_type }}

{% for artifact in artifacts %} * {{ artifact }} {% endfor %}
{% endfor %}