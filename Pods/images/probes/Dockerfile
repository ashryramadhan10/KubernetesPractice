FROM ubuntu:22.04

USER root

# Install dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    python3.9 \
    python3-pip \
    python3-setuptools \
    build-essential \
    libssl-dev \
    libffi-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install Flask
RUN pip install Flask

RUN groupadd -r probesgroup && \
    useradd -r -g probesgroup -d /home/probesuser -m -s /bin/bash -c "Probe User" probesuser

# working space ownership
RUN mkdir -p /home/probesuser/app && \
    chown -R probesuser:probesgroup /home/probesuser/app

# copy every files to working space
COPY main.py /home/probesuser/app/main.py
RUN chown -R probesuser:probesgroup /home/probesuser/app/main.py

# change mode to working space and related files
RUN chmod 700 /home/probesuser/app/main.py && \
    chmod 700 /home/probesuser/app

EXPOSE 8080

USER probesuser

WORKDIR /home/probesuser/app

ENTRYPOINT [ "python3" ]
CMD ["main.py"]