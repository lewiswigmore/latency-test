import time
import requests
import argparse
import statistics
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urlparse
from tqdm import tqdm

def print_welcome_screen():
    welcome = r"""
     _        _                                 
    | |      (_)                                
    | |       _  __ _ _ __ ___   __ _     
    | |      | |/ _` | '_ ` _ \ / _` |
    | |____  | | (_| | | | | | | (_| |
    |______| |_|\__, |_| |_| |_|\__,_|
                 __/ |                          
                |___/                           
    Ligma - Latency Measurement
    """
    print(welcome)

def normalise_url(url):
    """
    Automatically adds 'https://' and 'www.' to a URL if missing.

    Parameters:
        url (str): The URL to normalise.

    Returns:
        str: The normalised URL.
    """
    if not urlparse(url).scheme:
        url = "https://" + url
    if urlparse(url).netloc and not urlparse(url).netloc.startswith("www."):
        url = url.replace("://", "://www.")
    return url


def test_single_request(url, test_number, total_tests):
    """
    Tests the latency of a single request to the given URL.

    Parameters:
        url (str): The URL to test.
        test_number (int): Current test number.
        total_tests (int): Total number of tests.

    Returns:
        float: The latency in milliseconds or None if the request fails.
    """
    start_time = time.perf_counter()
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
    except requests.RequestException:
        print(f"Test {test_number}/{total_tests}: Request failed")
        return None
    end_time = time.perf_counter()
    latency = (end_time - start_time) * 1000  # Convert to milliseconds
    # print(f"Test {test_number}/{total_tests}: {latency:.2f} ms")
    return latency


def test_latency(url, num_tests=100, max_workers=10):
    """
    Tests the latency of a URL by making multiple requests and calculating the average latency.

    Parameters:
        url (str): The URL to test.
        num_tests (int): The number of requests to make.
        max_workers (int): Maximum number of concurrent requests.

    Returns:
        dict: A dictionary with various latency metrics.
    """
    latencies = []
    start_time = time.perf_counter()

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        results = executor.map(
            test_single_request,
            [url] * num_tests,
            range(1, num_tests + 1),
            [num_tests] * num_tests,
        )
        
        for latency in tqdm(results, total=num_tests, desc="Testing latency", unit="test"):
            if latency is not None:
                latencies.append(latency)

    end_time = time.perf_counter()

    if not latencies:
        print("All requests failed. Unable to calculate average latency.\n")
        return None

    average_latency = sum(latencies) / len(latencies)
    min_latency = min(latencies)
    max_latency = max(latencies)
    latency_stdev = statistics.stdev(latencies) if len(latencies) > 1 else 0
    success_rate = (len(latencies) / num_tests) * 100
    total_duration = end_time - start_time
    throughput = len(latencies) / total_duration  # Requests per second

    print(f"\nAverage Latency: {average_latency:.2f} ms over {len(latencies)} successful tests.")
    print(f"Min Latency: {min_latency:.2f} ms")
    print(f"Max Latency: {max_latency:.2f} ms")
    print(f"Latency Standard Deviation: {latency_stdev:.2f} ms")
    print(f"Success Rate: {success_rate:.2f}%")
    print(f"Total Test Duration: {total_duration:.2f} seconds")
    print(f"Throughput: {throughput:.2f} requests/second\n")

    return {
        "average_latency": average_latency,
        "min_latency": min_latency,
        "max_latency": max_latency,
        "latency_stdev": latency_stdev,
        "success_rate": success_rate,
        "total_duration": total_duration,
        "throughput": throughput
    }


def main():
    print_welcome_screen()

    parser = argparse.ArgumentParser(description="Test the latency of a specified URL with multiple requests.")
    parser.add_argument("url", type=str, help="The URL to test.")
    parser.add_argument("-n", "--num_tests", type=int, default=100, help="The number of tests to run (default is 100).")
    parser.add_argument("-w", "--workers", type=int, default=10, help="The number of concurrent workers (default is 10).")
    args = parser.parse_args()

    url = normalise_url(args.url)
    print(f"Testing URL: {url}")
    test_latency(url, args.num_tests, args.workers)


if __name__ == "__main__":
    main()