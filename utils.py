####!pip install fpdf

import json
from fpdf import FPDF

def extract_product_details(product_details):
    extracted_products = []
    for detail in product_details:
            try:
                products = json.loads(detail)  # Convert string JSON to dictionary
                extracted_products.extend(products)
            except json.JSONDecodeError:
                print("Error decoding product details. Skipping entry.")
    if len(extracted_products)>0:
        return extracted_products
    else:
        return product_details

# Function to extract relevant sections
def extract_Report_details(report):
    try:
        reports = json.loads(report) 
        return reports
    except Exception as e:
         print(str(e))
         return report
    # for detail in report:
    #         try:
    #             products = json.loads(detail)  # Convert string JSON to dictionary
    #             extracted_products.extend(products)
    #         except json.JSONDecodeError:
    #             print("Error decoding product details. Skipping entry.")
    # if len(extracted_products)>0:
    #     return extracted_products
    # else:
    #     return product_details

    # return extracted_products
    # if product_details_start == -1:
    #     raise ValueError("Couldn't find 'Product_Details' section.")
    
    # Locate "Report" start after "Product_Details"
    # report_start = text.find('"Report": "```json', product_details_start)
    # if report_start == -1:
    #     raise ValueError("Couldn't find 'Report' section after 'Product_Details'.")
    
    # Extract the portion
    # relevant_section = text[product_details_start:report_start]
    # return relevant_section, text[report_start:]

# Function to process and extract report and product details, then convert to PDF
def process_and_generate_pdf(input_text, output_pdf_path):
    try:
        # Step 1: Extract the relevant sections
        product_details, report_section = extract_product_details(input_text)
        
        # Step 2: Extract JSON from the "Report" section
        start_idx = report_section.find('"Report": "```json\n') + len('"Report": "```json\n')
        end_idx = report_section.find('```', start_idx)
        json_report = report_section[start_idx:end_idx]
        
        # Parse the JSON report
        report_data = json.loads(json_report)
        
        # Step 3: Generate PDF
        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()
        
        # Set Title
        pdf.set_font("Arial", size=16, style='B')
        pdf.cell(200, 10, txt="Extracted Report and Product Details", ln=True, align="C")
        
        # Set the Product Details Section
        pdf.ln(10)  # Line break
        pdf.set_font("Arial", size=8)
        pdf.multi_cell(0, 12, f"Product Details:\n{product_details}\n\n")
        
        # Set the Report Section (Formatted JSON)
        pdf.multi_cell(0, 12, f"Report Data:\n{json.dumps(report_data, indent=4)}")
        
        # Step 4: Save to PDF
        pdf.output(output_pdf_path)
        print(f"PDF saved to {output_pdf_path}")
        
    except Exception as e:
        print(f"Error: {e}")

