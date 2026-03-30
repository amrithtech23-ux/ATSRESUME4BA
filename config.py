import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Application configuration class"""
    
    # Secret Key
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    
    # Flask Settings
    WTF_CSRF_ENABLED = True
    MAX_CONTENT_LENGTH = int(os.environ.get('MAX_CONTENT_LENGTH', 16 * 1024 * 1024))  # 16MB
    
    # A4 Page Settings (in mm)
    A4_WIDTH = 210
    A4_HEIGHT = 297
    A4_WIDTH_PX = 794  # pixels at 96 DPI
    A4_HEIGHT_PX = 1123  # pixels at 96 DPI
    
    # Export Settings
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    EXPORT_DIR = os.path.join(BASE_DIR, 'exports')
    TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates_a4')
    DATA_DIR = os.path.join(BASE_DIR, 'data')
    
    # Validation Rules
    GRADUATION_YEAR_MIN = 1990
    GRADUATION_YEAR_MAX = 2026
    MIN_EXPERIENCE_YEARS = 0
    MAX_EXPERIENCE_YEARS = 40
    
    # Email Validation
    EMAIL_REGEX = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    # Experience Levels
    EXPERIENCE_LEVELS = {
        'fresher': {'min_years': 0, 'max_years': 1, 'pages': 1},
        'junior': {'min_years': 1, 'max_years': 3, 'pages': 2},
        'associate': {'min_years': 3, 'max_years': 6, 'pages': 2},
        'senior': {'min_years': 6, 'max_years': 8, 'pages': 2},
        'principal': {'min_years': 8, 'max_years': 10, 'pages': 3},
        'lead': {'min_years': 10, 'max_years': 15, 'pages': 3}
    }
    
    # Allowed Extensions
    ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx'}
    
    @classmethod
    def create_directories(cls):
        """Create necessary directories if they don't exist"""
        os.makedirs(cls.EXPORT_DIR, exist_ok=True)
        os.makedirs(cls.TEMPLATE_DIR, exist_ok=True)
        os.makedirs(cls.DATA_DIR, exist_ok=True)
