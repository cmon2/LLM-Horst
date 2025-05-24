"""
title: Append Taiga Projects
author: cmon2
author_url: https://github.com/cmon2
git_url: https://github.com/cmon2
description: Provides model with Taiga project context. Requires TAIGA_API_URL, TAIGA_USERNAME, and TAIGA_PASSWORD to be set in the environment variables.
requirements: cmon2lib
license: MIT
"""

import os
from pydantic import BaseModel, Field
from typing import Callable, Awaitable, Any, Optional

# Import the cmon2lib library
try:
    import cmon2lib.taiga.taiga_user_functions
    import cmon2lib.taiga.taiga_project_functions
except ImportError:
    raise ImportError("The 'cmon2lib' library is not installed. Please install it using 'pip install cmon2lib'.")


class Filter:
    class Valves(BaseModel):
        taiga_api_url: str = Field(
            default="",
            description="The URL of your Taiga API (e.g., https://api.taiga.io/api/v1)",
        )
        taiga_username: str = Field(
            default="",
            description="Your Taiga username",
        )
        taiga_password: str = Field(
            default="",
            description="Your Taiga password",
        )

    def __init__(self):
        self.valves = self.Valves(
            **{
                "taiga_api_url": os.getenv("TAIGA_API_URL", ""),
                "taiga_username": os.getenv("TAIGA_USERNAME", ""),
                "taiga_password": os.getenv("TAIGA_PASSWORD", ""),
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
        taiga_api_url = self.valves.taiga_api_url
        taiga_username = self.valves.taiga_username
        taiga_password = self.valves.taiga_password

        if not all([taiga_api_url, taiga_username, taiga_password]):
            print("Taiga API credentials not fully set. Skipping Taiga context.")
            return body

        try:
            # Get authenticated user projects
            user_projects = cmon2lib.taiga.taiga_user_functions.get_authenticated_user_projects(
                host=taiga_api_url,
                user=taiga_username,
                password=taiga_password,
            )

            # Build project context
            taiga_projects_list = []
            if user_projects:
                for project in user_projects:
                    # You might want to customize what project information you include
                    # For example, using cprint_project to get a formatted string
                    project_info = cmon2lib.taiga.taiga_project_functions.cprint_project(project)
                    taiga_projects_list.append(project_info)

            context = "\n".join(taiga_projects_list) if taiga_projects_list else "No Taiga projects found for the user."

            taiga_projects_message = {
                "role": "system",
                "content": f"Taiga Projects Context: \n{context}",
            }

            if "messages" in body and isinstance(body["messages"], list):
                body["messages"].insert(0, taiga_projects_message)
            else:
                body["messages"] = [taiga_projects_message]

        except Exception as e:
            print(f"Error fetching Taiga projects: {e}")

        return body