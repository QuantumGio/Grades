'''Server in python using flask'''
import json
from flask import Flask, render_template, request, jsonify, url_for, abort # module for the local server
import database


app = Flask(__name__,template_folder="../templates", static_folder="../static") # setting the server files


@app.errorhandler(404)
def return_404(error):
    return 'subject not found', 404


@app.route("/editGrade", methods=['POST'])
def edit_grade():
    grade_data = request.get_json()
    edit_status = database.edit_grade(grade_data)
    if edit_status:
        return jsonify({'ok': True, 'message': 'grade modified'})
    else:
        return jsonify({'ok': False, 'message': 'grade not modified, try again'})

@app.route("/<subject>", methods=['GET', 'POST'])
def return_subject_page(subject):
    if request.method == "POST":
        gradeData = request.get_json()
        code = gradeData.get('code')
        if code == '002':
            response = database.add_grade(grade=gradeData['grade'], subject_name=gradeData['subject'], date=gradeData['date'],weight=gradeData['grade_weight'], type_=gradeData['type'])
            if response:
                return jsonify({'ok':True, 'message': 'grade added successfully'}), 200
            else:
                return jsonify({'ok':False, 'message': 'error while adding a grade'}), 400
        if code == '004':
            response = database.delete_grade(id_=gradeData['id'])
            if response:
                return jsonify({'ok':True, 'message': 'grade deleted successfully'}), 201
            else:
                return jsonify({'ok':False, 'message': 'error while deleting a grade'}), 400
    
    if subject in database.list_subjects():
        return render_template("subject.html", subject=subject, grades=database.list_grades(subject), average=database.return_average(subject))
    else:
        abort(404)


@app.route("/", methods=["GET", "POST"])
def return_index():
    if request.method == "POST":
        subject: json = request.get_json()
        code = subject.get('code')
        if code and code == '001':
            response = database.add_subject(subject['subject'])
            if response is True:
                return jsonify({'ok':True, 'message': 'subject added successfully'}), 201
            elif response == "duplicate subject" :
                return jsonify({'ok':False, 'message': 'the subject already exists'}), 400
            else:
                return jsonify({'ok':False, 'message': 'errors while adding a subject'}), 400
        else:
            subject_redirect = subject['subject_redirect']
            return jsonify({'redirect': url_for('return_subject_page', subject=subject_redirect)}), 200
    
    return render_template("index.html", grade_bar=json.dumps(database.return_grade_proportions()), averages_list=database.return_averages(), subjects_list = database.list_subjects(), general_average=database.return_general_average())


@app.route("/getAverageByDate", methods=['GET'])
def get_average_by_date():
    data = database.return_average_by_date()
    return jsonify(data), 200


if __name__ == "__main__":
    app.run(debug=False)
