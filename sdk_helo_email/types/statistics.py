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


class StatisticsDailyResponseResult(HeloModel):
    timestamp: date | None = None
    transactional: DeliveryStats | None = None
    broadcast: DeliveryStats | None = None


class StatisticsDailyResponse(HeloModel):
    results: list[StatisticsDailyResponseResult] | None = None


class StatisticsHourlyResponseResult(HeloModel):
    timestamp: datetime | None = None
    transactional: DeliveryStats | None = None
    broadcast: DeliveryStats | None = None


class StatisticsHourlyResponse(HeloModel):
    results: list[StatisticsHourlyResponseResult] | None = None
