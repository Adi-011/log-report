There is an access log at `/app/access.log`. 
Parse it and write a JSON summary report to `/app/report.json`.

The report must be a single JSON object with these three keys:
1. `total_requests` — an integer, the total number of log lines in the file.
2. `unique_ips` — an integer, the number of different client IP addresses.
3. `top_path` — a string, the request path (e.g. `/index.html`) that comes up across all requests.

Example:
```json
{"total_requests": 6, "unique_ips": 3, "top_path": "/index.html"}
```

Criteria for success:
1. `/app/report.json` exists and it contains valid JSON.
2. It contains the given keys `total_requests`, `unique_ips`, and `top_path` and no more, no less.
3. Its `total_requests` should match the actual number of requests in `/app/access.log`.
4. Its `unique_ips` should match the actual number of distinct client IPs in `/app/access.log`.
5. Its `top_path` should match the actual most requested path in `/app/access.log`.