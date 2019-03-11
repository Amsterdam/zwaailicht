FROM amsterdam/python
MAINTAINER datapunt@amsterdam.nl

ENV PYTHONUNBUFFERED 1

EXPOSE 8000

ARG https_proxy=http://10.240.2.1:8080/
ENV https_proxy=$https_proxy

RUN apt-get install -y \
		libgeos-dev \
		netcat \
	&& apt-get clean \
	&& rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* \
	&& adduser --system datapunt \
	&& mkdir -p /static \
	&& chown datapunt /static \
	&& pip install uwsgi

WORKDIR /app
COPY requirements.txt /app/
RUN pip install --cert /usr/local/share/ca-certificates/extras/adp_rootca.crt -r requirements.txt

USER datapunt
COPY zwaailicht /app/
CMD /app/docker-entrypoint.sh
