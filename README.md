# Research Agent System Documentation

## Overview

The Research Agent System is a multi-agent framework designed to perform comprehensive research by decomposing complex queries into manageable sub-questions, conducting web searches, and consolidating findings into coherent reports. The system uses a hierarchical approach with specialized agents for different research tasks.

## Architecture

The system consists of three main components:

1. **Orchestration Agent** - Coordinates the overall research process
2. **Decomposition Agent** - Breaks down complex queries into strategic sub-questions
3. **Summarization Agent** - Consolidates findings into comprehensive reports

## Dependencies

```python
from agents import Agent, OpenAIProvider, Runner, OpenAIChatCompletionsModel, function_tool, set_tracing_disabled
from openai import AsyncOpenAI, OpenAI
import os
from dotenv import load_dotenv, find_dotenv
from tavily import TavilyClient
import json
import re
```

## Environment Variables

The following environment variables must be set:

- `GEMINI_API_KEY` - API key for Gemini models
- `OPENAI_API_KEY` - OpenAI API key (if using OpenAI models)
- `TAVILY_API_KEY` - API key for Tavily web search service

## Core Components

### 1. Web Search Function

```python
@function_tool
def search_web(query: str) -> str
```

**Purpose**: Performs web searches using the Tavily search API.

**Parameters**:
- `query` (str): The search query string

**Returns**: 
- Formatted string containing search results with title, URL, and content

**Features**:
- Retrieves up to 5 search results per query
- Formats results in a structured format
- Handles errors gracefully

### 2. Summarization Agent

```python
@function_tool
async def summarize_agent(sub_questions)
```

**Purpose**: Consolidates multiple question-answer pairs into a comprehensive, well-structured summary.

**Key Features**:
- Uses Gemini 2.5 Flash model for summarization
- Integrates findings into coherent narratives
- Maintains academic/professional tone
- Creates 200-400 word comprehensive paragraphs

**Requirements**:
- **Integration**: Synthesizes all answers into coherent narrative
- **Comprehensiveness**: Captures all key insights
- **Coherence**: Creates smooth transitions between aspects
- **Prioritization**: Emphasizes critical findings
- **Evidence**: Preserves supporting data points
- **Balance**: Gives appropriate weight to different perspectives

### 3. Decomposition Agent

```python
@function_tool
async def decomposing_agent(query)
```

**Purpose**: Breaks down complex research queries into 8-12 strategic sub-questions.

**Process**:
1. Analyzes the main research query
2. Creates comprehensive sub-questions covering all major aspects
3. Searches for answers using the web search tool
4. Compiles question-answer pairs
5. Passes results to summarization agent

**Sub-question Criteria**:
- Clear and specific question statements
- Answerable with available evidence
- Comprehensive coverage of the main query
- Strategic sequencing for efficient investigation
- Multiple stakeholder perspectives

### 4. Main Research Function

```python
def researcher_Agent(query)
```

**Purpose**: Main entry point that orchestrates the entire research process.

**Process Flow**:
1. Receives research query
2. Decomposes query into sub-questions
3. Performs searches on each sub-question
4. Summarizes results using the summarization agent
5. Formats output as a detailed formal research report

## Usage

### Basic Usage

```python
# Perform comprehensive research
result = researcher_Agent("What are the impacts of artificial intelligence on healthcare?")
print(result)
```

### Configuration

The system uses Gemini 2.5 Flash model by default:
- **Base URL**: `https://generativelanguage.googleapis.com/v1beta/openai/`
- **Model**: `gemini-2.5-flash`

## Output Format

The system generates formal research reports with:
- Executive summary
- Detailed findings from sub-questions
- Consolidated analysis
- Supporting evidence and data points
- Multiple stakeholder perspectives

## Error Handling

- Web search errors are caught and returned as formatted error messages
- Environment variable validation through dotenv
- Graceful handling of API failures


## Example Research Flow

1. **Input**: "What are the ethical implications of AI in education?"
2. **Decomposition**: Creates sub-questions about privacy, bias, accessibility, etc.
3. **Search**: Performs web searches for each sub-question
4. **Consolidation**: Synthesizes findings into comprehensive report
5. **Output**: Formal research report with integrated findings

## Troubleshooting

### Common Issues

1. **API Key Errors**: Verify all environment variables are set correctly
2. **Search Failures**: Check Tavily API key and internet connectivity
3. **Model Errors**: Ensure Gemini API key is valid and has sufficient quota
4. **Import Errors**: Verify all required packages are installed
