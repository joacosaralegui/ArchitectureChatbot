FROM ubuntu:18.04
ENTRYPOINT []
RUN apt-get update && apt-get install -y python3 python3-pip \
    && apt-get install -y python3-dev graphviz libgraphviz-dev pkg-config python-enchant \
    && python3 -m pip install --no-cache --upgrade pip          \
    && pip3 install --no-cache rasa==2.0 && pip3 install pyenchant && pip3 install pygraphviz
ADD . /app/
RUN chmod +x /app/start_services_nlu.sh
CMD /app/start_services_nlu.sh