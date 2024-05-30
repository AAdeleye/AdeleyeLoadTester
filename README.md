# AdeleyeFireWorksAI

## Objectives and Goals
- Takes an HTTP adress as input
- Supports a --qps flag to generate requests at a given fixed QPS
- Reports Latencies and error rates
- Make a buildable Docker image

## Running Example Code
A dockerfile is used to run the  `generalPurposeHTTPS_LoadTest.py` file. This file can be modified to test a single url or multiple. 
1. Testing a singel URL
   -   This line in the docerfile:
       ```
       CMD python ./generalPurposeHTTP_LoadTest.py --url_link http://httpbin.org/status/400%20%2C200 --qps 10 --n 1000 --c 100
       ```
       is an example of how to test a singal URL with flags for QPS, -n: number of request, and -c: number of concurrent request. 
2. Testing multiple URLs
   -   This line in the docerfile:
       ```
        CMD python ./generalPurposeHTTP_LoadTest.py --url_csv urllist.csv --qps 10 --n 1000 --c 100
       ```
       is an example of how to test a multiple URLs. A `.csv` file is requried for this test.

Once your dockerFile is configured, you can build and run it similarly inside of this cloned repo:
```
docker build -t fireworksai:app .
docker run -it --rm fireworksai:app
```
  









