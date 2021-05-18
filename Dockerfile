#Download base image ubuntu 20.04
FROM ubuntu:20.04
# LABEL about the custom image
LABEL maintainer="pedcremo@gmail.com"
LABEL version="0.1"
LABEL description="This is custom Docker Image for the IOT Internet wide scanner."
# Disable Prompt During Packages Installation
ARG DEBIAN_FRONTEND=noninteractive

# Update Ubuntu Software repository
RUN apt update
# Install python3 interpreter and python3-pip packet manager to run present project
# install too zmap and git because we need as prerequisite to run present project
RUN apt install -y python3 python3-pip zmap git wget && \
    rm -rf /var/lib/apt/lists/* && \
    apt clean

#Define the ENV variable
ENV OPT /opt
#ENV HOME /opt/iot_wide_scanner

#Create project folder 
RUN mkdir /root/iot_wide_scanner
#Clone zgrab2 project
#RUN cd /root && git clone https://github.com/zmap/zgrab2.git

COPY config.ini /root/iot_wide_scanner
COPY requirements.txt /root/iot_wide_scanner
RUN pip3 install -r /root/iot_wide_scanner/requirements.txt
# We are going to compile zgrab2 programmed in golang
RUN cd /tmp
RUN wget -d https://golang.org/dl/go1.16.3.linux-amd64.tar.gz
RUN tar -C /usr/local -xzf go1.16.3.linux-amd64.tar.gz
# Configure PATH to find go interpreter in path
ENV PATH="/usr/local/go/bin:${PATH}"

RUN go get github.com/zmap/zgrab2
RUN cd /root/go/pkg/mod/github.com/zmap/zgrab2@v0.1.7 && go mod download github.com/stretchr/testify
RUN cd /root/go/pkg/mod/github.com/zmap/zgrab2@v0.1.7 && make
RUN ln -s /root/go/pkg/mod/github.com/zmap/zgrab2@v0.1.7/zgrab2 /usr/bin/zgrab2
#CMD RUN PRoGRAM

