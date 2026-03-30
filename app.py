from flask import Flask, render_template, request, redirect, url_for, flash, send_file, session
from config import Config
from utils.validators import validate_graduation_year, validate_experience_period
from utils.resume_generator import generate_resume_html
from utils.pdf_export import export_to_pdf
from utils.word_export import export_to_word
import os
import json
from datetime import datetime
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config.from_object(Config)

# Create directories
Config.create_directories()

# Load BA Skills Data
def load_ba_skills(level='fresher'):
    """Load BA skills from JSON file based on experience level"""
    skills_file = os.path.join(Config.DATA_DIR, f'ba_skills_{level}.json')
    if os.path.exists(skills_file):
        with open(skills_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

@app.route('/')
def index():
    """Main page - Form to collect resume data"""
    ba_skills = load_ba_skills('fresher')
    return render_template('index.html', ba_skills=ba_skills, experience_levels=Config.EXPERIENCE_LEVELS)

@app.route('/submit', methods=['POST'])
def submit():
    """Process form submission and generate resume"""
    try:
        # Extract form data
        resume_data = extract_form_data(request.form)
        experience_level = resume_data.get('experience_level', 'fresher')
        
        # Validate data
        validation_errors = validate_resume_data(resume_data)
        if validation_errors:
            for error in validation_errors:
                flash(error, 'error')
            return redirect(url_for('index'))
        
        # Load skills if not provided
        if not resume_data.get('technical_expertise'):
            ba_skills = load_ba_skills(experience_level)
            resume_data['technical_expertise'] = ba_skills.get('technical', [])
        if not resume_data.get('functional_expertise'):
            ba_skills = load_ba_skills(experience_level)
            resume_data['functional_expertise'] = ba_skills.get('functional', [])
        
        # Store in session
        session['resume_data'] = resume_data
        session['experience_level'] = experience_level
        
        return redirect(url_for('preview'))
        
    except Exception as e:
        flash(f'Error processing form: {str(e)}', 'error')
        return redirect(url_for('index'))

@app.route('/preview')
def preview():
    """Preview generated resume"""
    if 'resume_data' not in session:
        flash('No resume data found. Please fill out the form first.', 'error')
        return redirect(url_for('index'))
    
    resume_data = session['resume_data']
    experience_level = session.get('experience_level', 'fresher')
    
    # Generate HTML Resume
    resume_html = generate_resume_html(resume_data, experience_level)
    
    return render_template('preview.html', 
                         resume_html=resume_html, 
                         resume_data=resume_data,
                         experience_level=experience_level)

@app.route('/export/<format_type>')
def export(format_type):
    """Export resume to PDF or Word format"""
    if 'resume_data' not in session:
        flash('No resume data found.', 'error')
        return redirect(url_for('index'))
    
    resume_data = session['resume_data']
    experience_level = session.get('experience_level', 'fresher')
    
    try:
        filename = f"BA_Architect_Resume_{resume_data['full_name'].replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        if format_type == 'pdf':
            file_path = export_to_pdf(resume_data, experience_level, filename)
            return send_file(file_path, as_attachment=True, download_name=f"{filename}.pdf")
        
        elif format_type == 'word':
            file_path = export_to_word(resume_data, experience_level, filename)
            return send_file(file_path, as_attachment=True, download_name=f"{filename}.docx")
        
        else:
            flash('Invalid export format.', 'error')
            return redirect(url_for('preview'))
            
    except Exception as e:
        flash(f'Error exporting resume: {str(e)}', 'error')
        return redirect(url_for('preview'))

@app.route('/reset')
def reset():
    """Clear session and reset form"""
    session.clear()
    flash('Form has been reset.', 'info')
    return redirect(url_for('index'))

def extract_form_data(form_data):
    """Extract and format data from form submission"""
    return {
        'full_name': form_data.get('full_name', ''),
        'email': form_data.get('email', ''),
        'phone': form_data.get('phone', ''),
        'location': form_data.get('location', ''),
        'linkedin': form_data.get('linkedin', ''),
        'portfolio': form_data.get('portfolio', ''),
        'work_authorization': form_data.get('work_authorization', ''),
        'languages': form_data.get('languages', ''),
        'experience_level': form_data.get('experience_level', 'fresher'),
        'professional_summary': form_data.get('professional_summary', ''),
        'graduate_degree': {
            'degree_name': form_data.get('graduate_degree_name', ''),
            'institution_name': form_data.get('graduate_institution', ''),
            'graduation_year': int(form_data.get('graduate_year', 0))
        },
        'post_graduate_degree': {
            'degree_name': form_data.get('post_graduate_degree_name', ''),
            'institution_name': form_data.get('post_graduate_institution', ''),
            'graduation_year': int(form_data.get('post_graduate_year', 0)) if form_data.get('post_graduate_year') else None
        },
        'certifications': extract_certifications(form_data),
        'technical_expertise': [x.strip() for x in form_data.get('technical_expertise', '').split(',') if x.strip()],
        'functional_expertise': [x.strip() for x in form_data.get('functional_expertise', '').split(',') if x.strip()],
        'domain_expertise': [x.strip() for x in form_data.get('domain_expertise', '').split(',') if x.strip()],
        'core_competencies': [x.strip() for x in form_data.get('core_competencies', '').split(',') if x.strip()],
        'tools_technologies': [x.strip() for x in form_data.get('tools_technologies', '').split(',') if x.strip()],
        'experience': extract_experience(form_data),
        'projects': form_data.get('projects', ''),
        'volunteering': form_data.get('volunteering', ''),
        'publications': form_data.get('publications', ''),
        'awards': form_data.get('awards', ''),
        'interests': form_data.get('interests', '')
    }

def extract_certifications(form_data):
    """Extract certifications from form data"""
    certifications = []
    i = 0
    while True:
        cert_name = form_data.get(f'certification_name_{i}', '')
        if not cert_name:
            break
        certifications.append({
            'certification_name': cert_name,
            'institution_name': form_data.get(f'certification_institution_{i}', ''),
            'certification_year': int(form_data.get(f'certification_year_{i}', 0)) if form_data.get(f'certification_year_{i}') else None
        })
        i += 1
    return certifications

def extract_experience(form_data):
    """Extract experience from form data"""
    experience = []
    i = 0
    while True:
        org_name = form_data.get(f'experience_org_{i}', '')
        if not org_name:
            break
        experience.append({
            'organization_name': org_name,
            'role': form_data.get(f'experience_role_{i}', ''),
            'job_start_year': int(form_data.get(f'experience_start_year_{i}', 0)),
            'job_end_year': form_data.get(f'experience_end_year_{i}', '') or 'Present',
            'project_detail': form_data.get(f'experience_details_{i}', '').split('\n')
        })
        i += 1
    return experience

def validate_resume_data(data):
    """Validate resume data"""
    errors = []
    
    # Required fields
    required_fields = ['full_name', 'email', 'phone', 'location', 'professional_summary']
    for field in required_fields:
        if not data.get(field):
            errors.append(f'{field.replace("_", " ").title()} is required')
    
    # Email validation
    import re
    if data.get('email') and not re.match(Config.EMAIL_REGEX, data['email']):
        errors.append('Invalid email format')
    
    # Graduation year validation
    grad_year = data.get('graduate_degree', {}).get('graduation_year', 0)
    if not validate_graduation_year(grad_year):
        errors.append(f'Graduation year must be between {Config.GRADUATION_YEAR_MIN} and {Config.GRADUATION_YEAR_MAX}')
    
    # Experience validation
    for exp in data.get('experience', []):
        if not validate_experience_period(exp.get('job_start_year', 0), exp.get('job_end_year')):
            errors.append(f'Invalid experience period for {exp.get("organization_name", "an organization")}')
    
    return errors

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
