import os
from werkzeug.utils import secure_filename
from flask import Flask, request, redirect, url_for, render_template, flash, send_from_directory, session
from llm_workflow.llm_tasks import Tasks

# Line Formatter
def line_formatter():
    print("-"*100)

app = Flask(__name__)
app.secret_key = "supersecretkey"
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['ALLOWED_EXTENSIONS'] = {'txt', 'png', 'jpg', 'jpeg', 'gif'}

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def upload_form():
    profile_photo = None
    if 'profile_photo' in request.cookies:
        profile_photo = request.cookies.get('profile_photo')
    return render_template('upload.html', profile_photo=profile_photo)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    if file and allowed_file(file.filename) and file.filename.rsplit('.', 1)[1].lower() == 'txt':
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        return redirect(url_for('process_file', filename=filename))
    else:
        flash('Allowed file types are txt')
        return redirect(request.url)

@app.route('/upload_profile', methods=['POST'])
def upload_profile():
    if 'profile_photo' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['profile_photo']
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    if file and allowed_file(file.filename) and file.filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        resp = redirect(url_for('upload_form'))
        resp.set_cookie('profile_photo', filename)
        return resp
    else:
        flash('Allowed file types are png, jpg, jpeg, gif')
        return redirect(request.url)

@app.route('/process/<filename>', methods=['GET', 'POST'])
def process_file(filename: str):
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    with open(filepath, 'r') as file:
        file_content = file.read()

    # # Update the session with the entities needed for LLM Task class
    # session['file_name'] = filename
    # session['file_content'] = file_content

    # Instantiate the Task class
    llm_task = Tasks(file_name=filename, file_text=file_content, port=8451, grpc_port=50053)

    if request.method == 'POST':
        option = request.form.get('option')
        if option == 'summary':
            result = summarize_text(llm_task, file_content)
            return render_template('summary_result.html', result=result, option=option.capitalize(), filename=filename.capitalize())
        elif option == 'entities':
            result = extract_entities(llm_task, file_content)
            return render_template('extraction_result.html', result=result, option=option.capitalize(), filename=filename.capitalize())
        elif option == 'qa':
            return redirect(url_for('qa_view', filename=filename))
        else:
            result = "Invalid option selected"

    return render_template('process.html', filename=filename)

@app.route('/qa/<filename>', methods=['GET', 'POST'])
def qa_view(filename):
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    with open(filepath, 'r') as file:
        file_content = file.read()
    # # Retrieve the file name and content from the process view
    # file_name = session.get('file_name')
    # file_content = session.get('file_content')
    
    if request.method == 'POST':
        # Retrieve the user input from question
        question = request.form.get('question')
        
        line_formatter()

        print(filename)
        print(file_content)

        line_formatter()
        # Instantiate the Task class
        llm_task = Tasks(file_name=filename, file_text=file_content, port=8451, grpc_port=50053)

        # Perform vector retrieval with LLMChain to Generate the Answer
        answer = question_answer(llm_task=llm_task, query=question)

        return render_template('qa_result.html', question=question, answer=answer, filename=filename)

    return render_template('qa_result.html', filename=filename)

def summarize_text(llm_task: Tasks, text: str):
    # Get the result
    result = llm_task.retrieve_summary(text=text)

    # Postprocess the result
    result = {k.capitalize().replace("_", " ") : v for k,v in result.items()}

    # Dummy summarization function
    return result

def extract_entities(llm_task: Tasks, text: str):
    # Get the result
    result = llm_task.extract_entities(text=text)
    # Dummy entity extraction function
    return result

def question_answer(llm_task: Tasks, query: str):
    # Run the method
    result = llm_task.question_answer(query=query)

    return result

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8900, debug=True)