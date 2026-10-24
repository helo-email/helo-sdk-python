from __future__ import annotations

from collections.abc import Sequence

from .._utils import build_params
from ..types.statistics import (
    StatisticsDailyResponse,
    StatisticsHourlyResponse,
    StatisticsTotalsResponse,
)
from ._base import AsyncBaseResource, BaseResource


class StatisticsResource(BaseResource):
    def retrieve_hourly(
        self,
        *,
        from_: str,
        to: str,
        channel_id: str | None = None,
        tags: Sequence[str] | None = None,
    ) -> StatisticsHourlyResponse:
        """Retrieve hourly statistics"""

        params = build_params(
            from_=from_,
            to=to,
            channel_id=channel_id,
            tags=",".join(tags) if tags else None,
        )
        data = self._http.get("/statistics/hourly", params=params)
        return StatisticsHourlyResponse.model_validate(data)

    def retrieve_daily(
        self,
        *,
        from_: str,
        to: str,
        timezone: str,
        channel_id: str | None = None,
        tags: Sequence[str] | None = None,
    ) -> StatisticsDailyResponse:
        """Retrieve daily statistics"""

        params = build_params(
            from_=from_,
            to=to,
            timezone=timezone,
            channel_id=channel_id,
            tags=",".join(tags) if tags else None,
        )
        data = self._http.get("/statistics/daily", params=params)
        return StatisticsDailyResponse.model_validate(data)

    def retrieve_totals(
        self,
        *,
        from_: str,
        to: str,
        channel_id: str | None = None,
        tags: Sequence[str] | None = None,
    ) -> StatisticsTotalsResponse:
        """Retrieve all time statistics"""

        params = build_params(
            from_=from_,
            to=to,
            channel_id=channel_id,
            tags=",".join(tags) if tags else None,
        )
        data = self._http.get("/statistics/totals", params=params)
        return StatisticsTotalsResponse.model_validate(data)


class AsyncStatisticsResource(AsyncBaseResource):
    async def retrieve_hourly(
        self,
        *,
        from_: str,
        to: str,
        channel_id: str | None = None,
        tags: Sequence[str] | None = None,
    ) -> StatisticsHourlyResponse:
        """Retrieve hourly statistics"""

        params = build_params(
            from_=from_,
            to=to,
            channel_id=channel_id,
            tags=",".join(tags) if tags else None,
        )
        data = await self._http.get("/statistics/hourly", params=params)
        return StatisticsHourlyResponse.model_validate(data)

    async def retrieve_daily(
        self,
        *,
        from_: str,
        to: str,
        timezone: str,
        channel_id: str | None = None,
        tags: Sequence[str] | None = None,
    ) -> StatisticsDailyResponse:
        """Retrieve daily statistics"""

        params = build_params(
            from_=from_,
            to=to,
            timezone=timezone,
            channel_id=channel_id,
            tags=",".join(tags) if tags else None,
        )
        data = await self._http.get("/statistics/daily", params=params)
        return StatisticsDailyResponse.model_validate(data)

    async def retrieve_totals(
        self,
        *,
        from_: str,
        to: str,
        channel_id: str | None = None,
        tags: Sequence[str] | None = None,
    ) -> StatisticsTotalsResponse:
        """Retrieve all time statistics"""

        params = build_params(
            from_=from_,
            to=to,
            channel_id=channel_id,
            tags=",".join(tags) if tags else None,
        )
        data = await self._http.get("/statistics/totals", params=params)
        return StatisticsTotalsResponse.model_validate(data)
