# 1. Verify logging
pytest -m valid -n 0

# 2. Verify screenshot + trace using the intentionally failing test
pytest -m debug --tracing retain-on-failure --screenshot only-on-failure -n 0

# 3. Run the full suite with parallel workers + HTML report
pytest -n 5 --html=reports/report.html --self-contained-html