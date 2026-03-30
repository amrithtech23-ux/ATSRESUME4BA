import streamlit as st
import json
import os
from datetime import datetime
from utils.validators import validate_graduation_year, validate_experience_period
from utils.resume_generator import generate_resume_html
import tempfile

# Page config - MUST be first Streamlit command
st.set_page_config(
    page_title="The BA Architect - ATS Resume Generator",
    page_icon="📄",
    layout="wide"
)

# Initialize ALL session state at the very top
if 'experience_level' not in st.session_state:
    st.session_state.experience_level = 'fresher'
if 'num_positions' not in st.session_state:
    st.session_state.num_positions = 0
if 'num_certs' not in st.session_state:
    st.session_state.num_certs = 0

# Title
st.title("📄 The BA Architect")
st.subheader("ATS-Compliant IT Business Analyst Resume Generator")

# Load BA Skills
def load_ba_skills(level):
    skills_file = f'data/ba_skills_{level}.json'
    if os.path.exists(skills_file):
        with open(skills_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

# Sidebar
st.sidebar.header("Select Experience Level")
exp_level = st.sidebar.selectbox(
    "Your Level",
    ['fresher', 'junior', 'associate', 'senior', 'principal', 'lead'],
    format_func=lambda x: x.title(),
    index=['fresher', 'junior', 'associate', 'senior', 'principal', 'lead'].index(st.session_state.experience_level)
)

if exp_level != st.session_state.experience_level:
    st.session_state.experience_level = exp_level
    st.rerun()

ba_skills = load_ba_skills(st.session_state.experience_level)

# Personal Information
st.header("Personal Information")
col1, col2 = st.columns(2)

with col1:
    full_name = st.text_input("Full Name *", key="full_name")
    email = st.text_input("Email Address *", key="email")
    phone = st.text_input("Phone Number *", key="phone")
    linkedin = st.text_input("LinkedIn Profile", key="linkedin")

with col2:
    location = st.text_input("Location (City, Country) *", key="location")
    portfolio = st.text_input("Portfolio/GitHub URL", key="portfolio")
    work_auth = st.text_input("Work Authorization", key="work_auth")
    languages = st.text_input("Languages", key="languages")

# Education
st.header("Education")
col1, col2 = st.columns(2)

with col1:
    st.subheader("Graduate Degree (Mandatory)")
    grad_degree = st.text_input("Degree Name *", key="grad_degree")
    grad_institution = st.text_input("Institution *", key="grad_institution")
    grad_year = st.number_input("Graduation Year *", min_value=1990, max_value=2026, key="grad_year", value=2020)

with col2:
    st.subheader("Post Graduate (Optional)")
    post_grad_degree = st.text_input("Degree Name", key="post_grad_degree")
    post_grad_institution = st.text_input("Institution", key="post_grad_institution")
    post_grad_year = st.number_input("Graduation Year", min_value=1990, max_value=2026, key="pg_year", value=2020)

# Professional Summary
st.header("Professional Summary")
professional_summary = st.text_area("Professional Summary (3-4 sentences) *", height=100, key="professional_summary")

# Core Competencies
st.header("Core Competencies")
default_competencies = ", ".join(ba_skills.get('functional', [])[:10]) if ba_skills else ""
core_competencies = st.text_area("Core Competencies (comma separated) *", height=80, value=default_competencies, key="core_competencies")

# Expertise
st.header("Expertise")
col1, col2 = st.columns(2)

with col1:
    default_tech = ", ".join(ba_skills.get('technical', [])) if ba_skills else ""
    technical_expertise = st.text_area("Technical Expertise (comma separated)", height=80, value=default_tech, key="technical_expertise")

with col2:
    default_func = ", ".join(ba_skills.get('functional', [])) if ba_skills else ""
    functional_expertise = st.text_area("Functional Expertise (comma separated)", height=80, value=default_func, key="functional_expertise")

domain_expertise = st.text_input("Domain Expertise (comma separated)", key="domain_expertise")

# Professional Experience Section
st.header("Professional Experience")

# Number input with explicit callback pattern
current_num_positions = st.number_input(
    "Number of Positions",
    min_value=0,
    max_value=10,
    value=st.session_state.num_positions,
    key="num_positions_input",
    help="Set the number, then scroll down to see the fields"
)

# Check if value changed and update session state
if current_num_positions != st.session_state.num_positions:
    st.session_state.num_positions = current_num_positions
    # Force re-run to show/hide fields
    st.rerun()

experience = []

# Render positions based on session state (not the input directly)
for i in range(st.session_state.num_positions):
    st.subheader(f"Position {i+1}")
    col1, col2 = st.columns(2)
    
    with col1:
        org_name = st.text_input("Organization Name *", key=f"org_{i}")
        role = st.text_input("Role *", key=f"role_{i}")
    
    with col2:
        start_year = st.number_input("Start Year *", min_value=1990, max_value=2026, key=f"start_{i}", value=2020)
        end_year = st.text_input("End Year (or 'Present')", value="Present", key=f"end_{i}")
    
    project_details = st.text_area("Project Details (one per line)", height=150, key=f"details_{i}")
    
    if org_name and role:
        experience.append({
            'organization_name': org_name,
            'role': role,
            'job_start_year': start_year,
            'job_end_year': end_year,
            'project_detail': project_details.split('\n') if project_details else []
        })
    
    if i < st.session_state.num_positions - 1:
        st.markdown("---")

# Certifications Section
st.header("Certifications")

# Number input with explicit callback pattern
current_num_certs = st.number_input(
    "Number of Certifications",
    min_value=0,
    max_value=10,
    value=st.session_state.num_certs,
    key="num_certs_input",
    help="Set the number, then scroll down to see the fields"
)

# Check if value changed and update session state
if current_num_certs != st.session_state.num_certs:
    st.session_state.num_certs = current_num_certs
    # Force re-run to show/hide fields
    st.rerun()

certifications = []

# Render certifications based on session state (not the input directly)
for i in range(st.session_state.num_certs):
    st.subheader(f"Certification {i+1}")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        cert_name = st.text_input("Certification Name *", key=f"cert_name_{i}")
    with col2:
        cert_institution = st.text_input("Institution", key=f"cert_inst_{i}")
    with col3:
        cert_year = st.number_input("Year", min_value=1990, max_value=2026, key=f"cert_year_{i}", value=2024)
    
    if cert_name:
        certifications.append({
            'certification_name': cert_name,
            'institution_name': cert_institution,
            'certification_year': cert_year
        })
    
    if i < st.session_state.num_certs - 1:
        st.markdown("---")

# Additional Information
st.header("Additional Information")
col1, col2 = st.columns(2)

with col1:
    projects = st.text_area("Key Projects (For Freshers)", height=80, key="projects")
    volunteering = st.text_area("Volunteering & Leadership", height=80, key="volunteering")

with col2:
    publications = st.text_area("Publications", height=80, key="publications")
    awards = st.text_area("Awards", height=80, key="awards")

interests = st.text_input("Interests", key="interests")

# Submit button
if st.button("Generate Resume", type="primary"):
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
            'experience_level': st.session_state.experience_level,
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
        
        # Generate resume HTML
        try:
            resume_html = generate_resume_html(resume_data, st.session_state.experience_level)
            
            st.success("✅ Resume Generated Successfully!")
            
            # Display preview
            st.header("Resume Preview")
            st.components.v1.html(resume_html, height=800, scrolling=True)
            
            # Download options
            st.header("Download Options")
            col1, col2 = st.columns(2)
            
            with col1:
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
                st.info("💡 For PDF/Word export, use browser's Print to PDF feature")
        
        except Exception as e:
            st.error(f"Error generating resume: {str(e)}")
            st.exception(e)

# Footer
st.markdown("---")
st.markdown("© 2026 The BA Architect - ATS-Compliant IT Business Analyst Resume Generator")
