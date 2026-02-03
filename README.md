# 🏗️ Osdag Structural Engineering Dashboard

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-2.3+-green.svg)](https://flask.palletsprojects.com)
[![PyTest](https://img.shields.io/badge/PyTest-7.0+-red.svg)](https://pytest.org)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A web-based structural engineering utility dashboard inspired by **Osdag**, providing load calculations, safety factor validation, and section capacity analysis per **IS 800:2007** (Indian Standard for General Construction in Steel).

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Running the Application](#running-the-application)
- [Running Tests](#running-tests)
- [API Endpoints](#api-endpoints)
- [Screenshots](#screenshots)
- [Engineering Calculations](#engineering-calculations)
- [Future Scope](#future-scope)
- [Author](#author)

---

## 🎯 Overview

This project is developed as part of the **FOSSEE Osdag Semester Long Internship – 2026** screening task. It demonstrates:

- Backend engineering calculation logic following IS 800:2007
- Web-based dashboard for structural analysis
- Comprehensive unit testing using PyTest
- Clean, modular, and extensible code architecture

The dashboard allows structural engineers to:
- Calculate factored loads for different combinations
- Validate safety factors
- Check section utilization ratios
- Calculate moment and shear capacities
- Verify deflection serviceability
- Retrieve material properties for steel grades

---

## ✨ Features

### Backend Features
- ✅ Load combination calculations (Normal, Wind, Seismic)
- ✅ Factored load calculations per IS 800:2007
- ✅ Safety factor validation with margin calculation
- ✅ Section utilization ratio analysis
- ✅ Moment capacity calculation
- ✅ Shear capacity calculation
- ✅ Deflection serviceability check
- ✅ Material properties lookup (IS 2062 steel grades)
- ✅ Complete structural analysis workflow

### Dashboard Features
- ✅ Modern, responsive web interface
- ✅ Interactive calculation type selection
- ✅ Real-time input validation
- ✅ Clear results display with status indicators
- ✅ Reference information panel
- ✅ Error handling with user-friendly messages

### Testing Features
- ✅ 50+ comprehensive test cases
- ✅ Normal calculation tests
- ✅ Boundary value tests
- ✅ Invalid input tests
- ✅ Exception handling tests
- ✅ Integration tests

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|------------|
| Backend | Python 3.8+ |
| Web Framework | Flask 2.3+ |
| Testing | PyTest 7.0+ |
| Coverage | pytest-cov 4.0+ |
| Frontend | HTML5, CSS3, JavaScript |
| Styling | Custom CSS (No frameworks) |

---

## 📁 Project Structure

```
osdag_pytest_submission/
├── app/
│   ├── __init__.py          # Application factory
│   ├── main.py              # Flask routes and views
│   ├── calculations.py      # Engineering calculation functions
│   ├── validators.py        # Input validation functions
│   └── config.py            # Configuration and constants
├── templates/
│   └── index.html           # Dashboard UI template
├── static/
│   └── style.css            # Dashboard styling
├── tests/
│   ├── __init__.py
│   ├── test_calculations.py # Tests for calculations module
│   └── test_validators.py   # Tests for validators module
├── run.py                   # Application entry point
├── requirements.txt         # Python dependencies
├── README.md                # Project documentation
└── REPORT.txt               # Detailed project report
```

---

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/osdag-structural-dashboard.git
   cd osdag-structural-dashboard
   ```

2. **Create virtual environment**
   ```bash
   python -m venv .venv
   ```

3. **Activate virtual environment**
   
   Windows:
   ```bash
   .venv\Scripts\activate
   ```
   
   Linux/Mac:
   ```bash
   source .venv/bin/activate
   ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

---

## ▶️ Running the Application

### Start the Dashboard

```bash
python run.py
```

The dashboard will be available at: **http://127.0.0.1:5000**

### Alternative Method

```bash
flask --app app run --debug
```

---

## 🧪 Running Tests

### Run All Tests

```bash
pytest -v
```

### Run with Coverage Report

```bash
pytest --cov=app --cov-report=term-missing
```

### Run Specific Test File

```bash
pytest tests/test_calculations.py -v
pytest tests/test_validators.py -v
```

### Expected Output

```
======================= test session starts =======================
collected 53 items

tests/test_calculations.py::TestFactoredLoadCalculations::test_normal_combination_basic PASSED
tests/test_calculations.py::TestFactoredLoadCalculations::test_wind_combination PASSED
...
tests/test_validators.py::TestValidateNumeric::test_valid_integer PASSED
...
======================= 53 passed in 0.45s =======================
```

---

## 🔌 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Main dashboard page |
| `/calculate` | POST | Perform calculation |
| `/complete-analysis` | POST | Complete structural analysis |
| `/api/steel-grades` | GET | Get available steel grades |
| `/api/load-combinations` | GET | Get load combination types |

---

## 📸 Screenshots

### Dashboard Overview
*[Screenshot placeholder - Main dashboard view]*

### Calculation Results
*[Screenshot placeholder - Results display with safety status]*

### Reference Panel
*[Screenshot placeholder - IS 800:2007 reference information]*

---

## 📐 Engineering Calculations

### Load Combinations (IS 800:2007)

| Combination | Formula |
|-------------|---------|
| Normal | 1.5×DL + 1.5×LL |
| Wind | 1.2×(DL + LL + WL) |
| Seismic | 1.2×(DL + LL + EQ) |

### Safety Factors

| Factor | Value | Description |
|--------|-------|-------------|
| γ_DL | 1.5 | Dead load factor |
| γ_LL | 1.5 | Live load factor |
| γ_m0 | 1.10 | Material factor (yielding) |
| γ_m1 | 1.25 | Material factor (ultimate) |

### Steel Grades (IS 2062)

| Grade | Yield Strength (MPa) | Ultimate Strength (MPa) |
|-------|---------------------|------------------------|
| E250 | 250 | 410 |
| E275 | 275 | 430 |
| E300 | 300 | 440 |
| E350 | 350 | 490 |
| E410 | 410 | 540 |
| E450 | 450 | 570 |

---

## 🔮 Future Scope

1. **Extended Calculations**
   - Beam design module
   - Column design module
   - Connection design calculations

2. **Enhanced Dashboard**
   - Interactive structural diagrams
   - PDF report generation
   - Calculation history

3. **Database Integration**
   - User accounts
   - Project management
   - Section database

4. **API Extensions**
   - RESTful API for integration
   - Batch calculation support
   - External tool integration

5. **Deployment**
   - Docker containerization
   - Cloud deployment (AWS/Azure)
   - CI/CD pipeline

---

## 👤 Author

**Name:** Suman Kumar  
**Email:** suman_2312res675@iitp.ac.in  
**GitHub:** [sumansingh20](https://github.com/sumansingh20)

- Project: FOSSEE Osdag Screening Task 2026
- Track: Software Development
- Focus: Unit Testing with PyTest

---

## 📄 License

This project is developed for educational purposes as part of the FOSSEE Osdag internship screening process.

---

## 🙏 Acknowledgments

- [FOSSEE](https://fossee.in/) - Free/Libre and Open Source Software for Education
- [Osdag](https://osdag.fossee.in/) - Open Steel Design and Graphics
- IS 800:2007 - Indian Standard for General Construction in Steel
- IS 2062 - Hot Rolled Medium and High Tensile Structural Steel

---

*Developed with ❤️ for FOSSEE Osdag Internship 2026*
