# Ubuntu installed with Python and Flask, running the Panduit Gateway Simulator

FROM ubuntu:16.04 

MAINTAINER Sameer Azad version: 1.0 

RUN apt-get update && apt-get install -y apt-utils && apt-get install -y curl vim python3 python3-pip net-tools && apt-get clean && rm -rf /var/lib/apt/lists/* && pip3 install flask && pip3 install flask-restful && pip3 install flask_httpauth
RUN mkdir panduit && cd panduit
COPY panduit_gw_token_auth.py /panduit/
RUN chmod +x /panduit/panduit_gw_token_auth.py

ENTRYPOINT ["/usr/bin/python3","/panduit/panduit_gw_token.py"]
