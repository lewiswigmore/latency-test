# Latency Measurement Tool

Python tool for measuring the latency of a specified URL by making multiple HTTP requests and calculating a few latency metrics. It supports concurrent testing using threads to simulate multiple requests in parallel for faster and more reliable results.

## Features

- Normalises the input URL by adding `https://` and `www.` if missing.
- Measures the latency of a URL by making multiple requests (default is 100).
- Uses concurrent requests for faster testing.
- Outputs latency metrics such as average latency, minimum latency, maximum latency, and standard deviation.
- Displays test results including success rate and throughput.

## Requirements

- Python 3.x
- `requests` library
- `tqdm` library

You can install the required libraries using the following:

```bash
pip install requests tqdm
```

## Usage

Run the script with the following command:

```bash
python latency_test.py <URL> [options]
```

### Options:
- `url`: The URL you want to test (e.g., `https://example.com`).
- `-n, --num_tests`: The number of tests to run (default is 100).
- `-w, --workers`: The number of concurrent workers to use for the tests (default is 10).

### Example:

```bash
python latency_test.py example.com -n 200 -w 20
```

This command will test the latency of `example.com` with 200 requests, using 20 concurrent workers.

## Output

The results will display:
- Average latency in milliseconds.
- Minimum and maximum latency.
- Standard deviation of latencies.
- Success rate of requests.
- Total test duration.
- Throughput (requests per second). 

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more information.