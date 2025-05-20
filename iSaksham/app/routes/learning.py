from flask import flash, render_template, request
from flask_smorest import Blueprint
from flask_login import login_required
from iSaksham.app.models.chapters import Chapters
from iSaksham.app.models.modules import Modules

from iSaksham.app.models.feedback import Feedback  # Importing login_required decorator

blp = Blueprint("learning","learning","Routes to LMS")


# Route for the home page
@blp.route('/')
@blp.route('/home')
def home():
    return render_template('home.html')  # Rendering home.html template

# Route for the FAQ page, accessible only to logged-in users
@blp.route('/faq')
# @login_required
def faq():
    return render_template('faq.html')  # Rendering faq.html template

# Route for the user manual page, accessible only to logged-in users
@blp.route('/user_manual')
# @login_required
def user_manual():
    return render_template('user_manual.html')  # Rendering user_manual.html template

# Route for the contact page
@blp.route('/contact')
def contact():
    return render_template('contact.html')  # Rendering contact.html template

# Route for the important links page
@blp.route('/important_links')
def important_links():
    return render_template('important_links.html')  # Rendering important_links.html template

# Route for the credits page
@blp.route('/credits')
def credits():
    return render_template('credits.html')  # Rendering credits.html template

@blp.route('/course_2018')
def course_2018():
    modules = Modules.get_all()
    chapters = Chapters.get_all()
    
    accordion_title = []
    accordion_content = []
    
    for module in modules:
        content = []
        accordion_title.append({"id":module.id,"name":module.name})
        for chapter in chapters:
            if module.id == chapter.module_id:
                json = {"id":chapter.id,"module_id": chapter.module_id,"link": chapter.link,"length":chapter.length, "title":chapter.title}
                content.append(json)
        accordion_content.append(content)
        
    
    return render_template('course_2018.html',accordion_content = accordion_content,accordion_title= accordion_title)

# Route for the course page, accessible only to logged-in users
@blp.route('/course_2024')
# @login_required
def course_2024():
    
    return render_template('course_2024.html')  # Rendering course.html template

@login_required
@blp.route('/play_chapter/<int:id>')
def play_chapter(id):
    modules = Modules.get_all()
    chapters = Chapters.get_all()
    accordion_title = []
    accordion_content = []
    
    for module in modules:
        content = []
        accordion_title.append({"id":module.id,"name":module.name})
        for chapter in chapters:
            if module.id == chapter.module_id:
                json = {"id":chapter.id,"module_id": chapter.module_id,"link": chapter.link,"length":chapter.length, "title":chapter.title}
                content.append(json)
        accordion_content.append(content)
        
    chapter_db = Chapters.get_chapters_by_id(id)
    if chapter_db['link']:
        iframe = True
    else:
        iframe = False
        
    next_chapter = Chapters.get_chapters_by_id(id+1)
    if id != 0:
        previous_chapter=Chapters.get_chapters_by_id(id-1)
    else:
        previous_chapter = 0
    return render_template('play_chapter.html',iframe=iframe,accordion_content = accordion_content,accordion_title= accordion_title,chapter_db=chapter_db,next_chapter=next_chapter,previous_chapter=previous_chapter)

# Route for the feedback submission page
@blp.route('/feedback', methods=['POST', 'GET'])
def feedback():
    if request.method == "POST":
        # Extracting form data
        name = request.form.get('name')
        email = request.form.get('email')
        subject = request.form.get('subject')
        message_category = request.form.get('message_type')
        rating = request.form.get('rating')
        if not rating:
            rating = request.form.get('rating-mobile')
        message = request.form.get('message')
        
        # Creating Feedback object and saving to database
        feedback = Feedback(name, email, subject, message_category, message, rating)
        feedback.save_to_db()

        flash("Thank You for sharing your feedback")  # Flashing a message to indicate successful feedback submission
        return render_template('feedback.html')  # Rendering feedback.html template
    return render_template('feedback.html')  # Rendering feedback.html template for GET requests
