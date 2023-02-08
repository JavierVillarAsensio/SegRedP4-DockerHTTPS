FROM midebian

COPY entrypoint.sh /entrypoint.sh
COPY file.py /home/file.py
COPY exceptions.py /home/exceptions.py
COPY users /home/users
COPY file.crt /home/file.crt
COPY file.key /home/file.key
COPY auth.crt /home/auth.crt
WORKDIR /home
ENTRYPOINT ["/bin/bash", "/entrypoint.sh"]
