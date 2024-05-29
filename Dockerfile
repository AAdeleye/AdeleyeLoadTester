FROM python:3.12

WORKDIR /usr/src/fireworksapp

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD python ./generalPurposeHTTP_LoadTest.py --url_link https://www.google.com
#CMD [ "python", "./your-daemon-or-script.py" ]
