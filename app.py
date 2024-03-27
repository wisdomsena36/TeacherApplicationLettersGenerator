from flask import Flask, render_template, request, send_file, redirect, session, url_for, jsonify, abort
from pathlib import Path
from docxtpl import DocxTemplate
from datetime import datetime
from authlib.integrations.flask_client import OAuth
from authlib.common.security import generate_token
import os
import csv
from credentials import SECRET_KEY, GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET

app = Flask(__name__)
app.secret_key = SECRET_KEY

oauth = OAuth(app)


# Authorization required
def login_is_required(function):
    def wrapper(*args, **kwargs):
        if "user" not in session:
            return abort(401)
        else:
            return function()

    return wrapper


def save_to_csv(data):
    file_exists = os.path.isfile('csv_file/feedbacks.csv')
    with open('csv_file/feedbacks.csv', mode='a', newline='') as file:
        fieldnames = ['Name', 'Email', 'Rating', 'Opinion']
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        # Write header row if file is empty
        if not file_exists:
            writer.writeheader()

        writer.writerow({'Name': data[0], 'Email': data[1], 'Rating': data[2], 'Opinion': data[3]})


def save_report_to_csv(data):
    file_exists = os.path.isfile('csv_file/reports.csv')
    with open('csv_file/reports.csv', mode='a', newline='') as file:
        fieldnames = ['Name', 'Email', 'Report']
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        # Write header row if file is empty
        if not file_exists:
            writer.writeheader()

        writer.writerow({'Name': data[0], 'Email': data[1], 'Report': data[2]})


@app.route('/dashboard', endpoint='dashboard')
@login_is_required
def dashboard():
    return render_template('dashboard.html')


@app.route('/fillapplication', endpoint='fillapplication')
@login_is_required
def fillapplication():
    return render_template('fillapplicationmaternityleave.html')


@app.route('/fillapplicationupgrading', endpoint='fillapplicationupgrading')
@login_is_required
def fillapplication():
    return render_template('fillapplicationupgrading.html')


@app.route('/fillacceptanceofappointment', endpoint='fillacceptanceofappointment')
@login_is_required
def fill_acceptance_of_appointment():
    return render_template('fillacceptanceofappointment.html')


@app.route('/filltransferorreposting', endpoint='filltransferorreposting')
@login_is_required
def fill_transfer_or_reposting():
    return render_template('filltransferorreposting.html')


@app.route('/fillreleasetransfer', endpoint='fillreleasetransfer')
@login_is_required
def fill_release_transfer():
    return render_template('fillreleasetransfer.html')


@app.route('/fillsalaryreactivation', endpoint='fillsalaryreactivation')
@login_is_required
def fill_salary_reactivation():
    return render_template('fillsalaryreactivation.html')


@app.route('/feedbackform', endpoint='feedbackform')
@login_is_required
def fill_feedback_form():
    return render_template('feedbackform.html')


@app.route('/reportform', endpoint='reportform')
@login_is_required
def fill_report_form():
    return render_template('reportform.html')


@app.route('/')
def login():
    return render_template('login.html')


@app.route('/submit_feedback', methods=['POST'], endpoint='submit_feedback')
@login_is_required
def submit_feedback():
    name = request.form['name']
    email = request.form['email']
    rating = request.form['rating']
    opinion = request.form['opinion']

    feedback_data = [name, email, rating, opinion]

    try:
        save_to_csv(feedback_data)
        return jsonify({"message": "Feedback submitted successfully!"}), 200
    except Exception as e:
        return str(e), 500


@app.route('/submit_report', methods=['POST'], endpoint='submit_report')
@login_is_required
def submit_report():
    name = request.form['name']
    email = request.form['email']
    report = request.form['report']

    feedback_data = [name, email, report]

    try:
        save_report_to_csv(feedback_data)
        return jsonify({"message": "Report submitted successfully!"}), 200
    except Exception as e:
        return str(e), 500


@app.route('/google/')
def google():
    CONF_URL = 'https://accounts.google.com/.well-known/openid-configuration'
    oauth.register(
        name='google',
        client_id=GOOGLE_CLIENT_ID,
        client_secret=GOOGLE_CLIENT_SECRET,
        server_metadata_url=CONF_URL,
        client_kwargs={
            'scope': 'openid email profile'
        }
    )

    # Redirect to google_auth function
    redirect_uri = url_for('google_auth', _external=True)
    print(redirect_uri)
    session['nonce'] = generate_token()
    return oauth.google.authorize_redirect(redirect_uri, nonce=session['nonce'])


@app.route('/logout')
def logout():
    session.pop('google_token', None)
    session.clear()
    return redirect(url_for('login'))


