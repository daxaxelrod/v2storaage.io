
from flask import Flask, g, render_template, flash, redirect, url_for, jsonify, request
from flask.ext.bcrypt import check_password_hash
from flask.ext.login import (LoginManager, login_user, logout_user, login_required, current_user)
from token2 import generate_confirmation_token, confirm_token
import stripe
#import re
import datetime
import os
from email_storaage import *
from flask.ext.mail import Mail



import models
import forms

DEBUG = True
PORT = 8000
HOST = '0.0.0.0'


stripe_keys = {
    'secret_key' : "sk_test_lFWKYrEKbzeotkeAoV5pm2lc",
    'publishable_key' : "pk_test_1fRtlKp9bekhlusVVMKIo1Nc"
}


#the secret one right?
stripe.api_key = stripe_keys['secret_key']

app = Flask(__name__)
app.secret_key = 'auoesh.bouoastuh.43,uoausoehuosth3ououea.aubjakdfboub!'


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

app.config.update #wtf if this for?


# class BaseConfig(object):
#     """Base configuration."""
#
#     # main config
#     DEBUG = False
#     BCRYPT_LOG_ROUNDS = 13
#     WTF_CSRF_ENABLED = True
#     DEBUG_TB_ENABLED = False
#     DEBUG_TB_INTERCEPT_REDIRECTS = False
#
#     # mail settings
#     MAIL_SERVER = 'smtp.googlemail.com'
#     MAIL_PORT = 465
#     MAIL_USE_TLS = False
#     MAIL_USE_SSL = True
#
#     # gmail authentication
#     MAIL_USERNAME = os.environ['MAIL_USERNAME']
#     MAIL_PASSWORD = os.environ['MAIL_PASSWORD']
#
#     # mail accounts
#     MAIL_DEFAULT_SENDER = 'human@storaage.io'


app.config.update(dict(
    DEBUG = True,
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = 587,
    MAIL_USE_TLS = True,
    MAIL_USE_SSL = False,
    MAIL_USERNAME = 'storaage.app@gmail.com',
    MAIL_PASSWORD = 'Space_Saver',

    #please work! this would be cool
    MAIL_DEFAULT_SENDER = 'human@storaage.io'

))



mail = Mail()
mail.init_app(app)


@login_manager.user_loader
def load_user(userid):
    try:
        return models.User.get(models.User.id == userid)
    except models.DoesNotExist:
        return None



@app.before_request
def before_request():
    """Connect to the database before each request."""
    g.db = models.DATABASE
    g.db.connect()
    g.user = current_user


@app.route('/')
def index():
    #buy sell boxes might as well be index.html TODO: change the contents of buy_sell_boxes to index
    # change the contents to index.html
# num_listings=models.SellListing.count()
    # if current_user.is_anonymous is not True and current_user.is_admin() is True: #TODO come back bc it doesnt register admins correctly
    #     return render_template('admin-stats.html', models=models)
    # else:
    model_count = models.User.select().count()
    if 1:
        pass
    #needs to be updated
    listing_count = models.SellListing.select().count()
    return render_template('layout.html', count_of_sell_listings = listing_count, models = models)
    # return render_template('index.html', count_of_sell_listings = listing_count)

# Messed up but may be useful in the future
# @app.route('/login', methods=('GET','POST'))
# def login():
#     form = forms.LoginForm()
#     if form.validate_on_submit():
#         try:
#             user = models.User.get(models.User.email == form.email.data)
#         except models.DoesNotExist:
#             flash("Your email or password do not match. COMMEEE ONNN")
#         else:
#             if check_password_hash(user.password, form.password.data):
#                 login_user(user)
#                 flash("You've been logged in!! Welcome to Storage!!", 'success')
#                 return redirect('login.html')
#
#
# @app.route('/confirm/<token>')
# @login_required
# def confirm_email(token):
#     try:
#         email = confirm_token(token)
#     except:
#         flash("The confirmation link is invalid or has exipred", 'danger')
#     user_instance = models.User.query.filter_by(email=email).first_or_404()
#     if user.confirmed_email:
#         flash("Account already confirmed. Please login.", 'success')
#     else:
#         user.confirmed_email = True
#         user.confirmed_on = datetime.datetime.now()
#         models.session.add(user)
#         models.session.commit()
#         flash("You have confirmed your account. Thanks!", 'success')
#         return redirect(url_for(index))




#lets send an enail
@app.route('/register', methods=("GET", "POST"))
def register():
    form = forms.RevisedRegisterForm()
    if form.validate_on_submit():
        flash("WOOT WOOT!! You've been registered", 'success')
        flash("Now just check your email, confirm it, and you'll be ready to go!")
        new_user = models.User.create_user(
            username = form.username.data,
            first_name = form.firstname.data,
            last_name = form.lastname.data,
            email = form.email.data,
            password = form.password.data
            # confirmed_email = False,
            # is_admin = False
        )
        user = models.User.select().where(models.User.email == form.email.data).get()
        # login_user(current_user) why doesn't this log the guy in????!!!!

        #app email logic
        token = generate_confirmation_token(user.email)
        confirm_url = url_for('confirm_email', token=token, _external=True)
        html = render_template('activate_email.html', confirm_url=confirm_url)
        subject = "Hello from Storaage!"

        # import pdb; pdb.set_trace()

        send_email(user.email, subject, html)

        login_user(user)

        return redirect(url_for('index'))
    return render_template('register.html', form=form)

