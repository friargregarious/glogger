from jinja2 import Template

mytemp = """this is a {{ test }} of my {{ template }}, please {{ action }}."""

context = {"test": "printjob", "template": "superpowers", "action": "disregard"}

output = Template(mytemp).render(**context)
print(mytemp)
print(output)