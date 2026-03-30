# The BA Architect - IT Business Analyst ATS Resume Generator

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0.0-green.svg)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

AI-powered web application for generating ATS-compliant IT Business Analyst resumes in A4 format. Targets both fresh graduates and experienced professionals.

## ✨ Features

- ✅ **ATS-Optimized Format** - Single column, standard headings, no graphics
- ✅ **A4 Page Layout** - Professional international standard
- ✅ **Auto-Suggested Skills** - Based on experience level (Fresher to Lead)
- ✅ **PDF & Word Export** - Both ATS-compatible formats
- ✅ **Email & Year Validation** - Real-time form validation
- ✅ **Experience Timeline Validation** - Ensures logical career progression
- ✅ **Bootstrap 5 Responsive UI** - Works on all devices
- ✅ **Session-Based Preview** - Review before exporting
- ✅ **Auto-Save Functionality** - Never lose your progress

## 📊 Experience Levels Supported

| Level | Experience | Pages |
|-------|-----------|-------|
| Fresher | 0-12 months | 1 page |
| Junior | 1-3 years | 2 pages |
| Associate | 3-6 years | 2 pages |
| Senior | 6-8 years | 2 pages |
| Principal | 8-10 years | 3 pages |
| Lead | 10-15+ years | 3 pages |

## 🚀 Installation

### Prerequisites

- Python 3.8 or higher
- wkhtmltopdf (for PDF export)

### Step-by-Step Setup

```bash
# 1. Clone the repository
git clone https://github.com/amrithtech23-ux/ba-architect-resume-generator.git
cd ba-architect-resume-generator

# 2. Create virtual environment
python -m venv venv

# 3. Activate virtual environment
# Windows
venv\Scripts\activate
# Mac/Linux
source venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Install wkhtmltopdf
# Windows: Download from https://wkhtmltopdf.org/downloads.html
# Mac: brew install wkhtmltopdf
# Linux: sudo apt-get install wkhtmltopdf

# 6. Create .env file
cp .env.example .env
# Edit .env and set your SECRET_KEY

# 7. Run application
python app.py
