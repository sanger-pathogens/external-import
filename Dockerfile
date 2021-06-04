FROM ubuntu:18.04
WORKDIR /opt

ARG EXTERNAL_IMPORT_BUILD_DIR=external-import
ARG ENA_BROWSER_TOOLS_VERSION=1.6

RUN apt update -qq -y && \
    apt install -y \
    python3 \ 
    python3-setuptools \
    python3-pip \
    wget \
    && apt clean -y

#install requests library
RUN pip3 install requests

#Install enaBrowserTools
RUN wget https://github.com/enasequence/enaBrowserTools/archive/v${ENA_BROWSER_TOOLS_VERSION}.tar.gz \
        && tar -xzf v${ENA_BROWSER_TOOLS_VERSION}.tar.gz \
        && rm v${ENA_BROWSER_TOOLS_VERSION}.tar.gz
ENV PATH="/opt/enaBrowserTools-${ENA_BROWSER_TOOLS_VERSION}/python3:$PATH"

# Install external-import
RUN mkdir -p $EXTERNAL_IMPORT_BUILD_DIR
COPY . $EXTERNAL_IMPORT_BUILD_DIR
RUN cd $EXTERNAL_IMPORT_BUILD_DIR \
    && python3 setup.py test \
    && python3 setup.py install
