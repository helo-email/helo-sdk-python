from __future__ import annotations

from datetime import date, datetime

from .shared import HeloModel


class DeliveryStats(HeloModel):
    sent: int | None = None
    delivered: int | None = None
    opened: int | None = None
    clicked: int | None = None
    bounced: int | None = None
    unsubscribed: int | None = None
    complained: int | None = None


class StatisticsTotalsResponse(HeloModel):
    transactional: DeliveryStats | None = None
    broadcast: DeliveryStats | None = None


class DailyStatisticsEntry(HeloModel):
    timestamp: date
    transactional: DeliveryStats | None = None
    broadcast: DeliveryStats | None = None


class StatisticsDailyResponse(HeloModel):
    results: list[DailyStatisticsEntry]


class HourlyStatisticsEntry(HeloModel):
    timestamp: datetime
    transactional: DeliveryStats | None = None
    broadcast: DeliveryStats | None = None


class StatisticsHourlyResponse(HeloModel):
    results: list[HourlyStatisticsEntry]
