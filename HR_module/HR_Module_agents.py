from phi.agent import Agent
from phi.model.ollama import Ollama
from phi.model.groq import Groq
from transformers import pipeline
from dotenv import load_dotenv
from langdetect import detect, detect_langs
import re
import json

# Load environment variables
load_dotenv()

# Initialize the translation pipeline
# translation_pipeline = pipeline(
#     "translation", model="facebook/m2m100_418M", tokenizer="facebook/m2m100_418M"
# )
# translation_pipeline = pipeline("translation", model="facebook/m2m100_418M")
# translation_pipeline = pipeline("translation", model="facebook/m2m100_418M")
translation_pipeline = pipeline("translation", model="facebook/mbart-large-50-many-to-many-mmt")

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
        model=Groq(id='llama3-8b-8192'),
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
    pattern = r"```(.*?)```"
    match = re.search(pattern, raw_info, re.DOTALL)
    
    if match:
        try:
            json_data= match.group(1).strip()
            result=json.loads(json_data)
            return result
        except Exception as e:
            print("Error in JSON: "+str(e))
            return raw_info
    else:
        return raw_info



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
        model=Groq(id='llama3-8b-8192'),  # Replace with your desired LLM model
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
            "Provide the following output format start and end with (''') Strictly in JSON format:",
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
    pattern = r"```(.*?)```"
    match = re.search(pattern, raw_info, re.DOTALL)
    
    if match:
        try:
            json_data= match.group(1).strip()
            result=json.loads(json_data)
            return result
        except Exception as e:
            print("Error in JSON: "+str(e))
            return raw_info
    else:
        return raw_info