# Example usage
text={
  "Links": [
    "https://duckduckgo.com/l/?uddg=https%3A%2F%2Fwww.amazon.com%2FApple%2DGeneration%2DBluetooth%2DHeadphones%2DMV7N2HN%2Fdp%2FB07Q6153FQ&rut=7fd8dc46ff1cabbee7c978128db39e51afd1b97639115c4cf8fb7e8d9f14aba1",
    "https://duckduckgo.com/l/?uddg=https%3A%2F%2Fwww.target.com%2Fp%2Fapple%2Dairpods%2D2nd%2Dgeneration%2Dwith%2Dcharging%2Dcase%2F%2D%2FA%2D54191097&rut=9dc63c6f60b8d3956291ddd6b9bdc54ed78ae320cc2a6edb1c890b1174b393b8",
    "https://duckduckgo.com/l/?uddg=https%3A%2F%2Fwww.amazon.com%2FApple%2DAirPods%2DCharging%2DLatest%2DModel%2Fdp%2FB07PXGQC1Q&rut=59242f8891ff42378712595bce2bffbe5b601e72001933c8a017c81f726f9b15",
    "https://duckduckgo.com/l/?uddg=https%3A%2F%2Fwww.apple.com%2Fairpods%2F&rut=c73c77d1db55417cbc73aeb763a3577b3fdb34a5a83781fb0783eaf64de05958",
    "https://duckduckgo.com/l/?uddg=https%3A%2F%2Fwww.bestbuy.com%2Fsite%2Fapple%2Dairpods%2Dwith%2Dcharging%2Dcase%2D2nd%2Dgeneration%2Dwhite%2F6084400.p&rut=a3289f41e2c07421aca9d302f738ad411025b9450e1cadb43ac64e542bf043fb",
    "https://duckduckgo.com/l/?uddg=https%3A%2F%2Fsupport.apple.com%2Fen%2Dus%2F111856&rut=a5aa75d810b958b6bee8be276ccdbf1e106feb85e9ec2830ae13d80513173877",
    "https://duckduckgo.com/l/?uddg=https%3A%2F%2Fwww.apple.com%2Fairpods%2Fcompare%2F%3FmodelList%3Dairpods%2D2nd%2Dgen%2Cairpods%2Dpro%2Cairpods%2D4%2Danc&rut=3c24a0f904d8fd39b1a56c1471fc42aa6df3fdaaec4e495c2c39680ce7249f84",
    "https://duckduckgo.com/l/?uddg=https%3A%2F%2Fwww.amazon.com%2FApple%2DCancellation%2DTransparency%2DPersonalized%2DHigh%2DFidelity%2Fdp%2FB0D1XD1ZV3&rut=734612c16b13ca064c1bc289befe15b1b84a3e7bf50f97abe5abcdd81d50b637",
    "https://duckduckgo.com/l/?uddg=https%3A%2F%2Fwww.tomsguide.com%2Faudio%2Fheadphones%2Fairpods%2D4%2Dvs%2Dairpods%2D2%2Dis%2Dit%2Dworth%2Dthe%2Dupgrade&rut=2b07b854e280fcd99bcb9a034375d59519de0552a7af2212ebdbfeb544b87dbf",
    "https://duckduckgo.com/l/?uddg=https%3A%2F%2Fwww.stuff.tv%2Ffeatures%2Fbest%2Dairpods%2F&rut=6193842bdd2c2f8872d3da983faa232c24c13eaf67403228d1e5f9d71e84ad49"
  ],
  "Product_Details": [
    "\n\n[\n    {\n        \"product\": \"Apple AirPods (2nd Generation)\",\n        \"price\": \"$199.00\",\n        \"source\": \"[Amazon](https://www.amazon.com/Apple-Generation-Bluetooth-Headphones-MV7N2HN/dp/B07Q6153FQ)\",\n        \"features\": \"- 4.5 hours of listening time per charge - 24 hour total battery life (based on normal use) - Support for spatial audio and voice activated personal assistant Siri - Compatible with Apple devices such as iPhone, iPad, iPod, Mac, and Apple Watch\"\n    },\n    {\n        \"product\": \"Apple AirPods (3rd Generation)\",\n        \"price\": \"$249.00\",\n        \"source\": \"[Amazon](https://www.amazon.com/Apple-AirPods-Generation-Lightning/dp/B0BDHB9Y8H)\",\n        \"features\": \"- 5 hours of listening time per charge - Up to 30 hour total battery life (based on normal use) - Support for spatial audio and voice activated personal assistant Siri - Waterproof and sweat-resistant - Compatible with Apple devices such as iPhone, iPad, iPod, Mac, and Apple Watch\"\n    },\n    {\n        \"product\": \"Apple AirPods (3rd Generation) EarPods with Lightning Charging Case\",\n        \"price\": \"$259.00\",\n        \"source\": \"[Amazon](https://www.amazon.com/Apple-AirPods-Generation-Lightning/dp/B0DFJTWSJL)\",\n        \"features\": \"- 5 hours of listening time per charge - Up to 30 hour total battery life (based on normal use) - Support for spatial audio and voice activated personal assistant Siri - Waterproof and sweat-resistant - Compatible with Apple devices such as iPhone, iPad, iPod, Mac, and Apple Watch\"\n    }\n]",
    "\n\n[\n    {\n        \"product\": \"Apple Airpods (2nd Generation) With Charging Case\",\n        \"price\": \"$null\",\n        \"source\": \"[Target](https://www.target.com/p/apple-airpods-2nd-generation-with-charging-case/-/A-54191097)\",\n        \"features\": \"- 6 hours battery life - Charging case provides additional 3 hours playtime - Wireless earbuds for freedom and convenience - High-quality audio with clear and crisp sound\"\n    },\n    {\n        \"product\": \"Apple Airpods Pro 2 With Active Noise Cancellation\",\n        \"price\": \"$null\",\n        \"source\": \"[Target](https://www.target.com/p/airpods-pro-2nd-generation-with-magsafe-case-usb-c/-/A-85978622)\",\n        \"features\": \"- 4 hours battery life - Fast charging gives you 1 hour of playtime with just 5 minutes of charging - Committed to delivering high-quality audio\"\n    },\n    {\n        \"product\": \"Refurbished Apple Airpods True Wireless Bluetooth Headphones\",\n        \"price\": \"$null\",\n        \"source\": \"[Target](https://www.target.com/p/refurbished-apple-airpods-true-wireless-bluetooth-headphones-with-charging-case-2019-2nd-generation-target-certified-refurbished/-/A-92202782)\",\n        \"features\": \"- 5 hours battery life - Compatible with iPhone, iPad, and iPod\"\n    },\n    {\n        \"product\": \"Apple AirPods (3rd Generation) With Lightning Charging Case\",\n        \"price\": \"$null\",\n        \"source\": \"[Target](https://www.target.com/p/ap2022-true-wireless-bluetooth-headphones/-/A-85978615)\",\n        \"features\": \"- 4.2 out of 5 stars with 2070 ratings\"\n    },\n    {\n        \"product\": \"Apple AirPods Pro 2 (2nd Generation) With Active Noise Cancellation\",\n        \"price\": \"$null\",\n        \"source\": \"[Target](https://www.target.com/p/ap2022-true-wireless-bluetooth-headphones/-/A-85978618)\",\n        \"features\": \"- 4 hours battery life\"\n    }\n]",
    "\n\n[\n    {\n        \"product\": \"Apple AirPods Wireless Ear Buds, Bluetooth Headphones\",\n        \"price\": \"Not provided in the search results.\",\n        \"source\": \"[Amazon](https://www.amazon.com/Apple-AirPods-Charging-Latest-Model/dp/B07PXGQC1Q)\",\n        \"features\": \"- Seamless connectivity with Apple devices - Up to 4 hours of talk time on a single charge - Up to 30 hours of listening time - Compatible with iPhone 6s or later\"\n    },\n    {\n        \"product\": \"Apple AirPods (3rd Generation) Wireless Ear Buds, Bluetooth\",\n        \"price\": \"Not provided in the search results.\",\n        \"source\": \"[Amazon](https://www.amazon.com/Apple-AirPods-Generation-Lighting-Charging/dp/B0BDHB9Y8H)\",\n        \"features\": \"- Up to 4 hours of talk time with a single charge - Up to 30 hours of listening time - MagSafe charging comes standard\"\n    },\n    {\n        \"product\": \"Apple AirPods 4 Wireless Earbuds, Bluetooth Headphones\",\n        \"price\": \"Not provided in the search results.\",\n        \"source\": \"[Amazon](https://www.amazon.com/Apple-Headphones-Cancellation-Transparency-Personalized/dp/B0DGJ7HYG1)\",\n        \"features\": \"- Up to 4.5 hours of talk time on a single charge - Custom high-excursion driver and amplifier for improved sound quality - Open design that doesn't require eartips - Wireless Charging (includes MagSafe)\"\n    }\n]"
  ],
  "Report": "```json\n{\n    \"vendorRankings\": [\n        {\n            \"vendor\": \"Amazon\",\n            \"products\": [\n                {\"product\": \"Apple AirPods (2nd Generation)\", \"price\": \"$199.00\"},\n                {\"product\": \"Apple AirPods (3rd Generation)\", \"price\": \"$249.00\"},\n                {\"product\": \"Apple AirPods (3rd Generation) EarPods with Lightning Charging Case\", \"price\": \"$259.00\"}\n            ]\n        },\n        {\n            \"vendor\": \"Target\",\n            \"products\": [\n                {\"product\": \"Apple Airpods (2nd Generation) With Charging Case\", \"price\": null},\n                {\"product\": \"Apple AirPods Pro 2 With Active Noise Cancellation\", \"price\": null},\n                {\"product\": \"Refurbished Apple Airpods True Wireless Bluetooth Headphones\", \"price\": null},\n                {\"product\": \"Apple AirPods (3rd Generation) With Lightning Charging Case\", \"price\": null},\n                {\"product\": \"Apple AirPods Pro 2 (2nd Generation) With Active Noise Cancellation\", \"price\": null}\n            ]\n        }\n    ]\n}\n```"
}

