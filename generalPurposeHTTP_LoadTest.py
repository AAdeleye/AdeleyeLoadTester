
import argparse
import validators
import time
import asyncio
import aiohttp
from tqdm import tqdm
import os
import pandas as pd


async def runURLRequest(url,session):
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

async def urlRequestStats(url,total_num_request,num_concurrent,qps):
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
    print(f"Testing URL: {url}")
    print(f"The Avereage Error Rate is: {error_rate}")
    print(f"The Average Latency is: {average_latency:.2f} seconds")
    print(f"This test was completed with Total request: {total_num_request}, Concurrent request: {num_concurrent}, with a QPS of: {qps}")
    

def main(url_or_csv,num_request,num_concurrent,qps):
    if not url_or_csv.lower().endswith('.csv'):
        asyncio.run(urlRequestStats(url_or_csv,num_request,num_concurrent,qps))
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
                asyncio.run(urlRequestStats(url,num_request,num_concurrent,qps))

if __name__ == "__main__":
    # Parse URL(s) 
    parser = argparse.ArgumentParser(description='Arguments for Https Load tester')
    parser.add_argument('--url_link', type=str, help='Enter URL Link you want to test')
    parser.add_argument('--url_csv',type=str, help='Enter a csv file with URL Links you want to test')
    parser.add_argument('--qps', type=int, default=0, help='Generate request at given fixed QPS. Plese note, if the --c flag is not set to zero, concurrent request may be sent at the fixed QPS.')
    parser.add_argument('--n',type=int, default=1000, help='total number of request to preform.')
    parser.add_argument('--c',type=int, default=100, help='number of concurrent request to preform untill total number of request is reached.')
    parse_args,unknown = parser.parse_known_args()

    #TODO: 
    # 2. Accpet a csv file of Http Websites
    # 3. Save results to a txt file. 

    if not parse_args.url_link and not parse_args.url_csv:
        print("Please enter a url link or csv file you want to test. Example: 'docker run fireworksai:app --url_link http:/www.google.com' ")
        exit()
    
    if parse_args.url_link:
        # Check if URL is valid
        if not validators.url(parse_args.url_link):
            print(f"{parse_args.url_link} not valid. Please check link and be sure to include full https://... url.")
            exit()
        main(parse_args.url_link,parse_args.n,parse_args.c,parse_args.qps)
    elif parse_args.url_csv:
        main(parse_args.url_csv,parse_args.n,parse_args.c,parse_args.qps)