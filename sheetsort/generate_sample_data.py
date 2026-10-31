"""Generate sample college data files for SheetSort testing and demos."""
from __future__ import annotations

import pandas as pd
import numpy as np
from faker import Faker
import os

fake = Faker()


def generate_exam_roster(n_students=50, output_path=None):
    """Generate a sample exam roster Excel file."""
    departments = ['CSE', 'IT', 'ECE', 'Mechanical', 'Civil', 'Aerospace']
    semesters = ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII']
    subjects = ['Mathematics', 'Physics', 'Chemistry', 'English', 'Computer Science',
                'Physics Lab', 'Chemistry Lab', 'English Communication']
    
    rows = []
    for i in range(n_students):
        dept = np.random.choice(departments)
        sem = np.random.choice(semesters)
        subject = np.random.choice(subjects)
        roll_no = f"{dept}{np.random.randint(100, 999)}"
        exam_date = fake.date_between(start_date='-1y', end_date='today')
        marks = np.random.randint(20, 100)
        
        rows.append({
            'Student Name': fake.name(),
            'Roll Number': roll_no,
            'Department': dept,
            'Semester': sem,
            'Subject': subject,
            'Exam Date': exam_date,
            'Marks': marks,
        })
    
    df = pd.DataFrame(rows)
    
    if output_path is None:
        output_path = "sample_data/exam_roster.xlsx"
    
    os.makedirs("sample_data", exist_ok=True)
    df.to_excel(output_path, index=False, sheet_name="Exam Data")
    print(f"Generated {output_path} with {n_students} records")
    return output_path


def generate_placement_data(n_students=100, output_path=None):
    """Generate a sample placement data CSV file."""
    companies = ['Google', 'Microsoft', 'Amazon', 'Meta', 'Apple', 'Netflix', 'Twitter', 'IBM']
    branches = ['CSE', 'IT', 'ECE', 'Mechanical', 'Civil', 'EEE']
    statuses = ['Placed', 'Not Placed', 'Pre-Placement Talk']
    
    rows = []
    for i in range(n_students):
        branch = np.random.choice(branches)
        company = np.random.choice(companies)
        # Only some students are placed
        placed = np.random.random() > 0.3
        status = np.random.choice(statuses) if not placed else company
        placement_date = fake.date_between(start_date='-1y', end_date='today') if placed else None
        salary = np.random.randint(4, 20) * 1000 if placed else None
        
        rows.append({
            'Student Name': fake.name(),
            'Branch': branch,
            'Company': company if placed else '',
            'Placement Status': status if placed else 'Not Placed',
            'Placement Date': placement_date,
            'Salary (LPA)': salary,
        })
    
    df = pd.DataFrame(rows)
    
    if output_path is None:
        output_path = "sample_data/placement_data.csv"
    
    os.makedirs("sample_data", exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"Generated {output_path} with {n_students} records")
    return output_path


def generate_attendance_data(n_students=200, output_path=None):
    """Generate a sample attendance data CSV file."""
    departments = ['CSE', 'IT', 'ECE', 'Mechanical', 'Civil', 'EEE', 'Arts', 'Commerce']
    
    rows = []
    for i in range(n_students):
        dept = np.random.choice(departments)
        attendance_pct = np.random.uniform(30, 100)
        risk = "High" if attendance_pct < 50 else "Medium" if attendance_pct < 75 else "Low"
        
        rows.append({
            'Student ID': fake.unique.random_number(digits=6),
            'Student Name': fake.name(),
            'Department': dept,
            'Attendance %': round(attendance_pct, 1),
            'Risk Category': risk,
        })
    
    df = pd.DataFrame(rows)
    
    if output_path is None:
        output_path = "sample_data/attendance_sample.csv"
    
    os.makedirs("sample_data", exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"Generated {output_path} with {n_students} records")
    return output_path


if __name__ == "__main__":
    print("Generating sample data files...")
    print()
    
    gen_exam = generate_exam_roster(50, "sample_data/exam_roster.xlsx")
    gen_placement = generate_placement_data(100, "sample_data/placement_data.csv")
    gen_attendance = generate_attendance_data(200, "sample_data/attendance_sample.csv")
    
    print()
    print(f"Generated 3 sample files:")
    print(f"  - {gen_exam}")
    print(f"  - {gen_placement}")
    print(f"  - {gen_attendance}")
    print()
    print("Sample data ready for SheetSort testing!")