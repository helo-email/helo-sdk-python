from __future__ import annotations

from typing import Any, Dict, List, Optional

from ..types.statistics import (
    StatisticsDailyResponse,
    StatisticsHourlyResponse,
    StatisticsTotalsResponse,
)
from ._base import BaseResource


class StatisticsResource(BaseResource):
    def retrieve_hourly(
        self,
        *,
        from_: str,
        to: str,
        channel_id: Optional[str] = None,
        tags: Optional[List[str]] = None,
    ) -> StatisticsHourlyResponse:
        params: Dict[str, Any] = {"from": from_, "to": to}
        if channel_id is not None:
            params["channelId"] = channel_id
        if tags is not None:
            params["tags"] = tags
        data = self._http.get("/activity/statistics/hourly", params=params)
        return StatisticsHourlyResponse.model_validate(data)

    def retrieve_daily(
        self,
        *,
        from_: str,
        to: str,
        timezone: str,
        channel_id: Optional[str] = None,
        tags: Optional[List[str]] = None,
    ) -> StatisticsDailyResponse:
        params: Dict[str, Any] = {"from": from_, "to": to, "timezone": timezone}
        if channel_id is not None:
            params["channelId"] = channel_id
        if tags is not None:
            params["tags"] = tags
        data = self._http.get("/activity/statistics/daily", params=params)
        return StatisticsDailyResponse.model_validate(data)

    def retrieve_totals(
        self,
        *,
        from_: str,
        to: str,
        channel_id: Optional[str] = None,
        tags: Optional[List[str]] = None,
    ) -> StatisticsTotalsResponse:
        params: Dict[str, Any] = {"from": from_, "to": to}
        if channel_id is not None:
            params["channelId"] = channel_id
        if tags is not None:
            params["tags"] = tags
        data = self._http.get("/activity/statistics/totals", params=params)
        return StatisticsTotalsResponse.model_validate(data)
