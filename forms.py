from flask.ext.wtf import Form
from wtforms import (StringField, PasswordField, TextAreaField, DecimalField,
        RadioField, SelectMultipleField, widgets, FileField, validators, IntegerField)
from wtforms.validators import (DataRequired, Regexp, ValidationError, Email, Length, EqualTo)




from models import User


def name_exists(form,field):
    if User.select().where(User.username == form.data).exists():
        raise ValidationError('User with that username already exists!')

def email_exists(form, field):
    if User.select().where(User.email == form.data).exists():
        # TODO: CHECK THIS METHOD
        raise ValidationError('User with that email already exists')

def above_reasonable_price(form, field):
    if form.data >= 100:
        raise ValidationError("You need to ask for a reasonable price")


# def validates_box_selection():



# class SimpleForm(Form):
#     string_of_files = ['one\r\ntwo\r\nthree\r\n']
#     list_of_files = string_of_files[0].split()
#     # create a list of value/description tuples
#     files = [(x, x) for x in list_of_files]
#     example = MultiCheckboxField('Label', choices=files)
#


# class MultiCheckboxField(SelectMultipleField):
#     widget = widgets.ListWidget(prefix_label=False)
#     option_widget = widgets.CheckboxInput()
#
#





class RevisedRegisterForm(Form):

    username = StringField('Username', validators=
                [DataRequired(), Regexp(r'^[a-zA-Z0-9_]+$', message=(
                                            'Username should be one word, letters, numbers and underscores only!')),
                                            name_exists])


    firstname = StringField('First Name', validators=
                [DataRequired(), Regexp(r'^[A-Z][a-z_]*$', message=(
                                            'Please capitalize the first letter'))])
    lastname = StringField('Last Name', validators=
                [DataRequired(), Regexp(r'^[A-Z][a-z_]*$', message=(
                                            'Please capitalize the first letter'))])
    email = StringField('Email', validators=[DataRequired(), Email(), email_exists])

    password = PasswordField('Password', validators=[DataRequired(), Length(min=5),
    EqualTo('password_confirm', message="Passwords must match")])

    password_confirm = PasswordField('Confirm Password', validators=[DataRequired()])




class LoginForm(Form):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])


class BuyForm(Form):
    cubic_feet = DecimalField('How many cubic feet do you need?',validators=[DataRequired()],places=2,rounding=None)
    bid = DecimalField('How much are you willing to spend?',validators=[DataRequired()],places=2,rounding=None)
    # should i ask how much total spend or per feet^3
    specs = StringField("Anything else you'd like to add?", validators=[DataRequired()])

class SellForm(Form):
    cubic_feet = DecimalField('How many cubic feet do you have available?',validators=[DataRequired()],places=2,rounding=None)
    ask = DecimalField('How much are you looking to make ft^3 per month??',validators=[DataRequired()],places=2,rounding=None)
    # should i ask how much total they want or per feet^3
    specs = StringField("Anything else you'd like to add about your space?", validators=[DataRequired()])

class SearchMarketPlace(Form):
    query_string = StringField("Search our storage universe", validators=[DataRequired()])
                                                            #DataRequired for a search for that'll be on the page??


class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()




class NumBoxesPerSelection(Form):

    #one per box max field length is 2 and they have to be intergers

    smll = IntegerField("Num Smalls", validators=[], default=0)
    med = IntegerField("Num Mediums", validators=[], default=0)
    lrg = IntegerField("Num Larges", validators=[], default=0)
    Xlrg = IntegerField("Num Extra Larges", validators=[], default=0)

    # class KwargsInSelection(Form):
    #     scl = MultiCheckboxField(contianers= list_containers):



class RevisedBuyForm(Form):
    # cubic_feet =
    #I dont think bid ask is usful anymore
    def get_choices():
        array_of_containers = ['Small\r\nMedium\r\nLarge\r\nXLarge\r\n']
        list_containers = array_of_containers[0].split()
        choice_tuples = [(x,x) for x in list_containers]
        return choice_tuples



    container_choice = MultiCheckboxField('Pick Your Container(s)!', choices = get_choices())

    duration = RadioField("How long do you need to store everything?",
                            validators = [DataRequired()], choices = [("1 Weeks", "1 Week"),
                                                                    ("1 Month", "1 Month"),
                                                                    ("2 Months", "2 Weeks"),
                                                                    ("3 Months", "3 Months"),
                                                                    ("6 Months", "6 Months"),
                                                                    ("1 Year", "1 Year")])

    #optional
    specs = StringField("Anything else you'd like to add? Ex. Dry, Need to belongings it more than normal",
                    validators=[])




class RevisedSellForm(Form):
    cubic_feet_avail = MultiCheckboxField("Cubic feet available", choices= [(10, "10 cubic feet"),(50, "50 cubic feet"), 100, "100 cubic feet"]) # how many units can you store?
    # image_of_space = FileField("Image of your space",  [validators.regexp(r'^[^/\\]\.jpg$')] , description=u"Field where users can upload pics of their space", id="fileUploader")
    duration = RadioField("How Long can you store stuff for?",
                        validators = [DataRequired()], choices = [("1 Week", "1 Week"),
                                                                ("1 Month", "1 Month"),
                                                                ("2 Months", "2 Weeks"),
                                                                ("3 Months", "3 Months"),
                                                                ("6 Months", "1 Week")])
    def validate_image(form,field):
        if field.data:
            field.data = re.sub(r'[^a-z0-9_.-]' , '_', field.data)

    def upload(request):
        form = UploadForm(request.POST)
        if form.image_of_space.data:
            imamge_data = request.FILES[form.image_of_space.name].read()
            open(os.path.join('/handle_image_real_quick', form.image_of_space.data),'w').write(imamge_data)
