FROM amazonlinux:latest
RUN yum -y install which unzip aws-cli
ADD remote_cmd.sh /usr/local/bin/remote_job.sh
WORKDIR /tmp
USER nobody
ENTRYPOINT ["/usr/local/bin/remote_cmd.sh"]