report="{\n    \"vendorRankings\": [\n        {\n            \"vendor\": \"Best Buy\",\n            \"products\": [\"iPhone 16 Pro\", \"iPhone 16 Plus\"],\n            \"rank\": 1\n        },\n        {\n            \"vendor\": \"Apple\",\n            \"products\": [\"iPhone 16 Pro\", \"iPhone 16 Pro Max\"],\n            \"rank\": 2\n        },\n        {\n            \"vendor\": \"T-Mobile\",\n            \"products\": [\"iPhone 16 Pro\"],\n            \"rank\": 3\n        },\n        {\n            \"vendor\": \"Best Buy Canada\",\n            \"products\": [\"iPhone 16\"],\n            \"rank\": 4\n        },\n        {\n            \"vendor\": \"Apple\",\n            \"products\": [],\n            \"rank\": 5\n        }\n    ]\n}"
output_pdf_path = "output_report.pdf"
#GIVE THE INPUT TEXT HERE --->>>>
# process_and_generate_pdf(input_text, output_pdf_path)
# results=extract_Report_details(report)
# print(results)



import re
import json
from typing import List, Union, Optional

def detect_jsons(input_string: str) -> Optional[List[Union[dict, list]]]:
    """
    Detects and extracts JSON objects or lists from a string.

    Args:
        input_string (str): The input string containing potential JSON.

    Returns:
        Optional[List[Union[dict, list]]]: A list of detected JSON objects or lists,
                                            or None if no valid JSON is found.
    """
    # Regular expression to match JSON objects or arrays
    json_pattern = r'(\{(?:[^{}]|(?R))*\}|\[(?:[^\[\]]|(?R))*\])'
    
    # Use findall to detect potential JSON strings
    potential_jsons = re.findall(json_pattern, input_string)
    detected_jsons = []
    
    for potential_json in potential_jsons:
        try:
            # Try to load the potential JSON string
            parsed_json = json.loads(potential_json)
            detected_jsons.append(parsed_json)
        except json.JSONDecodeError:
            # Skip invalid JSON strings
            continue
    
    return detected_jsons if detected_jsons else None