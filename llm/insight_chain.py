# llm/insight_chain.py

import os
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

from llm.prompts import INSIGHT_PROMPT


class InsightChain:
    """
    LangChain-based insight generation layer.

    Responsibilities:
    - Configure the LLM (OpenRouter / OpenAI-compatible)
    - Bind structured business statistics to a prompt
    - Generate natural-language insights safely and deterministically

    This class intentionally hides LangChain internals from the UI layer.
    """

    def __init__(self):
        """
        Initialize the LLM using environment variables.
        Required env vars:
        - OPENROUTER_API_KEY
        Optional:
        - OPENROUTER_MODEL (defaults to mistral)
        """

        api_key = os.getenv("OPENROUTER_API_KEY")
        if not api_key:
            raise ValueError(
                "OPENROUTER_API_KEY not found in environment variables"
            )

        model = os.getenv(
            "OPENROUTER_MODEL",
            "mistralai/mistral-7b-instruct"
        )

        self.llm = ChatOpenAI(
            api_key=api_key,
            base_url="https://openrouter.ai/api/v1",
            model=model,
            temperature=0.2,
        )

        # Prompt → LLM chain
        self.chain = INSIGHT_PROMPT | self.llm

    def run(self, statistics: dict, question: str) -> str:
        """
        Generate a business insight from structured statistics.

        Parameters
        ----------
        statistics : dict
            Output from StatsRetriever.as_dict()
        question : str
            User's natural language question

        Returns
        -------
        str
            LLM-generated insight
        """

        response = self.chain.invoke(
            {
                "statistics": statistics,
                "question": question,
            }
        )

        # Always return clean text
        return response.content.strip()
