import streamlit as st
import fitz
import re
import base64  # Import base64 module for encoding

# Function to detect email addresses in a given line of text
def detect_emails(text):
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    return re.findall(email_pattern, text)

def extract_emails_from_pdf(file_path):
    all_emails = []
    with fitz.open(file_path) as doc:
        for page in doc:
            file_text = page.get_text()
            lines = file_text.splitlines()
            for line in lines:
                line = line.strip()
                if line:  # Continue the program to detect email id
                    emails = detect_emails(line)
                    all_emails.extend(emails)
    return all_emails

def main():
    st.title("Email Extractor from PDF")
    
    uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")
    
    if uploaded_file is not None:
        # Save uploaded file temporarily
        with open("temp.pdf", "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        st.write("Extracting emails...")
        
        # Extract emails
        emails = extract_emails_from_pdf("temp.pdf")
        
        if emails:
            # Display emails in a scrollable box
            st.markdown("### Extracted Emails")
            st.text_area("Emails", "\n".join(emails), height=300)
            
            # Allow user to download the emails as a text file
            st.markdown("### Download Emails")
            email_text = "\n".join(emails)
            st.markdown(get_download_link(email_text, "emails.txt", "Download emails as text file"), unsafe_allow_html=True)
            
        else:
            st.write("No emails found in the PDF.")

def get_download_link(text, filename, text_display):
    """Generate a download link for a text file."""
    b64 = base64.b64encode(text.encode()).decode()  # Encode the text to base64
    href = f'<a href="data:file/txt;base64,{b64}" download="{filename}">{text_display}</a>'
    return href

if __name__ == "__main__":
    main()
