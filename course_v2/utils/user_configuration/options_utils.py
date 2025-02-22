class Options:
    def __init__(self):
        pass
    def degree_options(self):
        DEGREE_OPTIONS = {"CE": "Computer Engineering", "CSC": "Computer Science", "DSAI": "Data Science and Artificial Intelligence", "BCE": "Double Degree in Computer Engineering and Business", "CEEcons": "Double Degree in Computer Engineering and Economics", "BCG": "Double Degree in Computer Science and Business", "CSEcons": "Double Degree in Computer Science and Economics"}
        return DEGREE_OPTIONS
    def cohort_options(self):
        COHORT = ["2021", "2022", "2023", "2024"]
        return COHORT 
    def degree_type_options(self):
        DEGREE_TYPE = {"CE": ["Normal", "Poly", "ABP"],
               "CSC": ["Normal", "Poly", "ABP"],
               "DSAI": ["Normal"],
               "BCE": ["Normal"],
               "CEEcons": ["PI", "PA"],
               "BCG": ["Normal"],
               "CSEcons": ["PI", "PA"]}
        return DEGREE_TYPE
    def career_options(self):
        CAREER_OPTIONS = ["Blockchain Engineer", "DevOps Engineer", "Cloud Engineer/Architect", "Mixed/Virtual Reality Developer", "Cyber Security", "Software Engineer", "Full-stack Developer", "Front-End Engineer / Web Developer", "Backend Engineer", "Data Engineer", "Business Analyst", "Firmware Engineer", "Computer Hardware Engineer", "Embedded System Developer","AI Engineer", "Machine Learning Engineer", "Data Scientist", "Data Analyst", "AI Scientist", "System Architect", "Cybersecurity Consultant/Analyst", "Product Manager", "Entrepreneur", "Quantitative Analyst/Developer"]
        return CAREER_OPTIONS
    def year_standing_options(self):
        YEAR_STANDING = {0:"Prospective Student", 1:"Year 1", 2:"Year 2", 3:"Year 3", 4:"Year 4", 5:"Year 5"}
        return YEAR_STANDING
    def semester_options(self):
        SEMESTER = ["Semester 1", "Semester 2", "Not applicable"]
        return SEMESTER
    

