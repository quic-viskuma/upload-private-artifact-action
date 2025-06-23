FROM public.ecr.aws/docker/library/alpine:3.21

RUN apk add python3 py3-requests

COPY publish_artifacts.py /
ENTRYPOINT ["/publish_artifacts.py"]
