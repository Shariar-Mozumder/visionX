import PyPDF2
import spacy
from sentence_transformers import SentenceTransformer, util
import re
from datetime import datetime
import os
import zipfile
from bs4 import BeautifulSoup
from docx import Document

import sys
import os

# sys.path.append(os.path.abspath("agents"))

from HR_Module_agents import  process_resume,score_resume

# def extract_text_from_pdf(pdf_path):
#     with open(pdf_path, 'rb') as file:
#         reader = PyPDF2.PdfReader(file)
#         text = " ".join([page.extract_text() for page in reader.pages])
#     return text


import pdfplumber

def extract_text_from_file(file_path):
    file_extension = os.path.splitext(file_path)[1].lower()
    extracted_text = ""

    try:
        if file_extension == '.pdf':
            # Extract text from PDF
            # with open(file_path, 'rb') as file:
            #     reader = PyPDF2.PdfReader(file)
            #     extracted_text = " ".join([page.extract_text() for page in reader.pages])

            with pdfplumber.open(file_path) as pdf:
                extracted_text = ""
                for page in pdf.pages:
                    # Extract text with layout information
                    extracted_text += page.extract_text()

        elif file_extension in ['.docx', '.doc']:
            # Extract text from Word document
            doc = Document(file_path)
            # extracted_text = " ".join([paragraph.text for paragraph in doc.paragraphs])
            paragraphs = [paragraph.text for paragraph in doc.paragraphs if paragraph.text.strip()]
            tables = []
            for table in doc.tables:
                for row in table.rows:
                    for cell in row.cells:
                        tables.append(cell.text.strip())
            # Combine all extracted text
            extracted_text = " ".join(paragraphs + tables)

        elif file_extension == '.txt':
            # Extract text from plain text file
            with open(file_path, 'r', encoding='utf-8') as file:
                extracted_text = file.read()

        elif file_extension == '.html':
            # Extract text from HTML file
            with open(file_path, 'r', encoding='utf-8') as file:
                soup = BeautifulSoup(file, 'html.parser')
                extracted_text = soup.get_text()

        elif file_extension == '.zip':
            # Extract text from ZIP file
            with zipfile.ZipFile(file_path, 'r') as zip_file:
                for name in zip_file.namelist():
                    if name.endswith(('.pdf', '.docx', '.doc', '.txt', '.html')):
                        with zip_file.open(name) as file:
                            nested_extension = os.path.splitext(name)[1].lower()
                            nested_text = ""
                            if nested_extension == '.pdf':
                                reader = PyPDF2.PdfReader(file)
                                nested_text = " ".join([page.extract_text() for page in reader.pages])
                            elif nested_extension in ['.docx', '.doc']:
                                doc = Document(file)
                                nested_text = " ".join([paragraph.text for paragraph in doc.paragraphs])
                            elif nested_extension == '.txt':
                                nested_text = file.read().decode('utf-8')
                            elif nested_extension == '.html':
                                soup = BeautifulSoup(file, 'html.parser')
                                nested_text = soup.get_text()
                            extracted_text += nested_text + "\n"

        else:
            raise ValueError(f"Unsupported file type: {file_extension}")

    except Exception as e:
        return f"Error while processing {file_path}: {e}"

    return extracted_text




nlp = spacy.load("en_core_web_sm")

def preprocess_text(text):
    doc = nlp(text.lower())
    return " ".join([token.lemma_ for token in doc if not token.is_stop and token.is_alpha])



model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

def compute_similarity(job_description, resume_text):
    job_embedding = model.encode(job_description, convert_to_tensor=True)
    resume_embedding = model.encode(resume_text, convert_to_tensor=True)
    return util.pytorch_cos_sim(job_embedding, resume_embedding).item()



def extract_skills(text):
    skills_list = ["python", "machine learning", "data analysis", "communication"]  # Add more skills
    return [skill for skill in skills_list if skill in text.lower()]

