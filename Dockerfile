FROM python:3.12-alpine

RUN apk add --no-cache kubectl helm docker-cli docker-compose
COPY . /tmp
RUN pip install /tmp && rm -r /tmp
WORKDIR /work
ENV KUBECONFIG=/work/.kube/config
ENTRYPOINT [ "kube-compose" ]
