from phi.agent import Agent
from phi.model.ollama import Ollama
from phi.model.groq import Groq
from phi.model.huggingface import HuggingFaceChat
from transformers import pipeline
from dotenv import load_dotenv
from langdetect import detect, detect_langs
import re
import json
from typing import List, Union, Optional

# Load environment variables
load_dotenv()

# Initialize the translation pipeline
# translation_pipeline = pipeline(
#     "translation", model="facebook/m2m100_418M", tokenizer="facebook/m2m100_418M"
# )
# translation_pipeline = pipeline("translation", model="facebook/m2m100_418M")
# translation_pipeline = pipeline("translation", model="facebook/m2m100_418M")
translation_pipeline = pipeline("translation", model="facebook/mbart-large-50-many-to-many-mmt")

def detect_and_parse_json(input_string):

    def preprocess_json_fragment(fragment):
        """
        Cleans and normalizes a JSON fragment to make it valid.
        """
        # Remove backticks and unnecessary characters
        fragment = fragment.strip("` ")

        # Replace single quotes with double quotes
        fragment = re.sub(r"(?<!\\)'", '"', fragment)

        # Ensure all keys are quoted (keys that are words without quotes)
        fragment = re.sub(r'(\b\w+\b)(?=\s*:)', r'"\1"', fragment)

        # Handle inline fraction-like scores (e.g., 10/15) by wrapping them in quotes
        fragment = re.sub(r'(\d+/\d+)', r'"\1"', fragment)

        # Fix trailing commas (remove extra commas before closing brackets/braces)
        fragment = re.sub(r",\s*([\}\]])", r"\1", fragment)

        return fragment.strip()

    def is_valid_json(fragment):
        """
        Attempt to validate if a string fragment is a valid JSON object or array.
        """
        try:
            json.loads(fragment)
            return True
        except json.JSONDecodeError:
            return False

    def extract_json_fragments(input_string):
        """
        Extract potential JSON objects or arrays from the string.
        This pattern looks for balanced braces `{}` or brackets `[]`, 
        and can handle multiple JSON structures in the input.
        """
        # Look for JSON-like structures wrapped in `{}` or `[]`
        json_pattern = re.compile(r'(\{.*?\}|\[.*?\])', re.DOTALL)
        return json_pattern.findall(input_string)

    # Extract potential JSON fragments from the input string
    potential_fragments = extract_json_fragments(input_string)

    if not potential_fragments:
        return None

    valid_jsons = []
    for fragment in potential_fragments:
        # Preprocess and clean the fragment
        cleaned_fragment = preprocess_json_fragment(fragment)
        
        # Validate and collect the valid JSON objects or arrays
        if is_valid_json(cleaned_fragment):
            try:
                # Attempt to parse the fragment into a JSON object
                valid_jsons.append(json.loads(cleaned_fragment))
            except json.JSONDecodeError:
                continue

    # If no valid JSONs found, return None
    return valid_jsons if valid_jsons else None


def detect_and_parse_json2(input_string):
    def preprocess_json_fragment(fragment):
        """
        Cleans and normalizes a JSON fragment to make it valid.
        """
        # Remove backticks and unnecessary characters
        fragment = fragment.strip("` ")

        # Replace single quotes with double quotes
        fragment = re.sub(r"(?<!\\)'", '"', fragment)

        # Ensure all keys are quoted (keys that are words without quotes)
        fragment = re.sub(r'(\b\w+\b)(?=\s*:)', r'"\1"', fragment)

        # Handle inline fraction-like scores (e.g., 10/15) by wrapping them in quotes
        fragment = re.sub(r'(\d+/\d+)', r'"\1"', fragment)

        # Fix trailing commas (remove extra commas before closing brackets/braces)
        fragment = re.sub(r",\s*([\}\]])", r"\1", fragment)

        return fragment.strip()

    def is_valid_json(fragment):
        """
        Attempt to validate if a string fragment is a valid JSON object or array.
        """
        try:
            json.loads(fragment)
            return True
        except json.JSONDecodeError:
            return False

    def extract_json_fragments(input_string):
        """
        Extract potential JSON objects or arrays from the string.
        This pattern looks for balanced braces `{}` or brackets `[]`, 
        and can handle multiple JSON structures in the input.
        """
        # Look for JSON-like structures wrapped in `{}` or `[]`
        json_pattern = re.compile(r'(\{.*?\}|\[.*?\])', re.DOTALL)
        return json_pattern.findall(input_string)

    # Extract potential JSON fragments from the input string
    potential_fragments = extract_json_fragments(input_string)

    if not potential_fragments:
        return None

    valid_jsons = []
    for fragment in potential_fragments:
        # Preprocess and clean the fragment
        cleaned_fragment = preprocess_json_fragment(fragment)
        
        # Validate and collect the valid JSON objects or arrays
        if is_valid_json(cleaned_fragment):
            try:
                # Attempt to parse the fragment into a JSON object
                valid_jsons.append(json.loads(cleaned_fragment))
            except json.JSONDecodeError:
                continue

    # If no valid JSONs found, return None
    return valid_jsons if valid_jsons else None