# def extract_entities(resume_text):
#     doc = nlp(resume_text)
#     entities = {"Skills": [], "Education": [], "Experience": []}
#     for ent in doc.ents:
#         if ent.label_ in ["ORG", "EDUCATION"]:
#             entities["Education"].append(ent.text)
#         elif ent.label_ in ["DATE"]:
#             entities["Experience"].append(ent.text)
#         elif ent.label_ in ["PRODUCT", "WORK_OF_ART"]:
#             entities["Skills"].append(ent.text)
#     return entities
def extract_entities(resume_text):
    doc = nlp(resume_text)
    entities = {
        "Work Experience": [],
        "Projects": [],
        "Research": [],
        "Academic Achievements": [],
        "Education": [],
        "Skills": [],
        "Social Work/Volunteer": [],
    }

    for ent in doc.ents:
        # Classify entities based on their labels
        if ent.label_ in ["ORG", "EDUCATION"]:
            entities["Education"].append(ent.text)
        elif ent.label_ == "DATE":
            entities["Work Experience"].append(ent.text)
        elif ent.label_ in ["PRODUCT", "WORK_OF_ART"]:
            entities["Skills"].append(ent.text)
        elif ent.label_ in ["GPE", "LOC"] and "project" in ent.text.lower():
            entities["Projects"].append(ent.text)
        elif ent.label_ in ["PERSON", "ORG"] and "research" in ent.text.lower():
            entities["Research"].append(ent.text)
        elif ent.label_ == "MONEY" or "achievement" in ent.text.lower():
            entities["Academic Achievements"].append(ent.text)
        elif ent.label_ == "NORP" or "volunteer" in ent.text.lower():
            entities["Social Work/Volunteer"].append(ent.text)

    # Heuristic-based enhancements
    for line in resume_text.splitlines():
        line_lower = line.lower()
        if "intern" in line_lower or "work experience" in line_lower:
            entities["Work Experience"].append(line.strip())
        if "project" in line_lower:
            entities["Projects"].append(line.strip())
        if "research" in line_lower:
            entities["Research"].append(line.strip())
        if "achievement" in line_lower or "award" in line_lower:
            entities["Academic Achievements"].append(line.strip())
        if "volunteer" in line_lower or "social work" in line_lower:
            entities["Social Work/Volunteer"].append(line.strip())
        if "skill" in line_lower or "proficient in" in line_lower:
            entities["Skills"].append(line.strip())

    # Deduplicate and clean up extracted entities
    for category in entities:
        entities[category] = list(set(entities[category]))

    return entities


def weighted_keyword_match(resume_text, keywords):
    score = 0
    for keyword, weight in keywords.items():
        if keyword.lower() in resume_text.lower():
            score += weight
    return score

def calculate_experience(resume_text):
    dates = re.findall(r"\b(19|20)\d{2}\b", resume_text)
    if len(dates) >= 2:
        years = [int(date) for date in dates]
        experience = max(years) - min(years)
        return experience
    return 0


def extract_resumes(resumes):
    results = []
    for resume_path in resumes:
        resume_text = extract_text_from_file(resume_path)
        # preprocessed_text = preprocess_text(resume_text)
        # similarity_score = compute_similarity(job_description, preprocessed_text)
        # entities=extract_entities(resume_text)
        # exp=calculate_experience(resume_text)
        ai_rsponse=process_resume(resume_text)
        print(ai_rsponse)
        results.append(ai_rsponse)
        # results.append((resume_path, similarity_score))
    return results

def resumes_scores_count(job_description, resume_list):
    scores=[]
    for resume in resume_list:
        score_result=score_resume(resume,job_description)
        Contact_Details=resume.get('Contact Details')
        resume_sores={
            "Contact_Details":Contact_Details,
            "score_result": score_result
        }
        scores.append(resume_sores)
    return scores

def rank_resume(job_description,resume_paths):
    # needs to elaborate more
    resume_list=extract_resumes(resume_paths)
    score_result=resumes_scores_count(job_description,resume_list)
    return resume_list,score_result



def calculate_total_score(similarity, keyword_score, experience, soft_skills_score):
    return (
        0.4 * similarity +
        0.3 * keyword_score +
        0.2 * experience +
        0.1 * soft_skills_score
    )

