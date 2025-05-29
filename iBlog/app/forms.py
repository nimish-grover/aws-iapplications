from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length, Optional
from app.models import Category, Tag

class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(min=3, max=255)])
    slug = StringField('Slug', validators=[DataRequired(), Length(min=3, max=255)])
    excerpt = TextAreaField('Excerpt', validators=[Optional(), Length(max=500)])
    content = TextAreaField('Content', validators=[DataRequired()])
    status = SelectField('Status', choices=[
        ('draft', 'Draft'), 
        ('published', 'Published'),
        ('private', 'Private')
    ], validators=[DataRequired()])
    featured_image_url = StringField('Featured Image URL', validators=[Optional(), Length(max=255)])
    meta_title = StringField('Meta Title', validators=[Optional(), Length(max=255)])
    meta_description = TextAreaField('Meta Description', validators=[Optional()])
    submit = SubmitField('Save Post')