import regex
def extract_json_from_string(input_string):
    """
    Extracts valid JSON objects or arrays from an unstructured string using recursive regex.
    
    Args:
        input_string (str): The input string containing unstructured text and possible JSON.
    
    Returns:
        list: A list of extracted JSON objects or arrays as Python dictionaries or lists.
    """
    json_objects = []
    
    # Recursive regex pattern to capture JSON objects or arrays
    json_pattern = r'(\{(?:[^{}]++|(?R))*\}|\[(?:[^\[\]]++|(?R))*\])'
    
    try:
        # Find all potential JSON substrings in the input string
        matches = regex.findall(json_pattern, input_string, regex.DOTALL)
        
        for match in matches:
            match = match.strip()  # Remove extra spaces or newlines
            
            try:
                # Try to parse the matched substring as JSON
                parsed_json = json.loads(match)
                json_objects.append(parsed_json)
            except json.JSONDecodeError:
                # Ignore invalid JSON matches
                continue
        
    except Exception as e:
        print("Error : Failed to extract JSON. Reason: "+str(e))
        return None

    return json_objects

def detect_language(text):
    """
    Detects the language of the given text.
    
    Args:
        text (str): Input text for language detection.
    
    Returns:
        str: Detected language code (e.g., 'en' for English, 'fr' for French).
    """
    language = detect(text)  # Returns the language code
    return language

def translate_to_english(text, source_language):
    """
    Translates the input text to English if it's not already in English.
    
    Args:
        text (str): The input text to translate.
        source_language (str): The source language of the text (e.g., 'fr' for French, 'es' for Spanish).
    
    Returns:
        str: Translated text in English.
    """
    if source_language.lower() == "en":
        return text  # No translation needed
    return translation_pipeline(text, src_lang=source_language, tgt_lang="en")[0]["translation_text"]

def process_resume(cv_text):
    """
    Processes CV text to organize it into structured sections.
    
    Args:
        cv_text (str): Plain text extracted from the CV.
        language (str): Language of the CV text. Default is 'en' (English).
        
    Returns:
        str: JSON response containing organized CV sections.
    """
    language=detect_language(cv_text)
    # Translate to English if necessary
    # if language.lower() != "en":
    
    cv_text = translate_to_english(cv_text, language)

    # Initialize the HR agent
    hr_agent = Agent(
        name="HR Resume Processing Agent",
        # model=Ollama(id="llama2-13b"),  # LLM for processing and structuring text
        # model=Groq(id='llama3-8b-8192'),
        model=Groq(id='gemma2-9b-it'),
        description="You are an HR assistant specializing in processing resumes to extract and organize information into structured sections for review ,ranking and screening the resumes",
        instructions=[
            "You are a resume processing agent specializing in extracting structured information from plain text of CVs.",
            "Organize the information into the following sections:",
            "- Extract contact details: Collect contact information (emails, phone, location) if mentioned any."
            "- Work Experience: Extract information about jobs, roles, and durations if mentioned any.",
            "- Project Experience: Extract and Summarize any projects or assignments mentioned including technologies used and outcomes if mentioned any.",
            "- Research: Include publications, studies, and other scholarly work if mentioned any.",
            "- Academic Achievements: Extract awards, scholarships, or notable academic accolades if mentioned any.",
            "- Education: Summarize educational qualifications with degrees, institutions, and durations if mentioned any.",
            "- Skills and Certifications: Extract technical, soft, and domain-specific skills, certificates, and qualifications if mentioned any.",
            "- Recognize achievements: Identify quantifiable achievements and notable accomplishments from work history if mentioned any."
            "- Social Work/Volunteer: Include community service or voluntary activities if mentioned any.",
            "- Reference: Include references if mentioned any."
            "- Other Section: Include any other mentionable section from the text which is not given in instructions or missed.",
            "Do not add anything from your own,out of the given plain text.",
            "Respond in JSON format as shown in this example:",
            '''
            {   "Contact Details":[List information like Name, Phone, Email, Address, if given other wise return Not mentioned.],
                "Work Experience": ["List information such as Software Engineer Intern at ABC Corp, 2021-2022 if given other wise return Not mentioned"],
                "Project Experience": ["List information about any application or project information available if given other wise return Not mentioned"],
                "Research": ["List information such as Published paper or ongoing research, if given other wise return Not mentioned"],
                "Academic Achievements": ["List the academic achivements/Awards, if given other wise return Not mentioned"],
                "Education": ["List information such as Bachelor, University, Higher Secondary, Secondary, if mentioned."],
                "Skills and Certifications": ["List information about skills and certifications, if given other wise return Not mentioned"],
                "Recognized Achievements":["list the work or other recognized achivements if there any"],
                "Social Work/Volunteer": ["List the information about Volunteery or social work  if given other wise return Not mentioned"],
                "Reference": ["Include references if mentioned any"]
                "Other Section": ["Include any other mentionable section which is not given in instructions or missed"]
            }
            '''
        ],
        markdown=True,
    )

    # Process the (translated) CV text
    result = hr_agent.run(cv_text)
    raw_info= result.content
    # parsed_json =detect_and_parse_json2(raw_info)
    cleaned_text = raw_info.replace("\n", " ")
    parsed_json=extract_json_from_string(cleaned_text)
    if parsed_json:
        return parsed_json
    else:
        # return raw_info

        # json_text=json.dumps(parsed_json, indent=4)
        pattern = r"```(.*?)```"
        match = re.search(pattern, cleaned_text, re.DOTALL)
        
        if match:
            try:
                json_data= match.group(1).strip()
                result=json.loads(json_data)
                return result
            except Exception as e:
                print("Error in JSON: "+str(e))
                return cleaned_text
        else:
            return cleaned_text



