# Statistics

Retrieve delivery statistics. `from_` and `to` are ISO-8601 date strings.

## Hourly statistics

`GET /activity/statistics/hourly`

```python Statistics_retrieveHourly
import sdk_helo_email as helo

client = helo.Helo(api_key="your-api-key")

stats = client.statistics.retrieve_hourly(from_="2024-01-01", to="2024-01-02")
```

## Daily statistics

`GET /activity/statistics/daily`

```python Statistics_retrieveDaily
import sdk_helo_email as helo

client = helo.Helo(api_key="your-api-key")

stats = client.statistics.retrieve_daily(
    from_="2024-01-01",
    to="2024-01-31",
    timezone="America/New_York",
)
```

## Total statistics

`GET /activity/statistics/totals`

```python Statistics_retrieveTotals
import sdk_helo_email as helo

client = helo.Helo(api_key="your-api-key")

stats = client.statistics.retrieve_totals(from_="2024-01-01", to="2024-01-31")
```
