from agents import Agent, OpenAIProvider, Runner, OpenAIChatCompletionsModel, function_tool, set_tracing_disabled
from openai import AsyncOpenAI, OpenAI
import os
from dotenv import load_dotenv, find_dotenv
from tavily import TavilyClient
import json
import re

from agents_def_orig import summarize_agent

load_dotenv(find_dotenv())
gemini_key = os.environ.get("GEMINI_API_KEY")
base_url = "https://generativelanguage.googleapis.com/v1beta/openai/"

openai_api_key = os.environ.get("OPENAI_API_KEY")


@function_tool
def search_web(query: str) -> str:
    """Search the web using Tavily"""
    try:
        tavily_client = TavilyClient(api_key=os.environ.get("TAVILY_API_KEY"))
        response = tavily_client.search(query, max_results=5)
        
        # Format the results nicely
        results = []
        for result in response.get('results', []):
            results.append(f"Title: {result.get('title', 'N/A')}\nURL: {result.get('url', 'N/A')}\nContent: {result.get('content', 'N/A')}\n")
        
        return "\n---\n".join(results)
    except Exception as e:
        return f"Search error: {str(e)}"


@function_tool
async def summarize_agent(sub_questions):
    print("consolidate agent************")

    provider:AsyncOpenAI = AsyncOpenAI(api_key=gemini_key, base_url = "https://generativelanguage.googleapis.com/v1beta/openai/")
    llm_model:OpenAIChatCompletionsModel = OpenAIChatCompletionsModel(model="gemini-2.5-flash", openai_client=provider)


    conolidate_agent: Agent = Agent(name="conolidate_agent", 
                                model=llm_model,
                                tools=[search_web]
                                )

    consolodate_prompt = """
    summarize the following question-answer pairs into one comprehensive, well-structured paragraph that addresses the overarching research question: "{main_research_question}"

**Sub questions :**
{sub_questions}

**summarization Requirements:**
1. INTEGRATION: Synthesize all answers into a coherent narrative that flows logically
2. COMPREHENSIVENESS: Ensure all key insights from individual answers are captured
3. COHERENCE: Create smooth transitions between different aspects/perspectives
4. PRIORITIZATION: Emphasize the most critical findings while maintaining completeness
5. EVIDENCE: Preserve important supporting evidence and data points
6. BALANCE: Give appropriate weight to different perspectives and findings

**Output Guidelines:**
- Write as ONE comprehensive paragraph (200-400 words)
- Start with a clear topic sentence that addresses the main question
- Use transitional phrases to connect different insights
- Maintain academic/professional tone
- Avoid redundancy while ensuring completeness
- End with a concluding statement that ties everything together

**Structure the paragraph to:**
- Begin with primary findings/conclusions
- Present supporting evidence and analysis
- Address different stakeholder perspectives
- Include implementation considerations
- Conclude with synthesis and implications

Consolidate now:
    """

   # response = Runner.run_sync(general_agent,consolodate_prompt)
   # conolidate_agent.instructions=consolodate_prompt
    
    return Runner.run(summarize_agent,consolodate_prompt)

@function_tool
async def decomposing_agent(query):
    print("decompose agent************")
    provider = AsyncOpenAI(api_key=gemini_key, base_url=base_url)
    model = OpenAIChatCompletionsModel(model="gemini-2.5-flash", openai_client=provider)
    agent = Agent(name="Decomposition Agent", model = model, tools=[search_web, summarize_agent])
    
    """Intelligent decomposition into prioritized sub-questions"""
        
    decomposition_prompt = f"""
    Decompose this research query into strategic sub-questions:
    
    Main Query: "{query}"
    
    
    Create 8-12 sub-questions that:
    
    1. COVERAGE REQUIREMENTS:
        - Address all major aspects of the main question
        - Cover different stakeholder perspectives
        - Include foundational and advanced questions
        - Balance breadth and depth appropriately
    
    
    
    Ensure questions are:
    - Clear, specific question statement
    - Answerable with available evidence
    - Specific enough to guide research
    - Comprehensive enough to address the main query
    - Strategically sequenced for efficient investigation
    
    """


    decomposition_prompt += """
           once u have the sub questions, search answers using search web tool.
           add questions answers pairs to your response.
           pass the your response to consolidate agent tool and add its output to your response as a separate heading
    
    
    """
    response = await Runner.run(agent, input = decomposition_prompt)
    return response.final_output


def researcher_Agent(query):

    provider = AsyncOpenAI(api_key=gemini_key, base_url = "https://generativelanguage.googleapis.com/v1beta/openai/")
    model = OpenAIChatCompletionsModel(model="gemini-2.5-flash", openai_client=provider)
    orcheastrate_agent = Agent(model=model, name = "orcheastrate_agent", tools=[search_web,
         decomposing_agent,summarize_agent
         
              ])

    response =  Runner.run_sync(orcheastrate_agent,
     f""" perform a deep research on {query},
    1. Decompose query into sub question and perform search on each sub question
    2.  summarize results using summarize_agent agent
    format your response as a detailed formal research report
    """,
    
     )
    print(response.final_output)
    return response.final_output

