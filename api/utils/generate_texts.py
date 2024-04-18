from typing import List

import requests
from bs4 import BeautifulSoup
from decouple import config
from langchain.chains.summarize import load_summarize_chain
from langchain.prompts import PromptTemplate
from langchain.text_splitter import CharacterTextSplitter
from langchain_core.documents import Document
from langchain_openai import OpenAI

from .constants import company, company_information, sales_rep

openai_api_key = config('OPENAI_API_KEY')


def format_company_name(company_name: str) -> str:
    """
    Function to change company name to match ycombinator URL format
    makes lowercase, and replaces . or space with "-".

    Args: 
        str: company name

    Returns: 
        str: formatted company name
    """

    modified_company_name = company_name.replace(
        ".", "-").replace(" ", "-").lower()
    return modified_company_name


def get_company_page(company_name: str) -> str:
    """
    Function to return correct company URL, formatted for Y Combinator.
    Args: 
        str: company name

    Returns: 
        str: Y Combinator-compatible URL
    """
    company_path = format_company_name(company_name)
    y_combinator_url = f"https://www.ycombinator.com/companies/{company_path}"

    return y_combinator_url


def split_string(text: str, num_chunks: int = 2) -> str:
    """
    Function to add newlines to a string to create the desired number of chunks
    so that CharacterTextSplitter won't make 1,000 documents since it cuts by newlines

    Args: 
        str: text, company about text
        int: num_chunks, desired number of documents

    Returns: 
        str: formatted company about text
    """

    chunk_length_index = len(text) // num_chunks

    for i in range(num_chunks - 1):
        # this part finds the closest place there is a whitespace to avoid breaking up words
        space_index = text.rfind(' ', 0, chunk_length_index)
        if space_index == -1:
            text = text[:chunk_length_index] + '\n' + text[chunk_length_index:]
        else:
            text = text[:space_index] + '\n' + text[space_index:]
        chunk_length_index += chunk_length_index
        # finish the loop early if the next iteration would go out of bounds of the string
        if (len(text) - chunk_length_index) < 0:
            break
    return text


def generate_docs(company_name: str) -> List[Document] | List:
    """
    Function to generate docs that contain chunks of company information to avoid running into token limits

    Note that this function currently only works with Y Combinator companies.

    The reasoning for this is that Y Combinator has a good database of data about
    startups, so it is very useful.

    Ideally, this function would have subfunctions to investigate different
    sources if a YCombinator address isn't found.

    Args:
        str: company name

    Returns: 
        a list of Document objects if a URL is found, otherwise an empty list

    Raises: 
        Exception if company url is not found or if there is an error creating documents.
    """
    company_url = get_company_page(company_name)
    response = requests.get(company_url)
    soup = BeautifulSoup(response.content, "html.parser")

    # This works because the element "whitespace-pre-line" that contains the
    # company "about us" section is always first on the page
    inner_text = None
    try:
        element = soup.select_one(
            ".whitespace-pre-line")
        if element:
            inner_text = element.get_text(strip=True)
    except:
        raise Exception(company_url)

    # If any element is found, then create Documents from its contained text.
    if inner_text:
        try:
            doc_creator = CharacterTextSplitter(chunk_size=800, separator="\n")
            inner_text = split_string(inner_text)
            inner_text = doc_creator.split_text(inner_text)
            docs = doc_creator.create_documents(texts=inner_text)
            return docs
        except:
            raise Exception("Error creating documents about company.")
    else:
        return []


def generate_about_text() -> PromptTemplate:
    """
    Function to create a prompt template regarding a summary of company information.

    Args: 
        None (though text variables come from Langchain's chain)

    Returns: 
        PromptTemplate with company information.
    """
    map_prompt = """Below is a section of a website about {prospect}

  Write a concise summary about {prospect}. If the information is not about {prospect}, exclude it from your summary.

  {text}

  % CONCISE SUMMARY:"""
    map_prompt_template = PromptTemplate(
        template=map_prompt, input_variables=["text", "prospect"])
    return map_prompt_template


def generate_email_text() -> PromptTemplate:
    """
    Function to generate a template for prompting the llm about emails

    Ideally I would add that if for some reason we couldn't find data about
    the target company, we would use a different prompt, instructing the LLM 
    to write a more generic sales email based on the company emailing them.

    Args: 
        None (though text variables come from Langchain's chain)

    Returns: 
        PromptTemplate with company information.
    """
    combine_prompt = """
  Your goal is to write a personalized outbound email from {sales_rep}, a sales rep at {company} to {point_of_contact}, the {job_role} at {prospect}.

  A good email is personalized and combines information about the two companies on how they can help each other.
  Be sure to use value selling: A sales methodology that focuses on how your product or service will provide value to the customer instead of focusing on price or solution.

  % INFORMATION ABOUT {company}:
  {company_information}

  % INFORMATION ABOUT {prospect}:
  {text}

  % INCLUDE THE FOLLOWING PIECES IN YOUR RESPONSE:
  - Start the email with the sentence: "We love that {prospect} helps teams..." then insert what they help teams do.
  - The sentence: "We can help you do XYZ by ABC" Replace XYZ with what {prospect} does and ABC with what {company} does 
  - A 1-2 sentence description about {company}, be brief
  - End your email with a call-to-action such as asking them to set up time to talk more

  % DO NOT INCLUDE THE FOLLOWING PIECES IN YOUR RESPONSE:
  - Email subject line

  % YOUR RESPONSE:
  """
    combine_prompt_template = PromptTemplate(template=combine_prompt, input_variables=["sales_rep", "company", "prospect",
                                                                                       "text", "company_information", "point_of_contact", "job_role"])
    return combine_prompt_template


def final_email(prospect_name: str, point_of_contact: str, job_role: str) -> str:
    """
    Function to summarize information via Langchain feed to OpenAI's API.

    Args: 
        str: prospect_name, target company's name
        str: point_of_contact, name of person you are contacting
        str: job_role, point of contact's job title
    Returns: 
        Str with summarized email results.
    """

    # This calls OpenAI's large language model since I do not have my own trained model
    llm = OpenAI(temperature=.7, openai_api_key=openai_api_key,
                 max_tokens=1024)

    # Langchains' method for summarizing a chain of documents
    chain = load_summarize_chain(llm,
                                 chain_type="map_reduce",
                                 map_prompt=generate_about_text(),
                                 combine_prompt=generate_email_text(),
                                 verbose=True
                                 )
    # This feeds our different data and variables to the chain that are used in the chained prompts
    output = chain({"input_documents": generate_docs(prospect_name),  # The seven docs that were created before
                    "company": company, \
                    "company_information": company_information, \
                    "sales_rep": sales_rep, \
                    "prospect": prospect_name, \
                    "point_of_contact": point_of_contact, \
                    "job_role": job_role
                    })

    # return the final email text without trailing whitespaces and newlines
    return output['output_text'].rstrip()