# Example inputs
similarity = 0.85  # Similarity score from Sentence Transformers
keyword_score = 25
experience = 5  # Years
soft_skills_score = 0.9  # Sentiment analysis score

total_score = calculate_total_score(similarity, keyword_score, experience, soft_skills_score)

if __name__=="__main__":
    resumes=[
            'C:/Users/Lenovo/Downloads/Md_Shariar_Hossain_ML_CV.pdf',
             'C:/Users/Lenovo/Downloads/Samin-Yasar-Chowdhury_CV.pdf',
             'C:/Users/Lenovo/Downloads/Farjana_cv.pdf',
             'C:/Users/Lenovo/Downloads/doc_cv.docx',
             'C:/Users/Lenovo/Downloads/cv.txt']
    job_description='''Empowering Energy - AI Engineer Hiring Process
            Job Title: AI Engineer
            Location: Riyadh, Saudi Arabia (Initial remote work from Bangladesh)
            Vacancies: 3
            Salary: 80k to 120k BDT per month (with a higher salary upon relocation)
            Company Overview:
            Empowering Energy, based in Riyadh, Saudi Arabia, is a leader in smart building solutions. We specialize in integrating LED lighting, automation, control, and low-current systems. Our services enhance energy efficiency and reduce costs for homes and businesses. We offer advanced technology solutions, including Smart Homes, Smart Buildings, security systems, multi-room audio-video, and comprehensive SaaS services. Our Empowering Solution AI Portal leverages cutting-edge technology to deliver sustainable and efficient solutions.
            Job Description:
            We are seeking highly skilled AI Engineers with over 5 years of experience in AI and machine learning technologies. The ideal candidates will excel in managing existing AI projects and driving the development of innovative new AI features. Candidates should demonstrate a strong proficiency in AI frameworks, possess exceptional problem-solving abilities, and have a proven track record of delivering high-quality AI models. They should also be adept at collaborating with cross-functional teams to ensure seamless integration and performance optimization.
            Key Responsibilities:
            💻 Develop and maintain AI models and algorithms
            🔗 Integrate AI solutions with existing systems and APIs
            ⚙️ Optimize AI models for performance and scalability
            🤖 Automate AI workflows and streamline processes
            📈 Implement AI-driven automation to enhance operational efficiency
            🛠️ Maintain and improve existing AI codebase
            📝 Write clean, maintainable AI code
            👥 Participate in code reviews and uphold AI coding standards
            📚 Share AI knowledge and best practices
            🌟 Implement new AI features and enhancements
            🔍 Conduct debugging and troubleshooting of AI models
            🚀 Conduct performance testing and optimization of AI solutions
            🔒 Implement security and data protection measures for AI models
            🗓️ Participate in sprint planning and agile ceremonies
            📊 Monitor and improve AI performance metrics
            🧩 Develop reusable AI components and libraries
            📄 Document technical specifications and AI processes
            Requirements:
            📅 5+ years in AI and machine learning development
            💻 Strong understanding of Python, TensorFlow, PyTorch, and other AI frameworks
            🔄 Proficient in developing and deploying AI models
            🔧 Experience with data preprocessing and feature engineering
            🔗 Understanding of RESTful APIs and web services integration
            🛠️ Experience with microservices architecture and AI deployment
            🔧 Familiarity with modern build pipelines and tools (e.g., Docker, Kubernetes)
            📂 Proficient in version control systems (e.g., Git)
            🧪 Familiarity with testing frameworks for AI models
            🚀 Knowledge of performance optimization techniques for AI models
            🔒 Understanding of security best practices in AI development
            ⏰ Ability to work independently and manage time effectively
            🧠 Strong analytical and critical thinking abilities
            📚 Willingness to learn and stay updated with industry trends
            🌐 Experience with cloud services (e.g., Azure, AWS) for AI deployment
            🔹 Additional Required Skills:
            Machine Learning: Supervised/unsupervised learning, KNN, decision/regression trees, support vector machines
            Deep Learning and Neural Networks: CNNs, RNNs, GANs, Transformers
            AI Techniques and Tools: LangChain, RAG, Gradio, Vector Databases, Hugging Face libraries
            Generative AI and LLMs: LLM architectures, NLP, PyTorch torchtext, tokenization, sequence-to-sequence models
            Advanced Topics in AI: Fine-tuning LLMs, reinforcement learning, prompt engineering
            Benefits:
            💰 Competitive salary with significant growth potential
            ✈️ Comprehensive relocation package: visa, flight tickets, iqama, housing
            🌟 Dynamic and innovative team environment
            📈 Career advancement and professional development opportunities
            🧠 Access to premium AI tools: ChatGPT, Gemini, Claude AI
            🏥 Comprehensive medical insurance
            🏖️ Generous paid time off and holiday leave
            🤝 Inclusive and collaborative work culture
            🎉 Regular team-building activities and company events
            🔧 State-of-the-art technology stack
            💼 Performance-based bonuses and incentives
            🎁 Attractive employee referral program
            📊 Transparent and supportive management
            🌍 Opportunity to work on impactful global projects
            🏫 Company-sponsored training and workshops
            🗣️ Access to industry conferences and networking events
            Hiring Process:
            1. Application Submission:
            Submit your resume/CV with portfolio.
            2. Initial Screening:
            HR reviews applications and shortlists based on experience and skills.
            3. Technical Assessment:
            Shortlisted candidates complete a technical assessment.
            4. Technical Interview:
            Candidates who pass the assessment have a technical interview.
            5. Cultural Fit Interview:
            HR assesses cultural fit and communication skills.
            6. Offer and Initial Agreement:
            Successful candidates get a job offer for 3 months of remote work.
            7. Remote Work Period:
            Work remotely from Bangladesh with regular evaluations.
            8. Relocation to Saudi Arabia:
            After 3 months, relocate to Saudi Arabia with provided visa, ticket, iqama, housing.
            9. New Agreement and Salary Adjustment:
            Sign a new agreement with a higher salary upon relocation.
            10. Onboarding in Saudi Arabia:
            Onboard in Riyadh office with ongoing support and development opportunities.
            Frequently Asked Questions (FAQs):
            1. What is the application process?
            Submit your resume/CV to hamed@empoweringeng.com, including portfolio.
            2. What happens after I apply?
            HR reviews applications and shortlisted candidates undergo a technical assessment.
            3. What does the technical assessment involve?
            Evaluates coding skills and problem-solving abilities.
            4. What is the interview process?
            Includes a technical interview and a cultural fit interview with HR.
            5. What are the initial working conditions?
            Work remotely from Bangladesh for 3 months with regular evaluations.
            6. What happens after the remote period?
            Relocate to Saudi Arabia with visa, ticket, iqama, and housing provided.
            7. Will my salary change after relocation?
            Yes, a new agreement with a higher salary will be signed upon relocation.
            8. What support is provided in Saudi Arabia?
            Continuous support, professional development opportunities, and onboarding in Riyadh.
            9. What are the benefits offered?
            Competitive salary, relocation package, professional development, access to premium AI tools, health benefits, and more.
            10. What if I receive a better offer from another company after relocation?
            During the first 2 years, you are committed to staying with Empowering Energy. After this period, you may transfer if desired.
            11. What is the application deadline?
            The application deadline is Monday, 23rd December 2024.
            We look forward to receiving your applications and welcoming you to our team at Empowering Energy. For any inquiries, please contact hamed@empoweringeng.com.
            Don't miss this opportunity to bring your AI visions to life with us!
            For more about our company: 🌐 Empowering Energy - https://www.empoweringeng.com🌐 ESAP (IT Division) - https://www.esapai.com
            Let’s build the future together! '''
    job_des_path='Job_description.txt'
    extracted_text=''
    with open(job_des_path, 'r', encoding='utf-8') as file:
                extracted_text = file.read()
    result=rank_resume(extracted_text,resumes)
    print(result)


