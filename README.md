# AdeleyeLoadTester

## Objectives and Goals
- Takes an HTTP address input plus multiple addresses. 
- Supports a --qps flag to generate requests at a given fixed QPS
- Reports Latencies and error rates plus latencies and errors of concurrent requests.
- Make a buildable Docker image

## Running Example Code
A dockerfile is used to run the  `generalPurposeHTTPS_LoadTest.py` file. This file can be modified to test a single url or multiple as well as save or print results. 
1. Testing a single URL
   -   This line in the dockerfile:
       ```
       CMD python ./generalPurposeHTTP_LoadTest.py --url_link http://httpbin.org/status/400%20%2C200 --qps 10 --n 1000 --c 100
       ```
       is an example of how to test a single URL with flags for QPS, -n: number of request, and -c: number of concurrent request. 
2. Testing multiple URLs
   -   This line in the dockerfile:
       ```
        CMD python ./generalPurposeHTTP_LoadTest.py --url_csv urllist.csv --qps 10 --n 1000 --c 100
       ```
       is an example of how to test a multiple URLs. A `.csv` file is required for this test.
3. Saving results to .txt file
   -   The default is to print the results. Using the `--s` flag however, you can save results to a .txt file. 
   
Once your dockerFile is configured, you can build and run it similarly inside of this cloned repo:
```
docker build -t fireworksai:app .
docker run -it --rm fireworksai:app
```

If you choose to use the `--s` file. Be sure to cp your output file to your local host.
```
docker build -t fireworksai:app .
docker run --name fireworks fireworksai:app
docker cp fireworks:/usr/src/fireworksapp/outputlog.txt .
docker rm fireworks
```
  
## Testing/Comparing Code
The file test.py has a base level implementation of a web load testing software called [Locus](https://docs.locust.io/en/latest/what-is-locust.html).
Apart from this, online websites such as [PingDom](https://tools.pingdom.com/#63f2809af8000000) can be used. 








