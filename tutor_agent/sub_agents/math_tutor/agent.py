from google.adk.agents import ParallelAgent, SequentialAgent

from .sub_agents.google_search_agent import google_search_agent
from .sub_agents.wolfram_agent import wolfram_agent
from .sub_agents.synthesizer import synthesizer_agent


info_gatherer = ParallelAgent(
    name="Math_info_gatherer",
    sub_agents=[google_search_agent, wolfram_agent]
)

math_agent = SequentialAgent(
    name="Math_Tutor_Agent",
    sub_agents=[info_gatherer, synthesizer_agent]
)