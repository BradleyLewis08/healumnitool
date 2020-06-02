from flask import Flask, request, render_template, session, redirect
import sys
import get_data

app = Flask(__name__)
app.secret_key = '\xfd{H\xe5<\x95\xf9\xe3\x96.5\xd1\x01O<!\xd5\xa2\xa0\x9fR"\xa1\xa8'


@app.route("/", methods=['GET'])
def home():
    return render_template("search.html", error="")

@app.route("/search", methods=['GET', 'POST'])
def search():
    if request.method == "POST":
        subjects = []
        subjects.append(request.form["subject_one"].lower())
        subjects.append(request.form["subject_two"].lower())
        subjects.append(request.form["subject_three"].lower())
        if request.form["subject_four"].lower() != "none":
            subjects.append(request.form["subject_four"].lower())
        # Removes all duplicates in the list and then checks if its the same length as the original list
        if len(list(dict.fromkeys(subjects))) != len(subjects):
            return render_template("search.html", error="Please select different subjects in each box.")
        exact_matches, close_matches = get_data.get_subject_matches(subjects)
        print(exact_matches)
        print(close_matches)
        session["exact_matches"] = exact_matches
        session["close_matches"] = close_matches
        return redirect("/results")

@app.route("/results", methods=['GET', 'POST'])
def results():
    if request.method == "GET":
        exact_match_count = len(session["exact_matches"])
        close_match_count = len(session["close_matches"])
        return render_template("results.html", exact_matches=session["exact_matches"], close_matches=session["close_matches"], exact_match_count=exact_match_count, close_match_count=close_match_count)

@app.route("/course", methods=['GET', 'POST'])
def course():
    if request.method == 'GET':
        return render_template("course.html")
    elif request.method == 'POST':
        course_name = request.form["course"]
        session["course_matches"] = get_data.get_course_matches(course_name)
        return redirect("/courseresults")

@app.route("/courseresults", methods=['GET', 'POST'])
def courseresults():
    if request.method == 'GET':
        return render_template("course_results.html", matches=session["course_matches"])
    

