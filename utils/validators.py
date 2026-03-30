from datetime import datetime
from config import Config

def validate_graduation_year(year):
    """Validate graduation year is within acceptable range"""
    try:
        year = int(year)
        return Config.GRADUATION_YEAR_MIN <= year <= Config.GRADUATION_YEAR_MAX
    except (ValueError, TypeError):
        return False

def validate_experience_period(start_year, end_year=None):
    """Validate experience period is logical"""
    try:
        current_year = datetime.now().year
        start_year = int(start_year)
        
        if start_year < Config.GRADUATION_YEAR_MIN or start_year > current_year:
            return False
        
        if end_year and end_year != 'Present':
            end_year = int(end_year)
            if end_year < start_year or end_year > current_year:
                return False
        
        return True
    except (ValueError, TypeError):
        return False

def validate_email_format(email):
    """Validate email format"""
    import re
    return bool(re.match(Config.EMAIL_REGEX, email))

def validate_experience_vs_education(exp_start_year, grad_year, experience_level):
    """Validate experience timeline vs education"""
    try:
        exp_start_year = int(exp_start_year)
        grad_year = int(grad_year)
        
        if experience_level == 'fresher':
            # Freshers can have internship experience during education
            return exp_start_year >= grad_year - 1
        else:
            # Experienced should start after graduation
            return exp_start_year >= grad_year
    except (ValueError, TypeError):
        return False

def validate_required_fields(data, required_fields):
    """Validate that all required fields are present"""
    missing_fields = []
    for field in required_fields:
        if not data.get(field):
            missing_fields.append(field)
    return missing_fields

def validate_certification_year(cert_year):
    """Validate certification year"""
    try:
        cert_year = int(cert_year)
        current_year = datetime.now().year
        return Config.GRADUATION_YEAR_MIN <= cert_year <= current_year
    except (ValueError, TypeError):
        return False