def score_resume(cv_text,job_description):
    """
    Processes CV text to organize it into structured sections.
    
    Args:
        cv_text (str): Plain text extracted from the CV.
        language (str): Language of the CV text. Default is 'en' (English).
        
    Returns:
        str: JSON response containing organized CV sections.
    """
    # language=detect_language(cv_text)
    # Translate to English if necessary
    # if language.lower() != "en":
    
    # cv_text = translate_to_english(cv_text, language)

    # Initialize the HR agent
    scoring_agent = Agent(
        name="HR Resume Scoring Agent",
        # model=Groq(id='llama3-8b-8192'),  # Replace with your desired LLM model
        # model=HuggingFaceChat(id="deepseek-ai/DeepSeek-R1-Distill-Llama-8B"),
        model=Groq(id='gemma2-9b-it'),
        description="You are an HR assistant specializing in processing resumes to evaluate their compatibility with job descriptions. Your primary task is to compare the details in resumes against the job requirements and calculate a score out of 100.",
        instructions=[
            "You are an AI-powered HR assistant designed to compare resumes with job descriptions and assess compatibility based on specific criteria.",
            "The compatibility score should be calculated out of 100, based on the following weightage:",
            "- **Educational qualification check (15%)**: Verify if education meets minimum requirements and preferred qualifications.",
            "- **Work Experience level assessment (30%)**: Evaluate years of relevant experience and seniority levels in previous roles.",
            "- **Skills matching (25%)**: Match technical, domain-specific, and soft skills with job requirements.",
            "- **Project and Research Experience (15%)**: Match relevance to job responsibilities, technologies used, and outcomes.",
            "- **Gap analysis (5%)**: Identify and assess any career gaps, looking for explanations in Resume or cover letters.",
            "- **Job hopping detection(5%)**: Review employment duration patterns and consider context for short tenures.",
            "- **Achievement evaluation (5%)**: Assess the impact and relevance of listed achievements to the role.",
            "Use the resume text and job description provided to calculate the score.",
            "Provide the following output format Strictly only in JSON format: (No other text except JSON.)",
            '''
            {
                
                "Match_Analysis": {
                    "Educational qualification check (15%)": "Give the score on the basis of Educational requirements out of 15 and explain why.",
                    "Work Experience level assessment (30%)": "Give the score on the basis of Work Experience out of 30 and explain why.",
                    "Skills matching (25%)": "Give the score on the basis of Skills matching out of 25 and explain why.",
                    "Project and Research Experience (15%)": "Give the score on the basis of Project and Research Experience out of 15 and explain why.",
                    "Gap analysis (5%)": "Give the score on the basis of Gap analysis out of 5 and explain why.",
                    "Job hopping detection(5%)": "Give the score on the basis of Job hopping detection it out of 5 and explain why.",
                    "Achievement evaluation (5%)": "Give the score on the basis of Achievement out of 5 and explain why."
                },
                "Compatibility_Score": **//100. The score will be the sum of all the match analysis score.
            }
            '''
        ],
        markdown=True,
    )


    # Process the (translated) CV text
    result = scoring_agent.run('Job Description: '+job_description+'\n\n'+'Resume Information: '+str(cv_text))
    raw_info= result.content
    # parsed_json =detect_and_parse_json2(raw_info)
    cleaned_text = raw_info.replace("\n", " ")
    parsed_json=extract_json_from_string(cleaned_text)
    if parsed_json:
        return parsed_json
    else:
        # return raw_info
        pattern = r"```(.*?)```"
        match = re.search(pattern, cleaned_text, re.DOTALL)
        
        if match:
            try:
                json_data= match.group(1).strip()
                result=json.loads(json_data)
                return result
            except Exception as e:
                print("Error in JSON: "+str(e))
                return cleaned_text
        else:
            return cleaned_text
    # json_text=json.dumps(parsed_json, indent=4)
    # cleaned_text = raw_info.replace("\n", " ")
    # json_value=detect_and_parse_json(cleaned_text)
    # cleaned_text = raw_info.replace("\\n", " ")
    # pattern = r"```(.*?)```"
    # match = re.search(pattern, raw_info, re.DOTALL)
    
    # if json_value:
    #     return json_value
    # elif match:
    #     try:
    #         json_data= match.group(1).strip()
    #         result=json.loads(json_data)
    #         return result
    #     except Exception as e:
    #         print("Error in JSON: "+str(e))
    #         return raw_info
    # else:
    #     return raw_info



