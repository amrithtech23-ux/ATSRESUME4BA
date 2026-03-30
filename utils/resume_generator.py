from jinja2 import Environment, FileSystemLoader
import os
from config import Config

def generate_resume_html(resume_data, experience_level):
    """Generate ATS-compliant HTML resume"""
    
    env = Environment(loader=FileSystemLoader('templates_a4'))
    template = env.get_template('ats_resume_template.html')
    
    # Determine page length based on experience level
    page_length = get_page_length(experience_level)
    
    # Format data for template
    template_data = format_resume_data(resume_data, experience_level)
    template_data['page_length'] = page_length
    template_data['a4_width'] = Config.A4_WIDTH
    template_data['a4_height'] = Config.A4_HEIGHT
    
    html_content = template.render(**template_data)
    
    return html_content

def get_page_length(experience_level):
    """Determine resume length based on experience level"""
    length_map = {
        'fresher': 1,
        'junior': 2,
        'associate': 2,
        'senior': 2,
        'principal': 3,
        'lead': 3
    }
    return length_map.get(experience_level, 2)

def format_resume_data(resume_data, experience_level):
    """Format resume data according to ATS guidelines"""
    
    formatted = resume_data.copy()
    
    # Add level-specific keywords
    keywords = get_level_keywords(experience_level)
    formatted['level_keywords'] = keywords
    
    # Format experience bullets with action verbs
    if formatted.get('experience'):
        formatted['experience'] = format_experience_bullets(
            formatted['experience'], 
            experience_level
        )
    
    return formatted

def get_level_keywords(experience_level):
    """Get ATS keywords based on experience level"""
    keywords_map = {
        'fresher': [
            'Requirements Elicitation', 'User Stories', 'JIRA', 'SQL', 
            'Agile', 'Scrum', 'Stakeholder Communication', 'Business Process Modeling'
        ],
        'junior': [
            'User Story Mapping', 'Acceptance Criteria', 'API Testing', 
            'Gap Analysis', 'Impact Analysis', 'Backlog Management', 'Agile Ceremonies'
        ],
        'associate': [
            'Stakeholder Management', 'Requirements Traceability', 'Change Management',
            'Release Management', 'Post-Implementation Reviews', 'Metrics Definition'
        ],
        'senior': [
            'Product Strategy', 'Agile Transformation', 'Data Analytics', 
            'Roadmap Planning', 'Mentorship', 'Client Advisory'
        ],
        'principal': [
            'Enterprise Architecture', 'Portfolio Management', 'Strategic Planning',
            'Center of Excellence', 'Governance Frameworks', 'Value Realization'
        ],
        'lead': [
            'Transformation Leadership', 'P&L Ownership', 'Board Reporting', 
            'Strategic Planning', 'Organizational Impact', 'Thought Leadership'
        ]
    }
    return keywords_map.get(experience_level, keywords_map['junior'])

def format_experience_bullets(experience_list, experience_level):
    """Format experience bullets with appropriate action verbs"""
    
    action_verbs = {
        'fresher': ['Assisted', 'Supported', 'Documented', 'Participated', 'Analyzed', 'Created', 'Coordinated'],
        'junior': ['Elicited', 'Authored', 'Facilitated', 'Validated', 'Managed', 'Delivered', 'Collaborated'],
        'associate': ['Led', 'Defined', 'Drove', 'Orchestrated', 'Mentored', 'Advised', 'Optimized'],
        'senior': ['Led', 'Defined', 'Drove', 'Orchestrated', 'Mentored', 'Advised', 'Optimized', 'Governed'],
        'principal': ['Directed', 'Transformed', 'Architected', 'Established', 'Strategized', 'Championed'],
        'lead': ['Directed', 'Transformed', 'Architected', 'Established', 'Strategized', 'Championed', 'Spearheaded']
    }
    
    verbs = action_verbs.get(experience_level, action_verbs['junior'])
    
    for exp in experience_list:
        # Ensure bullets start with action verbs and include metrics
        if 'project_detail' in exp:
            details = exp['project_detail'] if isinstance(exp['project_detail'], list) else exp['project_detail'].split('\n')
            formatted_details = []
            for i, detail in enumerate(details):
                if detail.strip():
                    verb = verbs[i % len(verbs)]
                    if not detail.strip().startswith(verb):
                        detail = f"{verb} {detail.strip().lower()}"
                    # Add metric placeholder if not present
                    if '%' not in detail and '$' not in detail and '+' not in detail:
                        detail = detail.rstrip('.') + ' [Add Metric]'
                    formatted_details.append(detail)
            exp['project_detail'] = formatted_details
    
    return experience_list
