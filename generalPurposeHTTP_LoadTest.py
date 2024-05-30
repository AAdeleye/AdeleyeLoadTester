
import argparse
import validators
import time
import asyncio
import aiohttp
from tqdm import tqdm
import os
import pandas as pd
from datetime import datetime

async def runURLRequest(url,session):
    """ Calls a request to url.

    Args:
      url:
      session: number of request.

    Returns:
      current latency and error count. 
    """

    num_errors = 0
    start_time = time.monotonic()
    try:
        response = await session.get(url)
        end_time = time.monotonic()
        res = response.status
        if res < 200 or res > 299:
            num_errors += 1
        latency = end_time - start_time
    except Exception as e:
        end_time = time.monotonic() 
        num_errors += 1
        latency = end_time - start_time
        
    return num_errors,latency

async def urlRequestStats(url,total_num_request,num_concurrent,qps,s):
    """Shell for calling request to url and recording latency and error metrics.

    Args:
      url_or_csv: A str URL or path to a .csv file.
      num_reqest: number of request.
      num_concurrent: number of concurrent request.
      qps: Fixed QPS to generate request.

    """
    async with aiohttp.ClientSession() as session:
        totalErrors = 0 
        totalLatency = 0 
        num_request = total_num_request
        pbar = tqdm(total=num_request, desc="Processing Requests")
        interval = 1 / qps if qps > 0 else 0

        while num_request > 0:
            tasks = []
            
            #Make sure we run the exact number of request. 
            if num_request > num_concurrent:
                num_request -= num_concurrent
            else:
                num_concurrent = num_request
                num_request = 0

            for _ in range(num_concurrent):
                tasks.append(runURLRequest(url,session))
            start_time = time.monotonic()
            batchResponses = await asyncio.gather(*tasks,return_exceptions=True)
            end_time = time.monotonic()
            elapsed_time = end_time - start_time

            # Delay the next batch to maintain the QPS rate
            if elapsed_time < interval:
                await asyncio.sleep(interval - elapsed_time)
            errorSum,latencySum = map(sum,zip(*batchResponses))
            totalErrors += errorSum
            totalLatency += latencySum
            pbar.update(num_concurrent)

    pbar.close()

    average_latency = totalLatency / total_num_request if total_num_request > 0 else 0
    error_rate = totalErrors / total_num_request if total_num_request > 0 else 0

    if s:
        current_datetime = datetime.now()
        with open('outputlog.txt', 'a') as file:
            file.write(f"Date and Time: {current_datetime}\n")
            file.write(f"Testing URL: {url}\n")
            file.write(f"The Avereage Error Rate is: {error_rate}%\n")
            file.write(f"The Average Latency is: {average_latency:.2f} seconds\n")
            file.write(f"This test was completed with Total request: {total_num_request}, Concurrent request: {num_concurrent}, with a QPS of: {qps}\n")
            file.write(f"#################################################################################################################################\n")
    else:
        print(f"\nTesting URL: {url}")
        print(f"The Avereage Error Rate is: {error_rate}%")
        print(f"The Average Latency is: {average_latency:.2f} seconds")
        print(f"This test was completed with Total request: {total_num_request}, Concurrent request: {num_concurrent}, with a QPS of: {qps}")


def main(url_or_csv,num_request,num_concurrent,qps,s):
    """Main fuction that load tests either one url or multiple depending if we recived a url or csv file.

    Args:
      url_or_csv: A str URL or path to a .csv file.
      num_reqest: number of request.
      num_concurrent: number of concurrent request.
      qps: Fixed QPS to generate request.

    """

    if not url_or_csv.lower().endswith('.csv'):
        asyncio.run(urlRequestStats(url_or_csv,num_request,num_concurrent,qps,s))
    else:
        if not os.path.isfile(url_or_csv):
            print(f"Error: The file {url_or_csv} does not exist.")
            exit()
        try:
            df = pd.read_csv(url_or_csv)
        except Exception as e:
            print(f"File was not able to be read. Please make sure file is in CSV format where urls are on one line seperated by commas.\n Error: {e} ")
        
        for url in df.columns:
            if not validators.url(url):
                print(f"{url} not valid. Please check link and be sure to include full https://... url.")
            else:
                asyncio.run(urlRequestStats(url,num_request,num_concurrent,qps,s))

if __name__ == "__main__":

    """
    Python Main for running Custom Http Load testing. 
    Arguments are parsed here and sent to rest of code block

    """
    # Parse URL(s) 
    parser = argparse.ArgumentParser(description='Arguments for Https Load tester')
    parser.add_argument('--url_link', type=str, help='Enter URL Link you want to test')
    parser.add_argument('--url_csv',type=str, help='Enter a csv file with URL Links you want to test')
    parser.add_argument('--qps', type=int, default=0, help='Generate request at given fixed QPS. Plese note, if the --c flag is not set to zero, concurrent request may be sent at the fixed QPS.')
    parser.add_argument('--n',type=int, default=1000, help='total number of request to preform.')
    parser.add_argument('--c',type=int, default=100, help='number of concurrent request to preform untill total number of request is reached.')
    parser.add_argument('--s',action="store_true", help='Save results to a .txt file rather than print them')
    parse_args,unknown = parser.parse_known_args()

    # Checks for URL and CSV 
    if not parse_args.url_link and not parse_args.url_csv:
        print("Please enter a url link or csv file you want to test. Example: 'docker run fireworksai:app --url_link http:/www.google.com' ")
        exit()
    if parse_args.url_link: # url flag overides csv file. (design choice)
        if not validators.url(parse_args.url_link):
            print(f"{parse_args.url_link} not valid. Please check link and be sure to include full https://... url.")
            exit()
        main(parse_args.url_link,parse_args.n,parse_args.c,parse_args.qps,parse_args.s)
    elif parse_args.url_csv:
        main(parse_args.url_csv,parse_args.n,parse_args.c,parse_args.qps,parse_args.s)




"""
Code Notes and Things: 

TODO: 
4. Save results to a txt file. (Done at 9:43am with minimal testing)
5. Graphs to show latancy and errors. 
6. Add any more intresting load measurments. 
"""

 