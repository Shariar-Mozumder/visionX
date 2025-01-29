from sqlalchemy import create_engine, text
from phi.agent import Agent
from phi.model.groq import Groq
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
groq_api_key = os.environ.get("GROQ_API_KEY")

# Initialize SQLAlchemy
DATABASE_URL = 'mssql+pyodbc://DESKTOP-2419RQF/visionX?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes'
engine = create_engine(DATABASE_URL)

# Initialize Groq
# groq_instance = Groq(api_key=groq_api_key)

# Create a PhiData Agent
sql_agent = Agent(
    name="SQL Query Generator",
    role="Generates SQL queries based on user requests.",
    instructions=[
        "You are an assistant that generates SQL queries based on user input.",
        "Ensure the SQL queries are correct, optimized, and syntactically valid.",
        "No additional text or explaination please, just the raw query.",
        "if the user is not new one of the email address always will be given, use that as a key to find out the candidate and perform query. Remember, ContactInformation is a Text feild, use LIKE for email search."
        "These are the table schema you can get the tables and attributes: "
        '''
        CREATE TABLE [dbo].[Candidates](
            [CandidateID] [bigint] IDENTITY(1,1) NOT NULL,
            [ContactInformation] [text] NULL,
            [AcademicEducation] [text] NULL,
            [WorkExperience] [text] NULL,
            [Skills] [text] NULL,
            [CompatibilityScore] [int] NULL,
            [SimilarityScore] [float] NULL,
            [Stage] [text] NULL,
            [Shortlisted] [text] NULL,
            [ScreeningDate] [datetime] NULL,
            [ScreeningResult] [text] NULL,
            [TechnicalTestDate] [datetime] NULL,
            [TechnicalTestResult] [text] NULL,
            [HrTestDate] [datetime] NULL,
            [HrTestResult] [text] NULL,
            [JoiningDate] [datetime] NULL,
            [Joined] [text] NULL,
            [Blacklisted] [text] NULL,
            [JobDescription] [text] NULL,
        CONSTRAINT [PK_Candidates] PRIMARY KEY CLUSTERED 
        (
            [CandidateID] ASC
        )WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
        ) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
        GO
        '''
    ],
    model=Groq(id="gemma2-9b-it")  # Replace with your Groq model
)

# Function to generate SQL queries using the agent
def generate_sql_query_with_agent(prompt):
    try:
        response = sql_agent.run(prompt)
        return response.content.strip()  # Extract the generated SQL query
    except Exception as e:
        print(f"Error generating SQL query: {e}")
        return None

# Function to execute SQL queries
def execute_query(query, commit=False):
    try:
        # with engine.connect() as connection:
        #     result = connection.execute(text(query))
        #     return result.fetchall()
        with engine.connect() as connection:
            result = connection.execute(text(query))
            if commit:
                connection.commit()
            return result.fetchall() if not commit else "Query executed successfully."
    except Exception as e:
        print(f"Error executing SQL query: {e}")
        return None

import re
# Main function for querying the database
def query_database(prompt):
    try:
        # query_data=''
        # Generate SQL query using the agent
        sql_query = generate_sql_query_with_agent(prompt)
        pattern = r"```(.*?)```"
        match = re.search(pattern, sql_query, re.DOTALL)
        if match:
            sql_query= match.group(1).strip()
        
        # sql_query = sql_query.replace("\n", " ")
        try:
            start = sql_query.index('\n') + 1  # Find the first newline and move one step forward
            end = sql_query.rindex('\n')      # Find the last newline
            sql_query= text[start:end].strip()
        except Exception as e:
            sql_query = sql_query.replace("\n", " ")
            sql_query = sql_query.replace("sql", " ")
            # sql_query=sql_query

        semicolon_index = sql_query.find(';')
        if semicolon_index != -1:
            sql_query = sql_query[:semicolon_index + 1]  # Include the semicolon
            sql_query.strip()
    
        if not sql_query:
            return "Failed to generate SQL query."
        
        print(f"Generated SQL Query: {sql_query}")
        commit_needed = False

        if sql_query.strip().upper().startswith(("SELECT", "SHOW", "DESCRIBE")):
            commit_needed = False  # SELECT and similar queries do not modify the database
        elif sql_query.strip().upper().startswith(("INSERT", "UPDATE", "DELETE")):
            commit_needed = True  # INSERT, UPDATE, DELETE queries modify the database
        # Execute the generated SQL query
        results = execute_query(sql_query,commit_needed)
        return results
    except Exception as e:
        return f"Error: {e}"


def get_candidate_info(email, query):
    final_prompt=f"My email address is: {email}, my query is: {query}"
    query_results = query_database(final_prompt)
    
    
    print("Query Results:")
    if query_results:
        return query_results
    else:
        return ("Not available in database.")
        # for row in query_results:
        #     print(row)
# Example Usage
# if __name__ == "__main__":
#     email_address="shmozumder2@gmail.com"
#     user_prompt = "What about my skill noted?"
#     final_prompt=f"My email address is: {email_address}, my query is: {user_prompt}"
#     query_results = query_database(final_prompt)
    
#     print("Query Results:")
#     if query_results:
#         for row in query_results:
#             print(row)
