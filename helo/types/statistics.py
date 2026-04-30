from __future__ import annotations

from datetime import date, datetime
from typing import List, Optional

from .shared import HeloModel


class DeliveryStats(HeloModel):
    sent: Optional[int] = None
    delivered: Optional[int] = None
    opened: Optional[int] = None
    clicked: Optional[int] = None
    bounced: Optional[int] = None
    unsubscribed: Optional[int] = None
    complained: Optional[int] = None


class StatisticsTotalsResponse(HeloModel):
    transactional: Optional[DeliveryStats] = None
    broadcast: Optional[DeliveryStats] = None


class DailyStatisticsEntry(HeloModel):
    timestamp: date
    transactional: Optional[DeliveryStats] = None
    broadcast: Optional[DeliveryStats] = None


class StatisticsDailyResponse(HeloModel):
    results: List[DailyStatisticsEntry]


class HourlyStatisticsEntry(HeloModel):
    timestamp: datetime
    transactional: Optional[DeliveryStats] = None
    broadcast: Optional[DeliveryStats] = None


class StatisticsHourlyResponse(HeloModel):
    results: List[HourlyStatisticsEntry]
