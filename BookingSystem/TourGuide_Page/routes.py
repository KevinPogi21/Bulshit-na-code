from flask import render_template, redirect, url_for, flash, request, session, jsonify
from flask_login import login_required, current_user, logout_user, login_user
from BookingSystem.TourOperator_Page import touroperator
from . import tourguide  
from BookingSystem.TourOperator_Page.form import UserTourGuideForm
from BookingSystem import bcrypt, db
from werkzeug.security import check_password_hash, generate_password_hash
from BookingSystem.models import User, Characteristic, Skill, Availability
import os




@tourguide.route('/tourguide_dashboard')
@login_required
def tourguide_dashboard():
    print(f"Current user in dashboard: {current_user.email}, Role: {current_user.role}")
    # Your dashboard logic here
    return render_template('tourguide_dashboard.html')


@tourguide.route('/update-password', methods=['POST'])
@login_required
def update_password():
    data = request.get_json()
    logging.info(f"Data received: {data}")

    if not data:
        logging.error("No data received or invalid JSON.")
        return jsonify({"error": "Invalid input"}), 400

    current_password = data.get('current_password')
    new_password = data.get('new_password')

    if not current_user.password:
        logging.error("User password is missing or empty in the database.")
        return jsonify({"error": "User password not set."}), 500

    if not check_password_hash(current_user.password, current_password):
        logging.warning(f"Password mismatch for user: {current_user.email}")
        return jsonify({"error": "Current password is incorrect"}), 400

    if not new_password or len(new_password) < 6:
        logging.warning("New password validation failed.")
        return jsonify({"error": "New password must be at least 6 characters long"}), 400

    try:
        hashed_password = generate_password_hash(new_password)
        current_user.password = hashed_password
        db.session.commit()

        # Refresh the user session after password change
        login_user(current_user)
        logging.info("Password updated successfully.")
        return jsonify({"message": "Password updated successfully"}), 200
    except Exception as e:
        logging.error(f"Error updating password: {e}")
        return jsonify({"error": "Failed to update password"}), 500




@tourguide.route('/save-profile', methods=['POST'])
@login_required
def save_profile():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'error': 'No data received.'}), 400

        # Update permanent fields in the database
        current_user.fname = data.get('first_name')
        current_user.lname = data.get('last_name')
        current_user.email = data.get('email')
        current_user.contact_number = data.get('contact_number')
        current_user.bio = data.get('about')  # Save bio (about) in UserTourGuide

        # Update characteristics
        new_characteristics = data.get('characteristics', [])
        current_user.characteristics.clear()  # Clear current characteristics
        for characteristic_text in new_characteristics:
            characteristic = Characteristic(characteristic=characteristic_text)
            current_user.characteristics.append(characteristic)

        # Update skills
        new_skills = data.get('skills', [])
        current_user.skills.clear()  # Clear current skills
        for skill_text in new_skills:
            skill = Skill(skill=skill_text)
            current_user.skills.append(skill)

        # Commit all changes to the database
        db.session.commit()

        return jsonify({'success': True}), 200
    except Exception as e:
        db.session.rollback()  # Roll back in case of an error
        return jsonify({'success': False, 'error': str(e)}), 500
@login_required
def save_profile():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'error': 'No data received.'}), 400

        # Update user fields with the data from the request
        current_user.fname = data.get('first_name')
        current_user.lname = data.get('last_name')
        current_user.email = data.get('email')
        current_user.contact_number = data.get('contact_number')
        
        # Update 'About Me' (bio) field
        current_user.bio = data.get('about', '')

        # Update characteristics
        characteristics = data.get('characteristics', [])
        current_user.characteristics.clear()  # Clear existing characteristics
        for char_text in characteristics:
            new_char = Characteristic(characteristic=char_text, tour_guide=current_user)
            db.session.add(new_char)

        # Update skills
        skills = data.get('skills', [])
        current_user.skills.clear()  # Clear existing skills
        for skill_text in skills:
            new_skill = Skill(skill=skill_text, tour_guide=current_user)
            db.session.add(new_skill)

        # Commit all changes to the database
        db.session.commit()

        return jsonify({'success': True}), 200
    except Exception as e:
        db.session.rollback()  # Roll back in case of an error
        return jsonify({'success': False, 'error': str(e)}), 500







@tourguide.route('/logout')
@login_required
def logout():
    logout_user()
    session.clear()
    flash('Logged out successfully.', 'success')
    return redirect(url_for('main.home'))





