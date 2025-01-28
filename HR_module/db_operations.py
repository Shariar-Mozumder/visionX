from sqlalchemy import create_engine, MetaData, Table, text
from sqlalchemy.sql import insert

# Initialize SQLAlchemy engine (replace with your actual database URL)
DATABASE_URL = 'mssql+pyodbc://DESKTOP-2419RQF/visionX?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes'
engine = create_engine(DATABASE_URL)



# Data to be inserted dynamically


def insert_candidate(data):

    candidate_data = {
        "ContactInformation": data.get("ContactInformation"),
        "AcademicEducation": data.get("AcademicEducation"),
        "WorkExperience": data.get("WorkExperience"),
        "Skills": data.get("Skills"),
        "CompatibilityScore": data.get("CompatibilityScore"),
        "SimilaritSscore": data.get("SimilaritSscore"),
        "Stage": data.get("Stage"),
        "Shortlisted": data.get("Shortlisted"),
        "Joined": data.get("Joined"),
        "Blacklisted": data.get("Blacklisted")
    }
    try:
        # Connect to the database
        with engine.connect() as connection:
            # Dynamically build the insert query
            query = insert(Table('Candidates', MetaData(), autoload_with=engine)).values(data)
            connection.execute(query)
            connection.commit()
            print("Data inserted successfully.")
    except Exception as e:
        print(f"Error inserting data: {e}")

# Insert the candidate data
# insert_candidate(candidate_data)
