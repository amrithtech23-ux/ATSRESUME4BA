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
if 'experience_level' not in st.session_state:
    st.session_state.experience_level = 'fresher'

# Load BA Skills
def load_ba_skills(level):
    skills_file = f'data/ba_skills_{level}.json'
    if os.path.exists(skills_file):
        with open(skills_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

# Sidebar
st.sidebar.header("Select Experience Level")
experience_level = st.sidebar.selectbox(
    "Your Level",
    ['fresher', 'junior', 'associate', 'senior', 'principal', 'lead'],
    format_func=lambda x: x.title()
)

st.session_state.experience_level = experience_level
ba_skills = load_ba_skills(experience_level)

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

# Certifications - RIGHT AFTER EDUCATION (Optional)
st.header("Certifications (Optional)")
st.markdown("*Fill in certifications if applicable. Leave blank if not.*")

certifications = []

# Certification 1
col1, col2, col3 = st.columns(3)
with col1:
    cert1_name = st.text_input("Certification 1 Name", key="cert1_name")
with col2:
    cert1_inst = st.text_input("Institution", key="cert1_inst")
with col3:
    cert1_year = st.number_input("Year", min_value=1990, max_value=2026, key="cert1_year", value=2024)

if cert1_name:
    certifications.append({
        'certification_name': cert1_name,
        'institution_name': cert1_inst,
        'certification_year': cert1_year
    })

# Certification 2
col1, col2, col3 = st.columns(3)
with col1:
    cert2_name = st.text_input("Certification 2 Name", key="cert2_name")
with col2:
    cert2_inst = st.text_input("Institution", key="cert2_inst")
with col3:
    cert2_year = st.number_input("Year", min_value=1990, max_value=2026, key="cert2_year", value=2024)

if cert2_name:
    certifications.append({
        'certification_name': cert2_name,
        'institution_name': cert2_inst,
        'certification_year': cert2_year
    })

# Certification 3
col1, col2, col3 = st.columns(3)
with col1:
    cert3_name = st.text_input("Certification 3 Name", key="cert3_name")
with col2:
    cert3_inst = st.text_input("Institution", key="cert3_inst")
with col3:
    cert3_year = st.number_input("Year", min_value=1990, max_value=2026, key="cert3_year", value=2024)

if cert3_name:
    certifications.append({
        'certification_name': cert3_name,
        'institution_name': cert3_inst,
        'certification_year': cert3_year
    })

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
st.markdown("*Fill in positions if applicable. Leave blank if fresher.*")

experience = []

# Position 1
st.subheader("Position 1")
col1, col2 = st.columns(2)
with col1:
    pos1_org = st.text_input("Organization Name", key="pos1_org")
    pos1_role = st.text_input("Role", key="pos1_role")
with col2:
    pos1_start = st.number_input("Start Year", min_value=1990, max_value=2026, key="pos1_start", value=2020)
    pos1_end = st.text_input("End Year (or 'Present')", value="Present", key="pos1_end")
pos1_details = st.text_area("Project Details (one per line)", height=100, key="pos1_details")

if pos1_org and pos1_role:
    experience.append({
        'organization_name': pos1_org,
        'role': pos1_role,
        'job_start_year': pos1_start,
        'job_end_year': pos1_end,
        'project_detail': pos1_details.split('\n') if pos1_details else []
    })

# Position 2
st.subheader("Position 2")
col1, col2 = st.columns(2)
with col1:
    pos2_org = st.text_input("Organization Name", key="pos2_org")
    pos2_role = st.text_input("Role", key="pos2_role")
with col2:
    pos2_start = st.number_input("Start Year", min_value=1990, max_value=2026, key="pos2_start", value=2020)
    pos2_end = st.text_input("End Year (or 'Present')", value="Present", key="pos2_end")
pos2_details = st.text_area("Project Details (one per line)", height=100, key="pos2_details")

if pos2_org and pos2_role:
    experience.append({
        'organization_name': pos2_org,
        'role': pos2_role,
        'job_start_year': pos2_start,
        'job_end_year': pos2_end,
        'project_detail': pos2_details.split('\n') if pos2_details else []
    })

# Position 3
st.subheader("Position 3")
col1, col2 = st.columns(2)
with col1:
    pos3_org = st.text_input("Organization Name", key="pos3_org")
    pos3_role = st.text_input("Role", key="pos3_role")
with col2:
    pos3_start = st.number_input("Start Year", min_value=1990, max_value=2026, key="pos3_start", value=2020)
    pos3_end = st.text_input("End Year (or 'Present')", value="Present", key="pos3_end")
pos3_details = st.text_area("Project Details (one per line)", height=100, key="pos3_details")

if pos3_org and pos3_role:
    experience.append({
        'organization_name': pos3_org,
        'role': pos3_role,
        'job_start_year': pos3_start,
        'job_end_year': pos3_end,
        'project_detail': pos3_details.split('\n') if pos3_details else []
    })

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
