# In your main.py filfrom agents import Agent, Runner, OpenAIChatCompletionsModel, function_tool
import asyncio

import agents_group
import json_to_pdf

def main():
  response =   agents_group.researcher_Agent("What is renewable energy")
  json_to_pdf.text_to_pdf(response, "research.pdf")

if __name__ == "__main__":
    (main())