@app.route('/google/auth/')
def google_auth():
    try:
        token = oauth.google.authorize_access_token()
        user = oauth.google.parse_id_token(token, nonce=session['nonce'])
        session['user'] = user
        print(" Google User ", user)
        return redirect('/dashboard')
    except KeyError:
        # Handle KeyError if 'nonce' is not found in the session
        abort(400, "Invalid request: 'nonce' not found in session.")
    except Exception as e:
        # Handle other exceptions
        print("An error occurred during Google authentication:", e)
        abort(500, "An error occurred during Google authentication.")


@app.route('/download_maternity_leave', methods=['POST', 'GET'], endpoint='download_maternity_leave')
@login_is_required
def download_file_for_maternity_leave():
    if request.method == 'POST':
        # Handle POST request
        name = request.form.get('name')
        staff_id = request.form.get('staffid')
        phone = request.form.get('phone')
        registered_no = request.form.get('registeredno')
        school = request.form.get('school')
        address = request.form.get('address')
        district_town = request.form.get('district_town')
        address_town = request.form.get('address_town')
        district = request.form.get('district')
        date_on_letter = request.form.get('date_on_letter')

        # Parse the original date string
        original_date = datetime.strptime(date_on_letter, "%Y-%m-%d")

        # Format the date to the desired format
        formatted_date_str = original_date.strftime("%B %d, %Y")

        # Generate the document using the form data
        template_path = Path(__file__).parent / "letter_templates/maternity_leave.docx"
        doc = DocxTemplate(template_path)
        context = {
            "NAME": name.upper(),
            "SCHOOLNAME": school,
            "ADDRESS": address,
            "ADDRESSTOWN": address_town.upper(),
            "TOWN": district_town.upper(),
            "STAFFED": staff_id,
            "REGISTERNO": registered_no,
            "PHONE": f"({phone})",
            "DATEONLETTER": formatted_date_str.upper(),
            "DISTRICT": district.upper()  # Assuming you have a field named 'district' in your form
        }

        file_name = name + " Maternity Leave Application Letter.docx"
        file_name = "generated_letters/" + file_name

        doc.render(context)
        doc.save(Path(__file__).parent / file_name)

        # Return the generated document for download
        return send_file(Path(__file__).parent / file_name, as_attachment=True)

    elif request.method == 'GET':
        # Handle GET request (optional)
        # You may want to render a different template or provide some other response for GET requests to /download
        return "GET method not supported"

    else:
        # Handle other request methods (optional)
        return "Method not allowed"


@app.route('/download_upgrading', methods=['POST', 'GET'], endpoint='download_download_upgrading')
@login_is_required
def download_file_for_upgrading():
    if request.method == 'POST':
        # Handle POST request
        name = request.form.get('name')
        staff_id = request.form.get('staffid')
        phone = request.form.get('phone')
        registered_no = request.form.get('registeredno')
        school = request.form.get('school')
        address = request.form.get('address')
        district_town = request.form.get('district_town')
        address_town = request.form.get('address_town')
        district = request.form.get('district')
        date_on_letter = request.form.get('date_on_letter')
        years_in_service = request.form.get('years_in_service')
        program = request.form.get('program')
        years_completed = request.form.get('years_completed')
        current_rank = request.form.get('current_rank')
        next_rank = request.form.get('next_rank')

        # Parse the original date string
        original_date = datetime.strptime(date_on_letter, "%Y-%m-%d")

        # Format the date to the desired format
        formatted_date_str = original_date.strftime("%B %d, %Y")

        # Generate the document using the form data
        template_path = Path(__file__).parent / "letter_templates/upgrading.docx"
        doc = DocxTemplate(template_path)
        context = {
            "NAME": name.upper(),
            "SCHOOLNAME": school,
            "ADDRESS": address,
            "ADDRESSTOWN": address_town.upper(),
            "TOWN": district_town.upper(),
            "STAFFED": staff_id,
            "REGISTERNO": registered_no,
            "PHONE": f"({phone})",
            "DATEONLETTER": formatted_date_str.upper(),
            "DISTRICT": district.upper(),
            "NUMBEROFYEARSINSERVICE": years_in_service,
            "NAMEOFPROGRAM": program.title(),
            "YEARCOMPLETED": years_completed,
            "CURRENTRANK": current_rank,
            "NEXTRANK": next_rank,
            "NEXTRANKTITLE": next_rank.upper()
        }

        file_name = name + " Upgrading Application Letter.docx"
        file_name = "generated_letters/" + file_name

        doc.render(context)
        doc.save(Path(__file__).parent / file_name)

        # Return the generated document for download
        return send_file(Path(__file__).parent / file_name, as_attachment=True)

    elif request.method == 'GET':
        # Handle GET request (optional)
        # You may want to render a different template or
        # provide some other response for GET requests to /download
        return "GET method not supported"

    else:
        # Handle other request methods (optional)
        return "Method not allowed"


