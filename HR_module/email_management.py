# import requests
# from email_service import send_email  # Custom email-sending function

# class RecruitmentAgent:
#     def __init__(self):
#         self.templates = self.load_templates()

#     def load_templates(self):
#         return {
#             "shortlist": "Dear {name}, You have been shortlisted for {job_title}.",
#             "screening_result_pass": "Dear {name}, Congratulations! You have passed the screening test.",
#             "screening_result_fail": "Dear {name}, Unfortunately, you did not pass the screening test.",
#             "technical_invitation": "Dear {name}, Please take the technical test at {test_link}.",
#             "technical_result_pass": "Dear {name}, Congratulations! You have passed the technical test.",
#             "technical_result_fail": "Dear {name}, Unfortunately, you did not pass the technical test.",
#             "hr_invitation": "Dear {name}, Your HR interview is scheduled for {interview_date}.",
#             "offer_letter": "Dear {name}, We are pleased to offer you the position of {job_title}. Your offer letter is attached.",
#         }

#     def process_request(self, stage, data):
#         for candidate in data:
#             email = candidate["email"]
#             name = candidate.get("name")
#             if stage == "shortlist":
#                 subject = "You Have Been Shortlisted!"
#                 body = self.templates["shortlist"].format(name=name, job_title=candidate["job_title"])
#                 send_email(email, subject, body)
#             elif stage == "screening_results":
#                 if candidate["result"] == "passed":
#                     subject = "Screening Test Results"
#                     body = self.templates["screening_result_pass"].format(name=name)
#                     send_email(email, subject, body)
#                     # Send technical test invitation
#                     subject = "Technical Test Invitation"
#                     body = self.templates["technical_invitation"].format(name=name, test_link=candidate["test_link"])
#                     send_email(email, subject, body)
#                 else:
#                     subject = "Screening Test Results"
#                     body = self.templates["screening_result_fail"].format(name=name)
#                     send_email(email, subject, body)
#             elif stage == "technical_results":
#                 if candidate["result"] == "passed":
#                     subject = "Technical Test Results"
#                     body = self.templates["technical_result_pass"].format(name=name)
#                     send_email(email, subject, body)
#                     # Invite for HR interview
#                     subject = "HR Interview Invitation"
#                     body = self.templates["hr_invitation"].format(name=name, interview_date=candidate["interview_date"])
#                     send_email(email, subject, body)
#                 else:
#                     subject = "Technical Test Results"
#                     body = self.templates["technical_result_fail"].format(name=name)
#                     send_email(email, subject, body)
#             elif stage == "hr_results":
#                 if candidate["result"] == "passed":
#                     subject = "Offer Letter"
#                     body = self.templates["offer_letter"].format(name=name, job_title=candidate["job_title"])
#                     send_email(email, subject, body, attachment=candidate["offer_letter"])



# from fastapi import FastAPI, HTTPException, Request
# from pydantic import BaseModel
# from typing import List
# from phi.agent import Agent
# from phi.model.openai import OpenAIChat
# from phi.embedder.openai import OpenAIEmbedder
# from phi.knowledge.text import TextKnowledgeBase
# from phi.vectordb.lancedb import LanceDb, SearchType
# import smtplib
# from email.mime.text import MIMEText
# from email.mime.multipart import MIMEMultipart

# app = FastAPI()

# # Create a knowledge base
# knowledge_base = TextKnowledgeBase(
#     documents=[
#         {
#             "id": "job_description",
#             "text": "Software Engineer opening at Acme Corp. Requires experience in Python, FastAPI, and AI systems."
#         },
#         {
#             "id": "resume_1",
#             "text": "John Doe: Experienced Python Developer with FastAPI expertise and 5 years of AI project experience."
#         },
#         # Add more resumes or job descriptions as needed
#     ],
#     vector_db=LanceDb(
#         table_name="hr_management",
#         uri="tmp/lancedb",
#         search_type=SearchType.vector,
#         embedder=OpenAIEmbedder(model="text-embedding-3-small"),
#     ),
# )
# knowledge_base.load(recreate=False)

