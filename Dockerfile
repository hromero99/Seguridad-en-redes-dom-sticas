FROM python:3
COPY . /app
RUN pip3 install -r /app/requirements.txt
EXPOSE 8000
WORKDIR /app/Documentation/
CMD ["mkdocs","serve"]
