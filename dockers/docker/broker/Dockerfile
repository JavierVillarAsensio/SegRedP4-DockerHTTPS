FROM midebian

COPY entrypoint.sh /entrypoint.sh
COPY broker.py /home/broker.py
COPY exceptions.py /home/exceptions.py
COPY broker.crt /home/broker.crt
COPY broker.key /home/broker.key
COPY file.crt /home/file.crt
COPY auth.crt /home/auth.crt

WORKDIR /home
ENTRYPOINT ["/bin/bash", "/entrypoint.sh"]
