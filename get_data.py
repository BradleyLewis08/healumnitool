import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pprint import pprint

scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("hetool-eea73f187bd7.json", scope)
 
client = gspread.authorize(creds)

def retrieve_data():
    sheet = client.open("A Level and Uni data").sheet1
    data = sheet.get_all_records()
    return data

def get_subject_matches(subjects):
    # Gets the data from Google Sheet
    data = retrieve_data()
    exact_matches = []
    close_matches = []
    # Iteration through data from GSheet
    for item in data:
        # Tracks if there is a different subject. Will only be used if there is one different subject
        different_subject = ""
        matches = 0
        alumni_subjects = []
        if item["Subject 1"].lower() in subjects:
            matches += 1
        else:
            different_subject = item["Subject 1"]
            different_index = 0
        alumni_subjects.append(item["Subject 1"])
        if item["Subject 2"].lower() in subjects:
            matches += 1
        else:
            different_subject = item["Subject 2"]
            different_index = 1
        alumni_subjects.append(item["Subject 2"])
        if item["Subject 3"].lower() in subjects:
            matches += 1
        else:
            different_subject = item["Subject 3"]
            different_index = 2
        alumni_subjects.append(item["Subject 3"])
        # If user has entered 4 subjects
        if len(subjects) > 3 and item["Subject 4"] != '':
            if item["Subject 4"] in  subjects: 
                matches += 1
            else:
                different_subject = item["Subject 4"]
                different_index = 3
            alumni_subjects.append(item["Subject 4"])
        elif len(subjects) == 3 and item["Subject 4"] != '':
            different_subject = item["Subject 4"]
            different_index = 3
            alumni_subjects.append(item["Subject 4"])
        if matches == len(alumni_subjects):

            exact_matches.append({"Course":item["Course"], "University":item["Final University Destination"]})
        elif matches == len(alumni_subjects) - 1:
            if item['EPQ'] == "Yes":
                alumni_subjects.append('EPQ')
            close_matches.append({"Course": item["Course"], "University": item["Final University Destination"], "Subjects": alumni_subjects, "Index": different_index})
    return exact_matches, close_matches 


def make_subject_list(item):
    subjects = []
    for i in range(1,5):
        index = "Subject" + " " + str(i)
        if item[index] != "":
            subjects.append(item[index])
    return subjects

def get_course_matches(course):
    data = retrieve_data()
    match_data = []
    for item in data:
        if course.lower() in item["Course"].lower() and item["Course"] != "":
            subjects = make_subject_list(item)
            match_data.append({"Subjects": subjects, "University": item["Final University Destination"], "Course": item["Course"]})
    return match_data

print(get_course_matches("History"))