@app.route('/login', methods=("GET", "POST"))
def login():
    form = forms.LoginForm()
    if form.validate_on_submit():
        try:
            user = models.User.get(models.User.email == form.email.data)
        except models.DoesNotExist:
            flash("Your email or password do not match our records", 'error')
        else:
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember=True)
                flash("You've been logged in!", 'success')
                return redirect(url_for('index'))
            else:
                flash('Your email or password dont match dude', "error")
    return render_template('login.html', form=form)


@login_required
@app.route('/logout', methods=("GET", "POST"))
def logout():
    logout_user()
    flash("You've been logged out! Come back soon!", "success")
    return redirect(url_for('index'))


@app.route('/settings')
def settings():
    # if g.user.is_admin:
    #     return render_template('settings.html')
    return redirect(url_for('login'))


@app.route("/confirm/<token>")
@login_required
def confirm_email(token):
    try:
        email_for_confimation = confirm_token(token)
    except:
        flash("The confirmation link is invalid or has expired! Oh noes", 'danger')
    user = models.User.select().where(models.User.email == email_for_confimation).get()
    if user.confirmed_email:
        flash("Yo the account is already confirmed. I have no idea how you got here")
    else:
        user.confirmed_email = True
        user.save()
        #very important to save the crap to the database otherwise it will not update the DB

        # DATABASE.commit()
        # g.db.session.add(user)
        # g.db.session.commit()
        #peewee takes care of the transaction
        flash("congrats, you've confirmed your account")
    return redirect(url_for('index'))








@login_required
@app.route('/marketplace')
def marketplace():
    #this is going to be very similar to stream
    form = forms.SearchMarketPlace()
    template = 'marketplace.html'
    listing_list = models.SellListing.select().limit(10)
    user = current_user # Could use this line later with queries

    return render_template('marketplace.html', posts=listing_list, form=form , models =models)





@login_required
@app.route('/buy/<username>', methods=('GET','POST'))
def buy(username):
    if username and username == current_user.username:
        #allow for the page to be rendered
        form = forms.RevisedBuyForm()
        form_supplament = forms.NumBoxesPerSelection()

        if form.validate_on_submit() and form_supplament.validate_on_submit():

            bid_calculation = form.container_choice.data

            # test_string = ""
            cost_total = 0
            for single_bid in bid_calculation:
                cost_for_one_element_of_the_bid_calc = switch_equivalent = {
                    'Small' : 2 * 1, # the one stands for how many they want,
                    'Medium' : 4 *1, #same thing ^^,
                    'Large' : 8 * 1, #Yo read what i wrote ^^
                    'XLarge' : 12 *1 # see above

                }[single_bid] # would add the (x) after the value if i were to do that
                #hint, im going to do that
                cost_total += cost_for_one_element_of_the_bid_calc

                # return switch_equivalent nope that ends the function
            search = models.BuyListing.create(
                user = g.user.id,
                cubic_feet = form.container_choice.data,
                bid = cost_total,
                what_user_needs = form.specs.data
            )
            try:


                #mission critical function right here
                #params are number or each thing thats passed in
                # first 4 lines are based on the actual physical dimentions
                def figure_out_how_many_fit(s,m,l,xl):
                    # size box to num ^3rd feet
                    s_to_3rd = s * 1 #1 cubic foot
                    m_to_3rd = m * 3 # cubic feet
                    l_to_3rd = l * 6
                    xl_to_3rd = l * 10

                    total_space_buyer_wants = (s_to_3rd + m_to_3rd+ l_to_3rd + xl_to_3rd)
                            #should have something that tests the space avail first and then
                            #maybe the price
                    print(total_space_buyer_wants)
                    try:
                        all_listings = models.SellListing.select().where(
                                    models.SellListing.cubic_feet_avail >= total_space_buyer_wants)

                                    # You moron! You cannot itterate through a model element
                        # for listing in all_listings:
                        #     print(listing)
                        # for listing in all_listings:
                        return all_listings
                    except models.DoesNotExist:
                        flash("There are currently no listings that match your exact specifications :/ Feel free to look at our marketplace")
                        pass
                matched_listings = figure_out_how_many_fit(form_supplament.smll.data, form_supplament.med.data, form_supplament.lrg.data,form_supplament.Xlrg.data) # these numbers are going to change dynamically
                # print(matched_listings.get())
                # search = models.BuyListing.select().where(BuyListing.user == current_user)
                # match_feet = (models.SellListing.select().where(search.cubic_feet == BuyListing.cubic_feet_avail)).get()
                # match_price = (models.SellListing.select().where(search.bid == BuyListing.ask)).get()


            except models.DoesNotExist:
                flash("Something went horribly wrong and the listing you just created does not wasn't created propertly."
                +" Either try again (Hint do this one) or go outside and get a chai latte (And deliver it to me. Love those things)", 'error')
            else:
                return render_template('marketplace.html', posts=matched_listings, form=forms.SearchMarketPlace() , models = models)



                #redirects to the market place if no matches are found. Maybe i should tell them that no exact matches were found
            # return redirect('/marketplace')
        return render_template('buy_form.html', form=form, form2=form_supplament, models=models)

    else:
        flash('Yo get the hell outta here! You have to log in first!')
        return redirect(url_for('index'))

