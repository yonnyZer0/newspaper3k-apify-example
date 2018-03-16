FROM python:3.5

RUN apt-get install -yq python-dev libxml2-dev libxslt-dev libjpeg-dev zlib1g-dev libpng12-dev

RUN pip3 install newspaper

RUN python3 -c "import nltk; ntlk.download('punkt')"

CMD ['python3','newspaper-act.py']