def candidate_data(cv_text):
    """
    Processes CV text to organize it into structured sections.
    
    Args:
        cv_text (str): Plain text extracted from the CV.
        language (str): Language of the CV text. Default is 'en' (English).
        
    Returns:
        str: JSON response containing organized CV sections.
    """
    language=detect_language(cv_text)
    # Translate to English if necessary
    # if language.lower() != "en":
    
    cv_text = translate_to_english(cv_text, language)

    # Initialize the HR agent
    hr_agent = Agent(
        name="Contact information Retriever Agent",
        # model=Ollama(id="llama2-13b"),  # LLM for processing and structuring text
        # model=Groq(id='llama3-8b-8192'),
        model=Groq(id='gemma2-9b-it'),
        description="You are a Contact information Retriever Agent who can extract Contact data from CV text",
        instructions=[
            "You are a Contact information Retriever Agent who can extract Contact data such as Name, Phone Number Email and most recent company and designation from plain text of CVs.",
            "Organize the information into the following sections:",
            "- Name: Retrive the Name of the candidate which is most important.",
            "- Phone Number: Retrive the Phone Number of the candidate, number can be one or multiple, get all of them.",
            "- Email: Retrive the Email of the candidate, number can be one or multiple, get all of them.",
            "- Last Company: Retrive the most recent company Name of the candidate.",
            "- Designation: Retrive the most recent company Designation of the candidate.",
            
            "Do not add anything from your own,out of the given plain text.",
            "Respond in JSON format as shown in this example:",
            '''
            {   "Candidate Name ":"ABC DEF",
                "Phone Number": "***********",
                "Email": ["Email 1, Email 2"],
                "Last Company": "ABC Company",
                "Designation": "*********"
            }
            '''
        ],
        markdown=True,
    )

    # Process the (translated) CV text
    result = hr_agent.run(cv_text)
    raw_info= result.content
    # parsed_json =detect_and_parse_json2(raw_info)
    cleaned_text = raw_info.replace("\n", " ")
    parsed_json=extract_json_from_string(cleaned_text)
    if parsed_json:
        return parsed_json
    else:
        return raw_info
    

from rag_db import get_candidate_info
def normalize_data(email,query):
    """
    Processes CV text to organize it into structured sections.
    
    Args:
        cv_text (str): Plain text extracted from the CV.
        language (str): Language of the CV text. Default is 'en' (English).
        
    Returns:
        str: JSON response containing organized CV sections.
    """
    language=detect_language(query)
    # Translate to English if necessary
    # if language.lower() != "en":
    
    query = translate_to_english(query, language)

    data=get_candidate_info(email,query)

    # Initialize the HR agent
    hr_agent = Agent(
        name="Data presenter Agent",
        # model=Ollama(id="llama2-13b"),  # LLM for processing and structuring text
        # model=Groq(id='llama3-8b-8192'),
        model=Groq(id='gemma2-9b-it'),
        description="You are a data presenter chat  Agent who can prsent data like a chatbot with user query and database data.",
        instructions=[
            "You are a data presenter Agent who can present the information to user based on database data and user query.",
            "Organize the information from the data you are given and generate response according to user query.",
            "Do not add anything from your own,out of the given data.",
            "Respond very smartly and to the point answer, but seems like you are chating with the user.",
            "If the query is any contact information like Name, or Phone number, just give the name or number, noting else."
        ],
        markdown=True,
    )

    # Process the (translated) CV text
    result = hr_agent.run(f"User Query: {query}, Fetched Data: {data}")
    raw_info= result.content
    cleaned_text = raw_info.replace("\n", " ")
    return cleaned_text
    # # parsed_json =detect_and_parse_json2(raw_info)
    # cleaned_text = raw_info.replace("\n", " ")
    # parsed_json=extract_json_from_string(cleaned_text)
    # if parsed_json:
    #     return parsed_json
    # else:
    #     return raw_info