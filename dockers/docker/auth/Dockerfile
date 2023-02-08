FROM midebian

COPY entrypoint.sh /entrypoint.sh
COPY auth.py /home/auth.py
COPY exceptions.py /home/exceptions.py
COPY auth.crt /home/auth.crt
COPY auth.key /home/auth.key
COPY credentials.txt /home/credentials.txt
WORKDIR /home

ENTRYPOINT ["/bin/bash", "/entrypoint.sh"]

