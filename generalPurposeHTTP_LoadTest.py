
import argparse
import validators
import time
import asyncio
import aiohttp
from tqdm import tqdm




async def runURLRequest(url,session):
    num_errors = 0
    start_time = time.time()
    try:
        response = await session.get(url)
        end_time = time.time() 
        response.status
        latency = end_time - start_time
    except Exception as e:
        end_time = time.time() 
        num_errors += 1
        latency = end_time - start_time
        
    return num_errors,latency

async def urlRequestStats(url,num_request,num_congruent):
    async with aiohttp.ClientSession() as session:
        totalErrors = 0 
        totalLatency = 0 
        pbar = tqdm(total=num_request, desc="Processing Requests")
        while num_request > 0:
            tasks = []
            num_request -= num_congruent
            for _ in range(num_congruent):
                tasks.append(runURLRequest(url,session))
            batchResponses = await asyncio.gather(*tasks,return_exceptions=True)
            errorSum,latencySum = map(sum,zip(*batchResponses))
            totalErrors += errorSum
            totalLatency += latencySum
            pbar.update(num_congruent)

    pbar.close()

    average_latency = totalLatency / num_request if num_request > 0 else 0
    error_rate = totalErrors / num_request if num_request > 0 else 0
    print(f"The error rate was: {error_rate}")
    print(f"The Average Latency is: {average_latency}")
    

def main(url,num_request,num_congruent):
    asyncio.run(urlRequestStats(url,num_request,num_congruent))



if __name__ == "__main__":
    # Parse URL(s) 
    parser = argparse.ArgumentParser(description='Arguments for Https Load tester')
    parser.add_argument('--url_link', type=str, help='Enter URL Link you want to test')
    parser.add_argument('--qps', action='store_true', help='Generate request at given fixed QPS')
    parser.add_argument('--n',type=int, default=1000, help='total number of request to preform.')
    parser.add_argument('--c',type=int, default=100, help='number of congrent request to preform untill total number of request is reached.')
    parse_args,unknown = parser.parse_known_args()

    #TODO: 
    # 2. Accpet a csv file of Http Websites
    # 3. Save results to a txt file. 

    if not parse_args.url_link:
        print("Please enter a url link you want to test. Example: 'docker run fireworksai:app --url_link http:/www.google.com' ")
        exit()
    
    # Check if URL is valid
    if not validators.url(parse_args.url_link):
        print(f"{parse_args.url_link} not valid. Please check link and be sure to include full https://... url.")
        exit()
    
    main(parse_args.url_link,parse_args.n,parse_args.c)
    
