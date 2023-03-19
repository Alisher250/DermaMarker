from flask import request

from flask import Flask
from flask import render_template
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
import os
from werkzeug.utils import secure_filename
from wtforms.validators import InputRequired
import openai

from findPhotos import execute  # I was created by Amir :D


app = Flask(__name__)

class UploadFileForm(FlaskForm):
    file = FileField("File", validators=[InputRequired()])
    submit = SubmitField("Upload File")

app.config['SECRET_KEY'] = os.urandom(12)
app.config['UPLOAD_FOLDER'] = 'static/files'


@app.route("/index")
@app.route("/")
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contacts')
def feedback():
    return render_template('contact.html')

'''@app.route('/Services.html', methods=['GET', 'POST'])
def services():
    form = UploadFileForm()
    if form.validate_on_submit():
        file = form.file.data
        file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER'],secure_filename(file.filename)))
        return "the file has been uploaded successfully"
    return render_template('Services.html', form=form, x=execute())'''

@app.route('/scanner', methods=['GET', 'POST'])
def causes():
    form = UploadFileForm()
    x=[]
    x1 = ''
    x2 = ''
    openai.api_key = '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'
    if request.method == "POST":
        file = form.file.data
        file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER'],secure_filename(file.filename)))
        x = execute()
        x1 = 'On the pictures you can see:' \
             '1 - ' + x[0][0], '2 - ' + x[0][1], '3 - ' + x[0][2], '4 - ' + x[0][3], '5 - ' + x[0][4]


        prompt = f'Act like a Dermamarker, which is ai that detects and explains, recommends how to treat skin disease. Firstly, Interpret what is the possibility of skin diseases of the person(client) according to list below. Then recommend what to do. Dont sфн that it is a provided list. Say like you did this analysis. Be confident, and say everything like you did it all. Exactly say statistics to make sure client understands. Dont recommend dermatologist. Explain what is it and what to do in 500 words minimum. Write in a structred, specific way [{x[3]}]'
        # completion = openai.ChatCompletion.create(
        #     model = 'gpt-3.5-turbo',
        #     messages = [
        #         {'role': 'user', 'content': prompt}
        #     ]
        # )
        # x2 = completion.choices[0].message.content
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=1024,
            stop=None,
            temperature=0.5,
        )
        x2 = response.choices[0].text.strip()

    return render_template('causes.html', form=form, x=x, x1=x1, x2=x2)
# https://www.google.kz/search?q=2DnHWraKtR4v5vUzBbSy0FHEN23_5KfXy9zkA83dL9UpPgzFA&ie=UTF-8&oe=UTF-8&hl=en-kz&client=safari


if __name__ == '__main__':
    app.run()