@app.route('/download_acceptance_of_appointment', methods=['POST', 'GET'],
           endpoint='download_acceptance_of_appointment')
@login_is_required
def download_file_acceptance_of_appointment():
    if request.method == 'POST':
        name = request.form.get('name')
        reference = request.form.get('reference')
        phone = request.form.get('phone')
        school = request.form.get('school')
        address = request.form.get('address')
        region_town = request.form.get('region_town')
        address_town = request.form.get('address_town')
        region = request.form.get('region')
        date_on_letter = request.form.get('date_on_letter')
        date_on_appointment_letter = request.form.get('date_on_appointment_letter')

        # Parse the original date string
        original_date = datetime.strptime(date_on_letter, "%Y-%m-%d")

        # Format the date to the desired format
        formatted_date_str = original_date.strftime("%B %d, %Y")

        # Parse the original date string
        date_on_appointment_letter_original_date = datetime.strptime(date_on_appointment_letter, "%Y-%m-%d")

        # Format the date to the desired format
        date_on_appointment_letter_formatted_date_str = date_on_appointment_letter_original_date.strftime("%B %d, %Y")

        # Generate the document using the form data
        template_path = Path(__file__).parent / "letter_templates/acceptance_of_appointment.docx"
        doc = DocxTemplate(template_path)
        context = {
            "NAME": name.upper(),
            "SCHOOLNAME": school,
            "ADDRESS": address,
            "ADDRESSTOWN": address_town.upper(),
            "TOWN": region_town.upper(),
            "REFERENCEAPPOINTMENTLETTER": reference,
            "DATEONTHEAPPOINTMENTLETTER": date_on_appointment_letter_formatted_date_str,
            "PHONE": f"({phone})",
            "DATEONLETTER": formatted_date_str.upper(),
            "REGION": region.upper(),
        }

        file_name = name + " Acceptance of Appointment Application Letter.docx"
        file_name = "generated_letters/" + file_name

        doc.render(context)
        doc.save(Path(__file__).parent / file_name)

        # Return the generated document for download
        return send_file(Path(__file__).parent / file_name, as_attachment=True)

    elif request.method == 'GET':
        # Handle GET request (optional)
        # You may want to render a different template or provide some other response for GET requests to /download
        return "GET method not supported"

    else:
        # Handle other request methods (optional)
        return "Method not allowed"


@app.route('/download_transfer_or_reposting', methods=['POST', 'GET'], endpoint='download_transfer_or_reposting')
@login_is_required
def download_transfer_or_reposting():
    if request.method == 'POST':
        name = request.form.get('name')
        staff_id = request.form.get('staffid')
        phone = request.form.get('phone')
        registered_no = request.form.get('registeredno')
        school = request.form.get('school')
        address = request.form.get('address')
        district_town = request.form.get('district_town')
        address_town = request.form.get('address_town')
        district = request.form.get('district')
        date_on_letter = request.form.get('date_on_letter')
        years_in_school = request.form.get('years_in_school')
        reason = request.form.get('reason')
        new_school = request.form.get('new_school')

        # Parse the original date string
        original_date = datetime.strptime(date_on_letter, "%Y-%m-%d")

        # Format the date to the desired format
        formatted_date_str = original_date.strftime("%B %d, %Y")

        # Generate the document using the form data
        template_path = Path(__file__).parent / "letter_templates/reposting.docx"
        doc = DocxTemplate(template_path)
        context = {
            "NAME": name.upper(),
            "SCHOOLNAME": school,
            "ADDRESS": address,
            "ADDRESSTOWN": address_town.upper(),
            "TOWN": district_town.upper(),
            "STAFFED": staff_id,
            "REGISTERNO": registered_no,
            "PHONE": f"({phone})",
            "DATEONLETTER": formatted_date_str.upper(),
            "DISTRICT": district.upper(),
            "NUMBEROFYEARSSERVED": years_in_school,
            "NEWSCHOOLNAME": new_school.title(),
            "REASON": reason.lower()
        }

        file_name = name + " Reposting Application Letter.docx"
        file_name = "generated_letters/" + file_name

        doc.render(context)
        doc.save(Path(__file__).parent / file_name)

        # Return the generated document for download
        return send_file(Path(__file__).parent / file_name, as_attachment=True)

    elif request.method == 'GET':
        # Handle GET request (optional)
        # You may want to render a different template or provide some other response for GET requests to /download
        return "GET method not supported"

    else:
        # Handle other request methods (optional)
        return "Method not allowed"