# # Create an agent with the knowledge base
# agent = Agent(
#     model=OpenAIChat(id="gpt-4o"),
#     knowledge=knowledge_base,
#     show_tool_calls=True,
#     markdown=True,
# )

# # Data model for email requests
# class Candidate(BaseModel):
#     name: str
#     email: str
#     additional_info: str = None

# class ShortlistRequest(BaseModel):
#     job_id: str
#     job_title: str
#     shortlist_date: str
#     candidates: List[Candidate]

# class ResultRequest(BaseModel):
#     stage: str  # e.g., "Technical Test", "HR Interview"
#     candidates: List[Candidate]

# # SMTP email sender setup
# SMTP_HOST = "smtp.example.com"
# SMTP_PORT = 587
# SMTP_USER = "your-email@example.com"
# SMTP_PASSWORD = "your-email-password"

# def send_email(subject: str, body: str, recipient: str):
#     """Send an email to a recipient."""
#     msg = MIMEMultipart()
#     msg['From'] = SMTP_USER
#     msg['To'] = recipient
#     msg['Subject'] = subject

#     msg.attach(MIMEText(body, 'html'))
    
#     with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
#         server.starttls()
#         server.login(SMTP_USER, SMTP_PASSWORD)
#         server.sendmail(SMTP_USER, recipient, msg.as_string())

# # Helper function to generate email content
# def generate_email_content(candidate: Candidate, job_title: str, stage: str):
#     prompt = (
#         f"Generate an email for the {stage} stage of recruitment for the role {job_title}. "
#         f"Include the candidate's name {candidate.name} and the following additional info: {candidate.additional_info}."
#     )
#     response = agent.get_response(prompt)
#     subject = f"{stage} - {job_title}"
#     body = response.result
#     return subject, body

# # POST endpoint for shortlisting
# @app.post("/api/shortlist")
# async def shortlist_candidates(request: ShortlistRequest):
#     try:
#         for candidate in request.candidates:
#             subject, body = generate_email_content(
#                 candidate, request.job_title, "Initial Shortlist Result"
#             )
#             send_email(subject, body, candidate.email)
#         return {"status": "success", "message": "Emails sent successfully."}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

# # POST endpoint for sending results
# @app.post("/api/send-results")
# async def send_results(request: ResultRequest):
#     try:
#         for candidate in request.candidates:
#             stage = request.stage
#             subject, body = generate_email_content(candidate, "Job Application", stage)
#             send_email(subject, body, candidate.email)
#         return {"status": "success", "message": f"Emails sent for {request.stage} stage."}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))


import chromadb
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from phi.agent import Agent
from phi.model.groq import Groq
from phi.embedder.huggingface import HuggingfaceCustomEmbedder
from phi.knowledge.pdf import PDFUrlKnowledgeBase
from phi.vectordb.lancedb import LanceDb, SearchType
# from phi.knowledge.base import KnowledgeBase
import smtplib
import uvicorn
from chromadb import Client
from chromadb.config import Settings
from chromadb.utils import embedding_functions
from dotenv import load_dotenv
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from HR_Module_agents import candidate_data
load_dotenv()

app = FastAPI()


# Helper function for sending email
def send_email(to_email: str, subject: str, body: str, attachment: Optional[str] = None):
    try:
        # Create message
        from_email="shmozumder2@gmail.com"
        from_password="ilhnoxrbjlcnzldx"

        message = MIMEMultipart()
        message["From"] = "shmozumder2@gmail.com"
        message["To"] = to_email
        message["Subject"] = subject
        message.attach(MIMEText(body, "plain"))

        # Send the email
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:  # Replace with your SMTP server details
            server.login(from_email, from_password)
            server.sendmail(from_email, to_email, message.as_string())

        return (200,"Email sent")
        # Dummy SMTP server config (update with real credentials)
        # server = smtplib.SMTP("smtp.gmail.com", 465)
        # server.starttls()
        # server.login("shmozumder2@gmail.com", "ilhnoxrbjlcnzldx")
        # message = f"Subject: {subject}\n\n{body}"
        # server.sendmail("your_email@example.com", to_email, message)
        # server.quit()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Email sending failed: {e}")

