FROM python:3.7

WORKDIR /usr/src/norminette

COPY . .

RUN pip3 install -r requirements.txt
RUN python3 setup.py install

ENTRYPOINT ["norminette"]