@app.route('/download_release_transfer', methods=['POST', 'GET'], endpoint='download_release_transfer')
@login_is_required
def download_release_transfer():
    if request.method == 'POST':
        name = request.form.get('name')
        staff_id = request.form.get('staffid')
        phone = request.form.get('phone')
        registered_no = request.form.get('registeredno')
        school = request.form.get('school')
        address = request.form.get('address')
        district_town = request.form.get('district_town')
        address_town = request.form.get('address_town')
        district = request.form.get('district')
        date_on_letter = request.form.get('date_on_letter')
        years_in_school = request.form.get('years_in_school')
        reason = request.form.get('reason')
        new_dist_reg = request.form.get('new_dist_reg')
        curr_dist_reg = request.form.get('curr_dist_reg')
        level_of_transfer = request.form.get('level_of_transfer')

        # Parse the original date string
        original_date = datetime.strptime(date_on_letter, "%Y-%m-%d")

        # Format the date to the desired format
        formatted_date_str = original_date.strftime("%B %d, %Y")

        # Generate the document using the form data
        template_path = Path(__file__).parent / "letter_templates/releasetransfer.docx"
        doc = DocxTemplate(template_path)
        context = {
            "NAME": name.upper(),
            "SCHOOLNAME": school,
            "ADDRESS": address,
            "ADDRESSTOWN": address_town.upper(),
            "TOWN": district_town.upper(),
            "STAFFED": staff_id,
            "REGISTERNO": registered_no,
            "PHONE": f"({phone})",
            "DATEONLETTER": formatted_date_str.upper(),
            "DISTRICT": district.upper(),
            "NUMBEROFYEARSSERVED": years_in_school,
            "NEWDISTORREG": new_dist_reg.title(),
            "CURRENTDISTORREG": curr_dist_reg.title(),
            "LEVELOFTRANSFER": level_of_transfer.title(),
            "REASON": reason.lower()
        }

        file_name = name + " Transfer Application Letter.docx"
        file_name = "generated_letters/" + file_name

        doc.render(context)
        doc.save(Path(__file__).parent / file_name)

        # Return the generated document for download
        return send_file(Path(__file__).parent / file_name, as_attachment=True)

    elif request.method == 'GET':
        # Handle GET request (optional)
        # You may want to render a different template or provide some other response for GET requests to /download
        return "GET method not supported"

    else:
        # Handle other request methods (optional)
        return "Method not allowed"


@app.route('/download_salary_reactivation', methods=['POST', 'GET'], endpoint='download_salary_reactivation')
@login_is_required
def download_salary_reactivation():
    if request.method == 'POST':
        name = request.form.get('name')
        staff_id = request.form.get('staffid')
        phone = request.form.get('phone')
        registered_no = request.form.get('registeredno')
        school = request.form.get('school')
        address = request.form.get('address')
        district_town = request.form.get('district_town')
        address_town = request.form.get('address_town')
        district = request.form.get('district')
        date_on_letter = request.form.get('date_on_letter')
        month_or_s = request.form.get('month_or_s')
        circuit = request.form.get('circuit')

        # Parse the original date string
        original_date = datetime.strptime(date_on_letter, "%Y-%m-%d")

        # Format the date to the desired format
        formatted_date_str = original_date.strftime("%B %d, %Y")

        # Generate the document using the form data
        template_path = Path(__file__).parent / "letter_templates/salary_reactivation.docx"
        doc = DocxTemplate(template_path)
        context = {
            "NAME": name.upper(),
            "SCHOOLNAME": school,
            "ADDRESS": address,
            "ADDRESSTOWN": address_town.upper(),
            "TOWN": district_town.upper(),
            "STAFFED": staff_id,
            "REGISTERNO": registered_no,
            "PHONE": f"({phone})",
            "DATEONLETTER": formatted_date_str.upper(),
            "DISTRICT": district.upper(),
            "YOURDISTRICT": district.title(),
            "MONTHORS": month_or_s,
            "CIRCUITNAME": circuit.title()
        }

        file_name = name + " Salary Re-Activation Application Letter.docx"
        file_name = "generated_letters/" + file_name

        doc.render(context)
        doc.save(Path(__file__).parent / file_name)

        # Return the generated document for download
        return send_file(Path(__file__).parent / file_name, as_attachment=True)

    elif request.method == 'GET':
        # Handle GET request (optional)
        # You may want to render a different template or provide some other response for GET requests to /download
        return "GET method not supported"

    else:
        # Handle other request methods (optional)
        return "Method not allowed"


if __name__ == '__main__':
    app.run(port=5000, debug=True)
