import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Reasoning LLM configuration (for complex reasoning tasks)
REASONING_MODEL = os.getenv("REASONING_MODEL", "o1-mini")
REASONING_BASE_URL = os.getenv("REASONING_BASE_URL")
REASONING_API_KEY = os.getenv("REASONING_API_KEY")

# Non-reasoning LLM configuration (for straightforward tasks)
BASIC_MODEL = os.getenv("BASIC_MODEL", "gpt-4o")
BASIC_BASE_URL = os.getenv("BASIC_BASE_URL")
BASIC_API_KEY = os.getenv("BASIC_API_KEY")

# Vision-language LLM configuration (for tasks requiring visual understanding)
VL_MODEL = os.getenv("VL_MODEL", "gpt-4o")
VL_BASE_URL = os.getenv("VL_BASE_URL")
VL_API_KEY = os.getenv("VL_API_KEY")

# Chrome Instance configuration
CHROME_INSTANCE_PATH = os.getenv("CHROME_INSTANCE_PATH")
CHROME_HEADLESS = True if os.getenv("CHROME_HEADLESS") in ["True", "true", "1"] else False
CHROME_PROXY_SERVER = os.getenv("CHROME_PROXY_SERVER", None)
CHROME_PROXY_USERNAME = os.getenv("CHROME_PROXY_USERNAME", None)
CHROME_PROXY_PASSWORD = os.getenv("CHROME_PROXY_PASSWORD", None)
# Browser History Directory
BROWSER_HISTORY_DIR = os.getenv("BROWSER_HISTORY_DIR", "./logs/browser_history")

# Langfuse
LANGFUSE_SECRET_KEY = os.getenv("LANGFUSE_SECRET_KEY", None)
LANGFUSE_PUBLIC_KEY = os.getenv("LANGFUSE_PUBLIC_KEY", None)
LANGFUSE_HOST = os.getenv("LANGFUSE_HOST", "http://47.113.151.33:3000")
