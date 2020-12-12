FROM centos

WORKDIR /usr/app

COPY . .


RUN yum -y update && yum -y install python38 && yum -y install java-11-openjdk.x86_64

RUN ln -s /usr/bin/python3 /usr/bin/python && ln -s /usr/bin/pip3 /usr/bin/pip && pip install numpy

ENTRYPOINT ["/bin/bash", "/usr/app/runApp.sh"]
