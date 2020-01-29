FROM ubuntu:18.04
WORKDIR /opt

ARG TAG
ARG EXTERNAL_IMPORT_BUILD_DIR=/external-import

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

RUN ln -s -f /usr/bin/python3 /usr/local/bin/python

# Install external-import
RUN mkdir -p $EXTERNAL_IMPORT_BUILD_DIR
COPY . $EXTERNAL_IMPORT_BUILD_DIR
RUN cd $EXTERNAL_IMPORT_BUILD_DIR \
    && python3 setup.py clean --all \
    && python3 setup.py test \
    && python3 setup.py install \
    && ln -sf $EXTERNAL_IMPORT_BUILD_DIR/importer /usr/local/bin

#Install enaBrowserTools 
RUN wget https://github.com/enasequence/enaBrowserTools/archive/v1.5.4.tar.gz && \
	tar -xzf v1.5.4.tar.gz && \
        rm v1.5.4.tar.gz && \
	ln -sf $WORKDIR/enaBrowserTools/python3/enaDataGet /usr/local/bin	
