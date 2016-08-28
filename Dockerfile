FROM ubuntu:14.04
MAINTAINER euclid1990

RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
    apt-utils \
    apt-transport-https \
    ca-certificates \
    software-properties-common \
    net-tools \
    openssh-server \
    python-simplejson \
    python-pip \
    zip \
    vim

RUN apt-add-repository ppa:ansible/ansible
RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends ansible

RUN mkdir /var/run/sshd && mkdir -p /root/.ssh/

COPY ./ansible.cfg /etc/ansible/ansible.cfg

COPY ./entrypoint.py /scripts/entrypoint.py

ENTRYPOINT ["python", "/scripts/entrypoint.py"]