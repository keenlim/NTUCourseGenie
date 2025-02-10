import json 

def convert_courses_to_dict(infile_path, outfile_path):
    # 1. Read the JSON file (list of dicts)
    with open(infile_path, 'r', encoding='utf-8') as infile:
        courses_list = json.load(infile)
    
    # 2. Convert list into dictionary keyed by "courseCode"
    courses_dict = {course["courseCode"]: course for course in courses_list}

    # 3. Write the new dictionary to another JSON file
    with open(outfile_path, 'w', encoding='utf-8') as outfile:
        json.dump(courses_dict, outfile, indent=2, ensure_ascii=False)

def convert_careers_to_dict(infile_path, outfile_path):
    # 1. Read the JSON file (list of dicts)
    with open(infile_path, 'r', encoding='utf-8') as infile:
        career_list = json.load(infile)
    
    # 2. Convert list into dictionary keyed by "career" title
    career_dict = {career["career"]: career for career in career_list}

    # 3. Write the new dictionary to another JSON file
    with open(outfile_path, 'w', encoding='utf-8') as outfile:
        json.dump(career_dict, outfile, indent=2, ensure_ascii=False)
    

if __name__ == "__main__":
    # convert_courses_to_dict("data/courses.json", "data/courses_by_code.json")
    convert_careers_to_dict("data/Careers.json", "data/Careers_with_key.json")