@login_required
@app.route('/sell/<username>', methods=('GET','POST'))
def sell(username):
    if username and username == current_user.username:
        #agaion lets not allow users to post to our db if they are not logged in
        form = forms.SellForm()

        if form.validate_on_submit():
            models.SellListing.create(
                user = g.user.id,
                cubic_feet_avail = form.cubic_feet.data,
                ask = form.ask.data,
                what_user_is_offering = form.specs.data
            )
            return redirect('/marketplace')
        return render_template('sell_form.html', form=form, models=models) #pass in models for

    else:
        flash("Dude(or dudet) you are not logged in at all. You need to rethink your life and log in")
        return redirect(url_for('index'))

@login_required
@app.route('/marketplace/<int:listing_id>', methods=('GET', 'POST'))
def single_listing(listing_id):
    if isinstance(listing_id, int):
        single_listing = models.SellListing.select().join(models.User).where(models.SellListing.id == listing_id).get()
        # seller = models.User.select().where(models.SellListing.user == single_listing.user).get()
        print(single_listing)



    else:
        flash("Something went wrong returning the specific listing for the database. Sorry!!")
        single_listing = None
    # single_listing_usable = single_listing.exicute()
    #use list comprehension to exicute quiery
    # [l for listing_use in single_listing]
    return render_template('single_listing_template.html', listing = single_listing, models= models) #, bout_seller = seller

    #HOLY GOOD GOD ITS DONE
    #KEEP IN MIND THAT WE SHOULD NOT KEEP MODELS IN ALL THE GODDAMN TEMPLATES

#
#
#
# @app.route("/_render_single_listing")
# def render_single_listing():
#     single_listing = models.SellListing.select().where(request.args.get('a',None, type=int) == models.SellListing.id)
#
#
#     # used regex to make the string version
#     return model_to_dict(single_listing)
#     #listing_to_be_passed =
    #(re.sub(r"[^0-9]*", '' , str(single_listing)))

    #not returning render template anymore

# ------y----o----l----o--------p---a---y--------
@login_required
@app.route('/marketplace/<int:listing_id>/charge', methods=("GET","POST"))
def single_listing_stipe_charger(listing_id):



        # next line is a bit confusing so lets walk through it
        # request allows you to see the form data that is submitted.
        # does it run continously that the object retrieval happens async??
        # I sure hope so
        # the posted data acts as an array that we can reach IntegrityError#
        # why cant we just use dot notation

        # throught the request object in flask ????
    #token = request.POST['stripeToken'] # gets the credit card details subbmitted by the form

    # Well lolz after all that work we have a token that is rendered useless


        #create a customer
    customer_storaage = stripe.Customer.create(
            card = request.form['stripeToken'], # could also be source if card fails,
            email = g.user.email,
            description ="Example Customer"
            )
    seller = models.SellListing.select().where(models.SellListing.id == listing_id).get()
    if ((int(seller.ask)*100* int(seller.cubic_feet_avail))) <= 100:  # this multiplies the two togeth
        ammount_from_listing = 500 # minimume purchase price
    else:

        print(int(seller.ask))
        print(100)
        print(int(seller.cubic_feet_avail))

        ammount_from_listing = (int(seller.ask) * 100 * int(seller.cubic_feet_avail))

        #create the reuqest on Stipes servers - this will charge the user's card

    try:
        charge = stripe.Charge.create(
            amount=ammount_from_listing, #CALM DOWN!! ITS IN CENTS
            currency="usd",
            customer=customer_storaage.id,
            description="Test test yoloSwag"
        )
    except stripe.error.CardError as e:
        flash("yo there was an error reading your card. Please try again")
        # the card has been declined
        pass

    flash("We are processing your Payment!!!")

    return redirect('/marketplace')


# ------s----w----a----g----------------------


if __name__ == '__main__':
    models.initialize()
    try:
        models.User.create_user(
            username='davidaxelrod',
            first_name = "David",
            last_name = "Axelrod",
            email='daxaxelrod@gmail.com',
            password='testpassword!',
            is_admin = True,
            confirmed_email = True


        )
    except ValueError:
        pass
    app.run(debug=DEBUG, host=HOST, port=PORT)
