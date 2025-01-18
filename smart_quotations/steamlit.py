import streamlit as st
import requests

# FastAPI endpoint
API_URL = "http://localhost:8000/generate-quotation/"

# Streamlit app
st.title("Smart Quotation Generator")
st.markdown("Enter a product name to generate a quotation.")

# Input form
with st.form("quotation_form"):
    product_name = st.text_input("Product Name", placeholder="Enter the product name here")
    submitted = st.form_submit_button("Generate Quotation")
    Generate_pdf = st.form_submit_button("Generate Pdf")

if submitted:
    if not product_name:
        st.error("Please provide a product name.")
    else:
        # API request payload
        payload = {"product_name": product_name}
        
        # Send request to FastAPI
        try:
            response = requests.post(API_URL, json=payload)
            
            if response.status_code == 200:
                st.success("Quotation generated successfully!")
                st.json(response.json())  # Display formatted JSON response
            else:
                st.error(f"Failed to generate quotation. Error: {response.status_code}")
                st.text(response.text)
        except requests.exceptions.RequestException as e:
            st.error(f"An error occurred while connecting to the API: {e}")
