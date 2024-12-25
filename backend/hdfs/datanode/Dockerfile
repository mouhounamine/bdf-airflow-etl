FROM apache/hadoop:3.3.5

USER root
ENV HADOOP_HOME=/opt/hadoop

COPY ./init-datanode.sh /init-datanode.sh

WORKDIR /opt/hadoop

CMD ["/bin/bash", "/init-datanode.sh"]
