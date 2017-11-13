FROM python:2.7-slim
MAINTAINER "EEA: IDM2 C-TEAM" <eea-edw-c-team-alerts@googlegroups.com>

ENV WORK_DIR=/var/local/bdr.registry.notifications

RUN runDeps="curl vim build-essential netcat mysql-client libmysqlclient-dev" \
 && apt-get update \
 && apt-get install -y --no-install-recommends $runDeps \
 && rm -vrf /var/lib/apt/lists/*

RUN mkdir -p $WORK_DIR
COPY . $WORK_DIR/
WORKDIR $WORK_DIR

RUN pip install -r requirements-docker.txt

ENTRYPOINT ["./docker-entrypoint.sh"]
