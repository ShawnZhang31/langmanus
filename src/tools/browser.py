import asyncio

from pydantic import BaseModel, Field
from typing import Optional, ClassVar, Type
from langchain.tools import BaseTool
from browser_use import AgentHistoryList, Browser, BrowserConfig
from browser_use import Agent as BrowserAgent
from src.agents.llm import vl_llm
from src.tools.decorators import create_logged_tool
from src.config import (
    CHROME_INSTANCE_PATH,
    CHROME_HEADLESS,
    CHROME_PROXY_SERVER,
    CHROME_PROXY_USERNAME,
    CHROME_PROXY_PASSWORD,
    BROWSER_HISTORY_DIR,
)
import uuid
expected_browser = None

print("浏览器配置如下:")
print("="*10)
print(f"CHROME_HEADLESS: {CHROME_HEADLESS}")
print(f"CHROME_PROXY_SERVER: {CHROME_PROXY_SERVER}")
print(f"CHROME_PROXY_USERNAME: {CHROME_PROXY_USERNAME}")
print(f"CHROME_PROXY_PASSWORD: {CHROME_PROXY_PASSWORD}")
print(f"CHROME_INSTANCE_PATH: {CHROME_INSTANCE_PATH}")
print(f"BROWSER_HISTORY_DIR: {BROWSER_HISTORY_DIR}")
print("="*10)
# 优先使用代理服务器，其次使用本地 Chrome 实例
if CHROME_PROXY_SERVER:
    browser_config = BrowserConfig(
        headless=CHROME_HEADLESS,
        disable_security=True,
        cdp_url=CHROME_PROXY_SERVER
    )
elif CHROME_INSTANCE_PATH:
    browser_config = BrowserConfig(
        headless=CHROME_HEADLESS,
        disable_security=True,
        chrome_instance_path=CHROME_INSTANCE_PATH
    )
else:
    raise ValueError("No browser configuration found")



# if CHROME_PROXY_SERVER:
#     proxy_config = {
#         "server": CHROME_PROXY_SERVER,
#     }
#     if CHROME_PROXY_USERNAME:
#         proxy_config["username"] = CHROME_PROXY_USERNAME
#     if CHROME_PROXY_PASSWORD:
#         proxy_config["password"] = CHROME_PROXY_PASSWORD
#     browser_config.proxy = proxy_config

# # Use Chrome instance if specified
# if CHROME_INSTANCE_PATH:
#     expected_browser = Browser(
#         config=BrowserConfig(
#             headless=False,
#             disable_security=True,
#             chrome_instance_path=CHROME_INSTANCE_PATH)
#     )
expected_browser = Browser(config=browser_config)


class BrowserUseInput(BaseModel):
    """Input for WriteFileTool."""

    instruction: str = Field(..., description="The instruction to use browser")


class BrowserTool(BaseTool):
    name: ClassVar[str] = "browser"
    args_schema: Type[BaseModel] = BrowserUseInput
    description: ClassVar[str] = (
        "Use this tool to interact with web browsers. Input should be a natural language description of what you want to do with the browser, such as 'Go to google.com and search for browser-use', or 'Navigate to Reddit and find the top post about AI'."
    )

    _agent: Optional[BrowserAgent] = None

    def _run(self, instruction: str) -> str:
        generated_gif_path = f"{BROWSER_HISTORY_DIR}/{uuid.uuid4()}.gif"
        """Run the browser task synchronously."""
        self._agent = BrowserAgent(
            task=instruction,  # Will be set per request
            llm=vl_llm,
            browser=expected_browser,
            # TODO: 生成gif的时候总是失败，不知道为什么？
            # generated_gif_path=generated_gif_path,
        )
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                result = loop.run_until_complete(self._agent.run())
                return (
                    str(result)
                    if not isinstance(result, AgentHistoryList)
                    else result.final_result
                )
            finally:
                loop.close()
        except Exception as e:
            return f"Error executing browser task: {str(e)}"

    async def _arun(self, instruction: str) -> str:
        """Run the browser task asynchronously."""
        self._agent = BrowserAgent(
            task=instruction, llm=vl_llm  # Will be set per request
        )
        try:
            result = await self._agent.run()
            return (
                str(result)
                if not isinstance(result, AgentHistoryList)
                else result.final_result
            )
        except Exception as e:
            return f"Error executing browser task: {str(e)}"


BrowserTool = create_logged_tool(BrowserTool)
browser_tool = BrowserTool()
