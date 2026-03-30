import streamlit as st
import json
import os
from datetime import datetime
from utils.validators import validate_graduation_year, validate_experience_period
from utils.resume_generator import generate_resume_html
import tempfile

# Page config
st.set_page_config(
    page_title="The BA Architect - ATS Resume Generator",
    page_icon="📄",
    layout="wide"
)

# Title
st.title("📄 The BA Architect")
st.subheader("ATS-Compliant IT Business Analyst Resume Generator")

# Initialize session state
if 'resume_data' not in st.session_state:
    st.session_state.resume_data = None
if 'experience_level' not in st.session_state:
    st.session_state.experience_level = 'fresher'

# Load BA Skills
def load_ba_skills(level):
    skills_file = f'data/ba_skills_{level}.json'
    if os.path.exists(skills_file):
        with open(skills_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

# Sidebar - Experience Level
st.sidebar.header("Select Experience Level")
experience_level = st.sidebar.selectbox(
    "Your Level",
    ['fresher', 'junior', 'associate', 'senior', 'principal', 'lead'],
    format_func=lambda x: x.title()
)

st.session_state.experience_level = experience_level

# Load skills for auto-suggestions
ba_skills = load_ba_skills(experience_level)

# Main Form
with st.form("resume_form", clear_on_submit=False):
    st.header("Personal Information")
    col1, col2 = st.columns(2)
    
    with col1:
        full_name = st.text_input("Full Name *", "")
        email = st.text_input("Email Address *", "")
        phone = st.text_input("Phone Number *", "")
        linkedin = st.text_input("LinkedIn Profile", "")
    
    with col2:
        location = st.text_input("Location (City, Country) *", "")
        portfolio = st.text_input("Portfolio/GitHub URL", "")
        work_auth = st.text_input("Work Authorization", "")
        languages = st.text_input("Languages", "")
    
    st.header("Education")
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Graduate Degree (Mandatory)")
        grad_degree = st.text_input("Degree Name *", "")
        grad_institution = st.text_input("Institution *", "")
        grad_year = st.number_input("Graduation Year *", min_value=1990, max_value=2026)
    
    with col2:
        st.subheader("Post Graduate (Optional)")
        post_grad_degree = st.text_input("Degree Name", "")
        post_grad_institution = st.text_input("Institution", "")
        post_grad_year = st.number_input("Graduation Year", min_value=1990, max_value=2026, key="pg_year")
    
    st.header("Professional Summary")
    professional_summary = st.text_area(
        "Professional Summary (3-4 sentences) *",
        height=100,
        help="Summarize your experience, core competencies, and value proposition"
    )
    
    st.header("Core Competencies")
    core_competencies = st.text_area(
        "Core Competencies (comma separated) *",
        height=80,
        value=", ".join(ba_skills.get('functional', [])[:10]) if ba_skills else ""
    )
    
    st.header("Expertise")
    col1, col2 = st.columns(2)
    
    with col1:
        technical_expertise = st.text_area(
            "Technical Expertise (comma separated)",
            height=80,
            value=", ".join(ba_skills.get('technical', [])) if ba_skills else ""
        )
    
    with col2:
        functional_expertise = st.text_area(
            "Functional Expertise (comma separated)",
            height=80,
            value=", ".join(ba_skills.get('functional', [])) if ba_skills else ""
        )
    
    domain_expertise = st.text_input("Domain Expertise (comma separated)", "")
    
    # FIX ISSUE 1: Professional Experience Section
    st.header("Professional Experience")
    num_positions = st.number_input("Number of Positions", min_value=0, max_value=10, value=0, 
                                    help="Enter number of positions you want to add (0-10)")
    
    experience = []
    
    # Render position fields based on num_positions
    if num_positions > 0:
        for i in range(int(num_positions)):
            st.subheader(f"Position {i+1}")
            col1, col2 = st.columns(2)
            
            with col1:
                org_name = st.text_input("Organization Name *", key=f"org_{i}")
                role = st.text_input("Role *", key=f"role_{i}")
            
            with col2:
                start_year = st.number_input("Start Year *", min_value=1990, max_value=2026, 
                                           key=f"start_{i}", value=2020)
                end_year = st.text_input("End Year (or 'Present')", value="Present", key=f"end_{i}")
            
            project_details = st.text_area(
                "Project Details (one per line)",
                height=150,
                key=f"details_{i}",
                help="Enter each project responsibility/achievement on a new line"
            )
            
            # Only add to experience if organization and role are filled
            if org_name and role:
                experience.append({
                    'organization_name': org_name,
                    'role': role,
                    'job_start_year': start_year,
                    'job_end_year': end_year,
                    'project_detail': project_details.split('\n') if project_details else []
                })
            
            # Add separator between positions
            if i < num_positions - 1:
                st.markdown("---")
    
    # FIX ISSUE 2: Certifications Section
    st.header("Certifications")
    num_certs = st.number_input("Number of Certifications", min_value=0, max_value=10, value=0,
                                help="Enter number of certifications you want to add (0-10)")
    
    certifications = []
    
    # Render certification fields based on num_certs
    if num_certs > 0:
        for i in range(int(num_certs)):
            st.subheader(f"Certification {i+1}")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                cert_name = st.text_input("Certification Name *", key=f"cert_name_{i}")
            with col2:
                cert_institution = st.text_input("Institution", key=f"cert_inst_{i}")
            with col3:
                cert_year = st.number_input("Year", min_value=1990, max_value=2026, 
                                          key=f"cert_year_{i}", value=2024)
            
            # Only add to certifications if name is filled
            if cert_name:
                certifications.append({
                    'certification_name': cert_name,
                    'institution_name': cert_institution,
                    'certification_year': cert_year
                })
            
            # Add separator between certifications
            if i < num_certs - 1:
                st.markdown("---")
    
    st.header("Additional Information")
    col1, col2 = st.columns(2)
    
    with col1:
        projects = st.text_area("Key Projects (For Freshers)", height=80)
        volunteering = st.text_area("Volunteering & Leadership", height=80)
    
    with col2:
        publications = st.text_area("Publications", height=80)
        awards = st.text_area("Awards", height=80)
    
    interests = st.text_input("Interests", "")
    
    # Submit button
    submitted = st.form_submit_button("Generate Resume", type="primary")

if submitted:
    # Validate required fields
    required_fields = {
        'Full Name': full_name,
        'Email': email,
        'Phone': phone,
        'Location': location,
        'Professional Summary': professional_summary,
        'Graduate Degree': grad_degree,
        'Graduate Institution': grad_institution
    }
    
    missing_fields = [field for field, value in required_fields.items() if not value]
    
    if missing_fields:
        st.error(f"Please fill in all required fields: {', '.join(missing_fields)}")
    else:
        # Compile resume data
        resume_data = {
            'full_name': full_name,
            'email': email,
            'phone': phone,
            'location': location,
            'linkedin': linkedin,
            'portfolio': portfolio,
            'work_authorization': work_auth,
            'languages': languages,
            'experience_level': experience_level,
            'professional_summary': professional_summary,
            'graduate_degree': {
                'degree_name': grad_degree,
                'institution_name': grad_institution,
                'graduation_year': grad_year
            },
            'post_graduate_degree': {
                'degree_name': post_grad_degree if post_grad_degree else None,
                'institution_name': post_grad_institution if post_grad_institution else None,
                'graduation_year': post_grad_year if post_grad_year else None
            },
            'certifications': certifications,
            'technical_expertise': [x.strip() for x in technical_expertise.split(',') if x.strip()],
            'functional_expertise': [x.strip() for x in functional_expertise.split(',') if x.strip()],
            'domain_expertise': [x.strip() for x in domain_expertise.split(',') if x.strip()],
            'core_competencies': [x.strip() for x in core_competencies.split(',') if x.strip()],
            'experience': experience,
            'projects': projects,
            'volunteering': volunteering,
            'publications': publications,
            'awards': awards,
            'interests': interests
        }
        
        st.session_state.resume_data = resume_data
        
        # Generate resume HTML
        try:
            resume_html = generate_resume_html(resume_data, experience_level)
            
            st.success("✅ Resume Generated Successfully!")
            
            # Display preview
            st.header("Resume Preview")
            st.components.v1.html(resume_html, height=800, scrolling=True)
            
            # Download options
            st.header("Download Options")
            col1, col2 = st.columns(2)
            
            with col1:
                # Save as HTML file for download
                html_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.html')
                html_file.write(resume_html)
                html_file.close()
                
                with open(html_file.name, 'r', encoding='utf-8') as f:
                    st.download_button(
                        label="📥 Download as HTML",
                        data=f.read(),
                        file_name=f"BA_Resume_{full_name.replace(' ', '_')}.html",
                        mime="text/html"
                    )
            
            with col2:
                st.info("💡 For PDF/Word export, use the HTML file and convert using your browser's Print to PDF feature")
        
        except Exception as e:
            st.error(f"Error generating resume: {str(e)}")
            st.exception(e)  # Show full traceback for debugging

# Footer
st.markdown("---")
st.markdown("© 2026 The BA Architect - ATS-Compliant IT Business Analyst Resume Generator")
