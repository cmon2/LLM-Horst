"""
title: Append Basic Data
author: cmon2
author_url: https://github.com/cmon2
git_url: https://github.com/cmon2
description:
Appends the system prompt with basic data. Basic data includes:
* user id
* user name
requirements: cmon2lib
version: 0.0.1
license: MIT
"""

from pydantic import BaseModel, Field
from typing import Callable, Awaitable, Any, Optional
from cmon2lib.utils.cmon_logging import clog


class Filter:
    class Valves(BaseModel):
        pass

    def __init__(self):
        pass

    async def inlet(
        self,
        body: dict,
        __event_emitter__: Callable[[Any], Awaitable[None]],
        __request__: Any,
        __user__: Optional[dict] = None,
        __model__: Optional[dict] = None,
    ) -> dict:

        if "messages" in body and isinstance(body["messages"], list):
            body["messages"].insert(0, "Hello world:)")
        else:
            body["messages"] = ["Hello world:)"]

        return body
