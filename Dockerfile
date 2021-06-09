FROM python:3.8.6

RUN pip install \
	pandas==1.1.3

COPY bin/* /usr/local/bin/
RUN chmod a+x /usr/local/bin/*

LABEL maintainer="Xindi Guo <xindi.guo@sagebase.org>"
LABEL base_image="python:3.8.6"
LABEL about.summary="Docker image for add_missing_ntc.py script"
LABEL about.license="SPDX:Apache-2.0"
