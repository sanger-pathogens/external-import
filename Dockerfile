FROM ubuntu:18.04
WORKDIR /opt

ARG TAG
ARG EXTERNAL_IMPORT_BUILD_DIR=/external-import
ARG ENA_BROWSER_TOOLS_VERSION=1.5.4

RUN apt update -qq -y && \
    apt upgrade -qq -y && \
    apt install -y \
    python3 \ 
    python3-setuptools \
    python3-pip \
    wget
    
#Install pandas
RUN pip3 install pandas
RUN pip3 install testfixtures

#Install enaBrowserTools
RUN wget https://github.com/enasequence/enaBrowserTools/archive/v${ENA_BROWSER_TOOLS_VERSION}.tar.gz \
        && tar -xzf v${ENA_BROWSER_TOOLS_VERSION}.tar.gz \
        && rm v${ENA_BROWSER_TOOLS_VERSION}.tar.gz \
	&& ln -sf /opt/enaBrowserTools-1.5.4/python3/* /usr/local/bin

# Install external-import
RUN mkdir -p $EXTERNAL_IMPORT_BUILD_DIR
COPY . $EXTERNAL_IMPORT_BUILD_DIR
RUN cd $EXTERNAL_IMPORT_BUILD_DIR \
    && python3 setup.py clean --all \
    && python3 setup.py test \
    && python3 setup.py install \ 
    && ln -sf $EXTERNAL_IMPORT_BUILD_DIR/importer /usr/local/bin
