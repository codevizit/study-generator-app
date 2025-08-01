# logic.py

from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser, PydanticOutputParser
from pydantic import BaseModel, Field
from typing import List
import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

model = ChatOpenAI(
    model="llama3-70b-8192",
    openai_api_key=GROQ_API_KEY,
    openai_api_base="https://api.groq.com/openai/v1"
)

parser = StrOutputParser()

### Prompt & Chain: Notes
prompt_notes = PromptTemplate(
    template="Generate short and simple notes from the following text:\n\n{text}",
    input_variables=["text"]
)
notes_chain = prompt_notes | model | parser

### Prompt & Chain: Quiz
prompt_quiz = PromptTemplate(
    template="Generate 5 short question-answer pairs from the following text:\n\n{text}",
    input_variables=["text"]
)
quiz_chain = prompt_quiz | model | parser

### Prompt & Chain: Flashcards
class Flashcard(BaseModel):
    term: str = Field(description="The key term or concept")
    definition: str = Field(description="The explanation or definition of the term")

class FlashcardList(BaseModel):
    flashcards: List[Flashcard]

flashcard_parser = PydanticOutputParser(pydantic_object=FlashcardList)

prompt_flashcards = PromptTemplate(
    template="Extract 5 important terms and their definitions from the text below. Format them as flashcards.\n\n{text}\n\n{format_instructions}",
    input_variables=["text"],
    partial_variables={"format_instructions": flashcard_parser.get_format_instructions()}
)
flashcard_chain = prompt_flashcards | model | flashcard_parser

### Prompt & Chain: Summary
prompt_summary = PromptTemplate(
    template="Generate a short and concise summary of the following text:\n\n{text}",
    input_variables=["text"]
)
summary_chain = prompt_summary | model | parser

### Exported functions
def generate_notes(text: str) -> str:
    return notes_chain.invoke({"text": text})

def generate_quiz(text: str) -> str:
    return quiz_chain.invoke({"text": text})

def generate_summary(text: str) -> str:
    return summary_chain.invoke({"text": text})

def generate_flashcards(text: str) -> List[Flashcard]:
    return flashcard_chain.invoke({"text": text}).flashcards
