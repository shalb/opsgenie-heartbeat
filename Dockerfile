FROM python:3.7.1

RUN pip3 install prometheus_client
RUN pip3 install pyaml

COPY opsgenie_lamp/ /opt/opsgenie_lamp
COPY entrypoint/ /opt/entrypoint
RUN chmod -R u=rwX,g=rX,o=rX /opt/opsgenie_lamp/ /opt/entrypoint/
RUN chmod 755 /opt/opsgenie_lamp/lamp

RUN useradd -m -s /bin/bash my_user

USER my_user

ENTRYPOINT ["/usr/local/bin/python", "/opt/entrypoint/entrypoint.py"]
