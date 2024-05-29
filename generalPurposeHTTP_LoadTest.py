
import argparse
import validators

def latencies():
    pass

def error_rates():
    pass

def main(url):
    pass

if __name__ == "__main__":
    # Parse URL(s) 
    parser = argparse.ArgumentParser(description='Arguments for Https Load tester')
    parser.add_argument('--url_link', type=str, help='Enter URL Link you want to test')
    parser.add_argument('--qps', action='store_true', help='Generate request at given fixed QPS')
    parse_args,unknown = parser.parse_known_args()

    #TODO: 
    # 2. Accpet a csv file of Http Websites
    if not parse_args.url_link:
        print("Please enter a url link you want to test. Example: 'docker run fireworksai:app --url_link http:/www.google.com' ")
        exit()
    
    # Check if URL is valid
    if not validators.url(parse_args.url_link):
        print(f"{parse_args.url_link} not valid. Please check link and be sure to include full https://... url.")
        exit()
    
    main(parse_args.url_link)
    