# Request Models
class ShortlistRequest(BaseModel):
    email_ids: List[str]

class TestInvitationRequest(BaseModel):
    email_ids: List[str]
    meeting_link: str

class TestResultRequest(BaseModel):
    email_ids: List[str]
    results: List[bool]

class FinalResultRequest(BaseModel):
    email_ids: List[str]
    results: List[bool]
    offer_letter_path: Optional[str]


candidate_data={
            "name":"Md Shariar Hossain"
        }
# Endpoints
@app.post("/shortlist")
def send_shortlist_emails(request: ShortlistRequest):
    for email in request.email_ids:
        # candidate_data = agent.generate(f"Fetch data for {email}")
        
        subject = f"Shortlist Confirmation for {candidate_data['name']}"
        body = f"Dear {candidate_data['name']},\n\nCongratulations! You have been shortlisted. Please find more details below.\n\nBest regards,\nHR Team"
        send_email(email, subject, body)
    return {"message": "Shortlist emails sent successfully"}

@app.post("/online-screening-invitation")
def send_online_screening_invitation(request: TestInvitationRequest):
    for email in request.email_ids:
        # candidate_data = agent.generate(f"Fetch data for {email}")
        subject = f"Online Screening Test Invitation for {candidate_data['name']}"
        body = f"Dear {candidate_data['name']},\n\nYou are invited to an online screening test. Please join using the following link: {request.meeting_link}\n\nBest regards,\nHR Team"
        send_email(email, subject, body)
    return {"message": "Online screening test invitations sent successfully"}

@app.post("/technical-test-invitation")
def send_technical_test_invitations(request: TestResultRequest):
    for email, result in zip(request.email_ids, request.results):
        # candidate_data = agent.generate(f"Fetch data for {email}")
        if result:
            subject = f"Technical Test Invitation for {candidate_data['name']}"
            body = f"Dear {candidate_data['name']},\n\nCongratulations on passing the online screening test! You are invited to a technical test.\n\nBest regards,\nHR Team"
        else:
            subject = f"Online Screening Test Result for {candidate_data['name']}"
            body = f"Dear {candidate_data['name']},\n\nThank you for participating in the online screening test. Unfortunately, you did not pass. We wish you all the best for your future endeavors.\n\nBest regards,\nHR Team"
        send_email(email, subject, body)
    return {"message": "Technical test invitations and results sent successfully"}

@app.post("/hr-interview-invitation")
def send_hr_interview_invitations(request: TestResultRequest):
    for email, result in zip(request.email_ids, request.results):
        # candidate_data = agent.generate(f"Fetch data for {email}")
        if result:
            subject = f"HR Interview Invitation for {candidate_data['name']}"
            body = f"Dear {candidate_data['name']},\n\nCongratulations on passing the technical test! You are invited to an HR interview.\n\nBest regards,\nHR Team"
        else:
            subject = f"Technical Test Result for {candidate_data['name']}"
            body = f"Dear {candidate_data['name']},\n\nThank you for participating in the technical test. Unfortunately, you did not pass. We wish you all the best for your future endeavors.\n\nBest regards,\nHR Team"
        send_email(email, subject, body)
    return {"message": "HR interview invitations and results sent successfully"}

@app.post("/final-result")
def send_final_results(request: FinalResultRequest):
    for email, result in zip(request.email_ids, request.results):
        # candidate_data = agent.generate(f"Fetch data for {email}")
        if result:
            subject = f"Offer Letter for {candidate_data['name']}"
            body = f"Dear {candidate_data['name']},\n\nCongratulations! We are pleased to offer you a position at our company. Please find your offer letter attached.\n\nBest regards,\nHR Team"
            send_email(email, subject, body, attachment=request.offer_letter_path)
        else:
            subject = f"HR Interview Result for {candidate_data['name']}"
            body = f"Dear {candidate_data['name']},\n\nThank you for participating in the HR interview. Unfortunately, you were not selected. We wish you all the best for your future endeavors.\n\nBest regards,\nHR Team"
            send_email(email, subject, body)
    return {"message": "Final results sent successfully"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)