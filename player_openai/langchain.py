# """
# https://zenn.dev/umi_mori/books/prompt-engineer/viewer/langchain_overview
# """
from typing import List
from dotenv import load_dotenv
load_dotenv()
import os
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

from langchain_core.output_parsers import StrOutputParser
from langchain.output_parsers import PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from pydantic import BaseModel
from typing import Type, Literal

from langchain_core.runnables.utils import Input
from typing import Literal

class OpenAIAgent():
    def __init__(self, model_name = "gpt-4o", temperature = 0) -> None:
        # OpenAIのモデルのインスタンスを作成
        self.llm = ChatOpenAI(model_name=model_name, temperature=temperature)
        self.json_llm = self.llm.bind(response_format={"type": "json_object"})
    
    def chat(self, system: str, template: Literal["f-string", "mustache"], input: Input) -> str:
        output_parser = StrOutputParser()

        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", "{system}"),
                ("human", "{template}"),
            ]
        )

        chain = prompt | self.llm | output_parser

        return chain.invoke({"system": system.format(**input), "template": template.format(**input)})

    def json_mode_chat(self, system: str, template: Literal["f-string", "mustache"], input: Input, pydantic_object: Type[BaseModel]) -> dict:
        output_parser = PydanticOutputParser(pydantic_object=pydantic_object)

        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "{system}\nAnswer the user query. Wrap the output in `json` tags\n{format_instructions}",
                ),
                ("human", "{template}"),
            ]
        ).partial(format_instructions=output_parser.get_format_instructions())

        chain = prompt | self.json_llm | output_parser

        return chain.invoke({"system": system.format(**input), "template": template.format(**input)})
