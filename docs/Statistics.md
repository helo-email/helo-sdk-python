# Statistics

Access activity statistics.

| Method | HTTP request | Description |
| ------ | ------------ | ----------- |
| [**statistics.retrieve_hourly**](#retrieve_hourly) | **GET** /statistics/hourly | Retrieve hourly statistics |
| [**statistics.retrieve_daily**](#retrieve_daily) | **GET** /statistics/daily | Retrieve daily statistics |
| [**statistics.retrieve_totals**](#retrieve_totals) | **GET** /statistics/totals | Retrieve all time statistics |

## retrieve_hourly

`GET /statistics/hourly`

Fetches hourly aggregated statistics.

```python Statistics_retrieveHourly
import sdk_helo_email as helo

client = helo.Helo()  # reads HELO_API_KEY from the environment

statistics_hourly = client.statistics.retrieve_hourly(
    from_="2024-01-01T00:00:00Z",
    to="2024-01-01T00:00:00Z",
    channel_id="550e8400-e29b-41d4-a716-446655440000",
)
```

## retrieve_daily

`GET /statistics/daily`

Fetches daily aggregated statistics.

```python Statistics_retrieveDaily
import sdk_helo_email as helo

client = helo.Helo()  # reads HELO_API_KEY from the environment

statistics_daily = client.statistics.retrieve_daily(
    from_="2024-01-01",
    to="2024-01-01",
    timezone="America/New_York",
    channel_id="550e8400-e29b-41d4-a716-446655440000",
)
```

## retrieve_totals

`GET /statistics/totals`

Fetches cumulative statistics.

```python Statistics_retrieveTotals
import sdk_helo_email as helo

client = helo.Helo()  # reads HELO_API_KEY from the environment

statistics_totals = client.statistics.retrieve_totals(
    from_="2024-01-01T00:00:00Z",
    to="2024-01-01T00:00:00Z",
    channel_id="550e8400-e29b-41d4-a716-446655440000",
)
```
