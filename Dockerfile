FROM alpine as platform-base
RUN apk update q
RUN apk add build-base git vim curl sqlite
WORKDIR /opt/src
COPY . .
RUN git config --global --add safe.directory /opt/src


FROM platform-base as app-api
RUN apk add python3 python3-dev py3-pip
RUN cd api && pip install -U pip
RUN cd api && pip install --ignore-installed -e .
CMD cd api && flask --app mnaccounts run --host ${HOSTNAME}


FROM platform-base as app-static
RUN apk add nodejs npm
#RUN cat /etc/ssl/openssl.cnf
ENV NODE_OPTIONS --openssl-legacy-provider
RUN cd static && npm install
RUN cd static && npm run build
CMD cd static && npm start
