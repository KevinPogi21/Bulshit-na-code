from flask import render_template, redirect, url_for, flash, request, session
from flask_login import login_required, current_user, logout_user
from . import touroperator  
from werkzeug.security import generate_password_hash, check_password_hash
from BookingSystem import bcrypt, db 
from BookingSystem.TourOperator_Page.form import UserTourGuideForm
from BookingSystem.models import User, TourOperator, TourGuide

@touroperator.route('/create_tourguide', methods=['GET', 'POST'])
@login_required
def create_tourguide():
    form = UserTourGuideForm()  # Instantiate the form
    if form.validate_on_submit():
        # Hash the password
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        
        # Create a new tour guide instance
        new_tourguide_user = User(
            first_name=form.fname.data,
            last_name=form.lname.data,
            email=form.email.data,
            password=hashed_password,
            role='tourguide',
        )

        try:
            # Save to the database
            db.session.add(new_tourguide_user)
            db.session.commit()
            
            
            tour_operator = TourOperator.query.filter_by(user_id=current_user.id).first()
            if not tour_operator:
                flash("Error: Current user is not a valid tour operator.", 'danger')
                return redirect(url_for('touroperator.touroperator_dashboard'))

            flash("Tour Operator ID: {tour_operator.id}")  # Debugging: Check the TourOperator ID
            
            # Create the TourGuide entry with the new User ID and the TourOperator's ID
            new_tourguide_record = TourGuide(
                user_id=new_tourguide_user.id,
                toperator_id=tour_operator.id,  # Use the TourOperator ID
                contact_num=form.contact_number.data,
            )
            db.session.add(new_tourguide_record)
            db.session.commit()
            flash('Tour Guide account created successfully!', 'success')
            return redirect(url_for('touroperator.touroperator_dashboard'))  # Redirect to the tour guide dashboard

        except Exception as e:
            # Handle errors gracefully
            db.session.rollback()
            flash('An error occurred while creating the account. Please try again.', 'danger')
            print(f"Database error: {e}")  # Debugging information

    return render_template('touroperator_dashboard.html', form=form)  # Render the create tour guide template


@touroperator.route('/dashboard')
@login_required
def touroperator_dashboard():
    # Ensure only tour operators can access this page
    if current_user.role != 'touroperator':
        flash('You do not have permission to access this page.', 'danger')
        return redirect(url_for('main.home'))
    
    form = UserTourGuideForm()  # Instantiate the form for the dashboard
    return render_template('touroperator_dashboard.html', title='TourOperator Dashboard', form=form)


@touroperator.route('/logout')
@login_required
def logout():
    logout_user()
    session.clear()
    flash('Logged out successfully.', 'success')
    return redirect(url_for('main.home'))





@touroperator.route('/tourguide_dashboard/<int:id>', methods=['GET'])
@login_required
def tourguide_profile(id):
    print(f"Received Tour Guide ID: {id}")  # Debug

    tourguide = User.query.get_or_404(id)
    print(f"Tour Guide: {tourguide.email}, ID: {tourguide.id}")  # Debug

    return render_template('tourguide_dashboard.html', tourguide=tourguide)



