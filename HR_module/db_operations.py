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
        "SimilarityScore": data.get("SimilarityScore"),  # Fixed typo
        "Stage": data.get("Stage"),
        "Shortlisted": data.get("Shortlisted"),
        "ScreeningDate": data.get("ScreeningDate"),
        "ScreeningResult": data.get("ScreeningResult"),
        "TechnicalTestDate": data.get("TechnicalTestDate"),
        "TechnicalTestResult": data.get("TechnicalTestResult"),
        "HrTestDate": data.get("HrTestDate"),
        "HrTestResult": data.get("HrTestResult"),
        "JoiningDate": data.get("JoiningDate"),
        "Joined": data.get("Joined"),
        "Blacklisted": data.get("Blacklisted"),
        "JobDescription": data.get("JobDescription"),
    }
    try:
        # Connect to the database
        with engine.connect() as connection:
            # Dynamically build the insert query
            query = insert(Table('Candidates', MetaData(), autoload_with=engine)).values(candidate_data)
            connection.execute(query)
            connection.commit()
            print("Data inserted successfully.")
            return 200
    except Exception as e:
        print(f"Error inserting data: {e}")
        return 500

# Insert the candidate data
# insert_candidate(candidate_data)


from sqlalchemy import update, select

def update_candidate(data,email):
    # email = data.get("ContactInformation")  # Extract email for filtering
    if not email:
        print("Error: Email is required to update a candidate.")
        return 400  # Bad request

    # Define updatable fields
    update_data = {
        "ContactInformation": data.get("ContactInformation"),
        "AcademicEducation": data.get("AcademicEducation"),
        "WorkExperience": data.get("WorkExperience"),
        "Skills": data.get("Skills"),
        "CompatibilityScore": data.get("CompatibilityScore"),
        "SimilarityScore": data.get("SimilarityScore"),  # Fixed typo
        "Stage": data.get("Stage"),
        "Shortlisted": data.get("Shortlisted"),
        "ScreeningDate": data.get("ScreeningDate"),
        "ScreeningResult": data.get("ScreeningResult"),
        "TechnicalTestDate": data.get("TechnicalTestDate"),
        "TechnicalTestResult": data.get("TechnicalTestResult"),
        "HrTestDate": data.get("HrTestDate"),
        "HrTestResult": data.get("HrTestResult"),
        "JoiningDate": data.get("JoiningDate"),
        "Joined": data.get("Joined"),
        "Blacklisted": data.get("Blacklisted"),
        "JobDescription": data.get("JobDescription"),
    }

    # Remove any None values to prevent overwriting existing values with NULL
    update_data = {key: value for key, value in update_data.items() if value is not None}

    if not update_data:
        print("Error: No data provided to update.")
        return 400  # No updates provided

    try:
        with engine.connect() as connection:
            # Check if a candidate with the given email exists
            candidates_table = Table('Candidates', MetaData(), autoload_with=engine)
            query_check = select(candidates_table).where(candidates_table.c.ContactInformation.like(f"%{email}%"))
            result = connection.execute(query_check).fetchone()

            if not result:
                print("Error: No matching candidate found.")
                return 404  # Not found

            # Build and execute the update query
            query = update(candidates_table).where(candidates_table.c.ContactInformation.like(f"%{email}%")).values(update_data)
            connection.execute(query)
            connection.commit()
            print("Data updated successfully.")
            return 200  # Success
    except Exception as e:
        print(f"Error updating data: {e}")
        return 500  # Internal server error

