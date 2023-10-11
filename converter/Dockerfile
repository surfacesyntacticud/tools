# Start with a base Python3 image
FROM python:3.9-slim

# Update packages and install required tools for OCaml and OPAM
RUN apt-get update && apt-get install -y \
    opam \
    wget \
    m4 \
    unzip \
    librsvg2-bin \
    curl \
    bubblewrap \
    && rm -rf /var/lib/apt/lists/*


RUN opam init -a -y

# Initialize OPAM (this installs the latest version of OCaml)
RUN opam switch create 4.14.1 4.14.1


RUN opam remote add grew "http://opam.grew.fr"
RUN opam install grew -y



RUN pip3 install conllup

COPY ./grs /app/grs
COPY ./test2/data /app/test/data
COPY ./test2/check_conversion_auto.py /app/test/check_conversion_auto.py
COPY ./test2/tests_description.json /app/test/tests_description.json

WORKDIR /app/test/


CMD [ "python3", "check_conversion_auto.py" ]