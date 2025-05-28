import os
from dotenv import load_dotenv
import wolframalpha

load_dotenv()
WOLFRAM_API_KEY = os.getenv("WOLFRAM_ALPHA_APPID")

async def wolfram_tool(query:str) -> dict:
    """Use Wolfram Alpha to solve math or science-related questions."""
    
    wolfram_client = wolframalpha.Client(WOLFRAM_API_KEY)
    try:
        res = await wolfram_client.aquery(query)
        return {"result":res}
    except Exception as e:
        return {"error": f"Wolfram Alpha tool error: {e}"}