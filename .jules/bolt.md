## 2024-05-01 - [Python Regex Precompilation]
**Learning:** Python code in this application often performs repeated regex matches on incoming request headers or payload lines (e.g. `domain_fronter.py` content-range matching or cookie splitting).
**Action:** Extract inline `re.search` or `re.split` inside high-traffic loops into module-level variables like `RE_CONTENT_RANGE = re.compile(...)`. This yields measurable CPU and memory savings by skipping implicit dictionary lookups and potential cache evictions in the internal Python re cache.
