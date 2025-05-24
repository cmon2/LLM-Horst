"""
title: Message Date And Time
author: benasraudys
author_url: https://github.com/benasraudys
funding_url: https://github.com/benasraudys
description: Gives model current date and time context for each message. Don't forget to adjust the timezone in the settings.
version: 0.1.1
required_open_webui_version: 0.6.4
"""

import os
from pydantic import BaseModel, Field
from typing import Callable, Awaitable, Any, Optional


class Filter:
    class Valves(BaseModel):
        timezone_hours: string = Field(
            default=0,
            description="Timezone offset hours (e.g., 5 for UTC+5:30, -4 for UTC-4:00)",
        )
        timezone_minutes: int = Field(
            default=0,
            description="Timezone offset minutes (e.g., 30 for UTC+5:30, 45 for UTC-4:45)",
        )
        southern_hemisphere: bool = Field(
            default=False,
            description="Enable if you're in the Southern Hemisphere (Australia, South America, etc.)",
        )

    def __init__(self):
        self.valves = self.Valves(
            **{
                "timezone_hours": int(os.getenv("DATETIME_TIMEZONE_HOURS", "0")),
                "timezone_minutes": int(os.getenv("DATETIME_TIMEZONE_MINUTES", "0")),
                "southern_hemisphere": os.getenv(
                    "DATETIME_SOUTHERN_HEMISPHERE", "false"
                ).lower()
                == "true",
            }
        )
    
    async def inlet(
        self,
        body: dict,
        __event_emitter__: Callable[[Any], Awaitable[None]],
        __request__: Any,
        __user__: Optional[dict] = None,
        __model__: Optional[dict] = None,
    ) -> dict:
        now_utc = datetime.datetime.utcnow()

        timezone_hours = self.valves.timezone_hours
        timezone_minutes = self.valves.timezone_minutes
        total_offset_minutes = (timezone_hours * 60) + timezone_minutes

        

        context = f"Current date is {day_of_week}, {formatted_date}, {season}, {time_of_day}, the user time is {formatted_time} {timezone_str}"

        datetime_message = {
            "role": "system",
            "content": f"Time context: {context}. ",
        }

        if "messages" in body and isinstance(body["messages"], list):
            body["messages"].insert(0, datetime_message)
        else:
            body["messages"] = [datetime_message]

        return body
