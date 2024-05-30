FROM python:3.12

WORKDIR /usr/src/fireworksapp

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .


# Run main code Examples
# CMD python ./generalPurposeHTTP_LoadTest.py --url_link http://httpbin.org/status/400%20%2C200 --qps 10 --n 1000 --c 100
CMD python ./generalPurposeHTTP_LoadTest.py --url_csv urllist.csv --qps 10 --n 1000 --c 100
# CMD python ./generalPurposeHTTP_LoadTest.py --url_csv urllist.csv --qps 10 --n 1000 --c 100 --s

# Compare performance using locust
#CMD locust -f test.py --headless -u 10 -r 10 --run-time 1m

