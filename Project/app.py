from flask import Flask, render_template, request, redirect, url_for, session
from flask_mail import Mail, Message
from datetime import datetime, timedelta
from flask_mysqldb import MySQL
from flask_session import Session

app = Flask(__name__)
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'fitness_center'
mysql = MySQL(app)

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'crimedetectionproject@gmail.com'
app.config['MAIL_PASSWORD'] = 'pyrv xlfs zalm syxy'
app.config['MAIL_DEFAULT_SENDER'] = 'crimedetectionproject@gmail.com'
mail = Mail(app)

@app.route('/')
def login():
    message = request.args.get('message', None)
    return render_template('login.html', message=message)

@app.route('/authenticate', methods=['POST'])
def authenticate():
    role = request.form['role']
    username = request.form['username']
    password = request.form['password']

    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s AND role=%s", (username, password, role))
    user = cursor.fetchone()
    mysql.connection.commit()
    cursor.close()

    if user:
        session['user_id'] = user[0]
        session['username'] = user[1]
        session['role'] = user[3]

        if user[3] == 'admin':
            return redirect(url_for('admin_dashboard'))
        elif user[3] == 'receptionist':
            return redirect(url_for('receptionist_dashboard'))
        elif user[3] == 'trainer':
            return redirect(url_for('trainer_dashboard'))
    else:
        message = "Incorrect username/password"
        return redirect(url_for('login', message=message))

@app.route('/admin_dashboard')
def admin_dashboard():
    if 'user_id' in session and 'username' in session and 'role' in session and session['role'] == 'admin':
        return render_template('admin_dashboard.html')
    else:
        return redirect(url_for('login'))


@app.route('/add_remove_trainer')
def add_remove_trainer():
    message = request.args.get('message', None)
    return render_template('add_remove_trainer.html', message=message)

@app.route('/add_removetrainer', methods=['POST'])
def add_removetrainer():
    if 'user_id' in session and 'username' in session and 'role' in session and session['role'] == 'admin':
        operation = request.form['operation']
        trainer_name = request.form['trainer_name']
        username = request.form['username']
        password = request.form['password']
        trainer_id = request.form['trainer_id']
        trainer_contact = request.form['trainer_contact']

        cursor = mysql.connection.cursor()
        if operation == 'add':
            cursor.execute("SELECT * FROM users WHERE username = %s OR user_id = %s", (username, trainer_id))
            user = cursor.fetchone()
            if user:
                message = "username or user id already exists"
                return redirect(url_for('add_remove_trainer', message=message))
            cursor.execute("insert into users values(%s,%s,%s,%s)", (trainer_id, username, password, "trainer"))
            cursor.execute("insert into trainers values(%s,%s,%s)", (trainer_id, trainer_name, trainer_contact))
            mysql.connection.commit()
            message1 = "Trainer added successfully"
            return redirect(url_for('add_remove_trainer', message=message1))
        elif operation == 'remove':
            cursor.execute("SELECT * FROM users WHERE username = %s AND  user_id = %s AND password=%s", (username, trainer_id, password))
            user = cursor.fetchone()
            if not user:
                message2 = "No user with the given credentials"
                return redirect(url_for('add_remove_trainer', message=message2))
            cursor.execute("select * from trainers where trainer_id=%s AND trainer_name=%s AND trainer_contact=%s",
                           (trainer_id, trainer_name, trainer_contact))
            user1 = cursor.fetchone()
            if not user1:
                message3 = "No user with the given credentials"
                return redirect(url_for('add_remove_trainer', message=message3))
            result = cursor.execute(
                "DELETE FROM trainers WHERE trainer_id = %s AND trainer_name = %s AND trainer_contact = %s",
                (trainer_id, trainer_name, trainer_contact))
            cursor.execute("DELETE FROM trainer_member_relationship where trainer_id=%s",(trainer_id,))
            result1 = cursor.execute(
                "DELETE FROM users WHERE user_id = %s AND username = %s AND password=%s AND role= %s",
                (trainer_id, username, password, "trainer"))
            mysql.connection.commit()
            message4 = "Deleted Trainer Succesfully "
            return redirect(url_for('add_remove_trainer', message=message4))
        cursor.close()
    else:
        return redirect(url_for('login'))

@app.route('/add_remove_member')
def add_remove_member():
    message = request.args.get('message', None)
    return render_template('add_remove_member.html', message=message)

@app.route('/add_removemember', methods=['POST'])
def add_removemember():
    if 'user_id' in session and 'username' in session and 'role' in session and ((session['role'] == 'admin') or (session['role'] == 'receptionist')):
        operation = request.form['operation']
        member_name = request.form['member_name']
        username = request.form['username']
        password = request.form['password']
        member_id = request.form['member_id']
        email_id = request.form['email_id']
        member_contact = request.form['member_contact']
        workout_plan_id = request.form['workout_plan_id']

        cursor = mysql.connection.cursor()
        if operation == 'add':
            cursor.execute("SELECT * FROM users WHERE username = %s OR user_id = %s", (username, member_id))
            user = cursor.fetchone()
            if user:
                message = "Username or User ID already exists"
                return redirect(url_for('add_remove_member', message=message))
            cursor.execute("SELECT * FROM workout_plans WHERE plan_id = %s", (workout_plan_id,))
            isthere = cursor.fetchone();
            if not isthere:
                message = "Invalid workout plan"
                return redirect(url_for('add_remove_member', message=message))
            cursor.execute("insert into users values(%s, %s, %s, %s)", (member_id, username, password, "member"))
            cursor.execute("insert into members(member_id, member_name, member_contact,email_id, workout_plan_id) values(%s, %s, %s, %s,%s)",
                           (member_id, member_name, member_contact,email_id, workout_plan_id))
            mysql.connection.commit()
            message = "Member added successfully"
            return redirect(url_for('add_remove_member', message=message))
        elif operation == 'remove':
            cursor.execute("SELECT * FROM users WHERE username = %s AND  user_id = %s AND password=%s",
                           (username, member_id, password))
            user = cursor.fetchone()
            if not user:
                message2 = "No user with the given credentials"
                return redirect(url_for('add_remove_member', message=message2))
            cursor.execute(
                "SELECT * FROM members WHERE member_id=%s AND member_name=%s AND member_contact=%s AND workout_plan_id=%s",
                (member_id, member_name, member_contact, workout_plan_id))
            user1 = cursor.fetchone()
            if not user1:
                message3 = "No user with the given credentials"
                return redirect(url_for('add_remove_member', message=message3))
            result = cursor.execute(
                "DELETE FROM members WHERE member_id = %s AND member_name = %s AND member_contact = %s AND workout_plan_id = %s",
                (member_id, member_name, member_contact, workout_plan_id))
            cursor.execute("DELETE FROM trainer_member_relationship where member_id=%s",(member_id,))
            result1 = cursor.execute(
                "DELETE FROM users WHERE user_id = %s AND username = %s AND password=%s AND role= %s",
                (member_id, username, password, "member"))
            mysql.connection.commit()
            message4 = "Deleted Member Successfully "
            return redirect(url_for('add_remove_member', message=message4))
        cursor.close()
    else:
        return redirect(url_for('login'))

@app.route('/add_remove_receptionist')
def add_remove_receptionist():
    message = request.args.get('message', None)
    return render_template('add_remove_receptionist.html', message=message)

@app.route('/add_removereceptionist', methods=['POST'])
def add_removereceptionist():
    if 'user_id' in session and 'username' in session and 'role' in session and session['role'] == 'admin':
        operation = request.form['operation']
        recep_name = request.form['recep_name']
        username = request.form['username']
        password = request.form['password']
        recep_id = request.form['recep_id']
        recep_contact = request.form['recep_contact']

        cursor = mysql.connection.cursor()
        if operation == 'add':
            cursor.execute("SELECT * FROM users WHERE username = %s OR user_id = %s", (username, recep_id))
            user = cursor.fetchone()
            if user:
                message = "Username or User ID already exists"
                return redirect(url_for('add_remove_receptionist', message=message))
            cursor.execute("INSERT INTO users VALUES (%s, %s, %s, %s)", (recep_id, username, password, "receptionist"))
            cursor.execute("INSERT INTO receptionist VALUES (%s, %s, %s)", (recep_id, recep_name, recep_contact))
            mysql.connection.commit()
            message = "Receptionist added successfully"
            return redirect(url_for('add_remove_receptionist', message=message))
        elif operation == 'remove':
            cursor.execute("SELECT * FROM users WHERE username = %s AND user_id = %s AND password = %s",
                           (username, recep_id, password))
            user = cursor.fetchone()
            if not user:
                message2 = "No user with the given credentials"
                return redirect(url_for('add_remove_receptionist', message=message2))
            cursor.execute(
                "SELECT * FROM receptionist WHERE recep_id = %s AND recep_name = %s AND recep_contact = %s",
                (recep_id, recep_name, recep_contact))
            receptionist = cursor.fetchone()
            if not receptionist:
                message3 = "No user with the given credentials"
                return redirect(url_for('add_remove_receptionist', message=message3))
            result = cursor.execute(
                "DELETE FROM receptionist WHERE recep_id = %s AND recep_name = %s AND recep_contact = %s",
                (recep_id, recep_name, recep_contact))
            result1 = cursor.execute(
                "DELETE FROM users WHERE user_id = %s AND username = %s AND password = %s AND role = %s",
                (recep_id, username, password, "receptionist"))
            mysql.connection.commit()
            message4 = "Deleted Receptionist Successfully"
            return redirect(url_for('add_remove_receptionist', message=message4))
        cursor.close()
    else:
        return redirect(url_for('login'))

@app.route('/view_users')
def view_users():
    if 'user_id' in session and 'username' in session and 'role' in session and ((session['role'] == 'admin') or (session['role'] == 'receptionist')):
        cursor = mysql.connection.cursor()

        cursor.execute("SELECT * FROM members")
        members = cursor.fetchall()

        cursor.execute("SELECT * FROM trainers")
        trainers = cursor.fetchall()

        cursor.execute("SELECT * FROM receptionist")
        receptionists = cursor.fetchall()

        cursor.execute("SELECT user_id, username, role FROM users WHERE role='admin'")
        admins = cursor.fetchall()

        cursor.execute("SELECT * FROM workout_plans")
        workout_plans = cursor.fetchall()

        cursor.execute("SELECT * FROM equipment")
        equipment = cursor.fetchall()

        cursor.close()

        return render_template('view_users.html', members=members, trainers=trainers, receptionists=receptionists,
                               admins=admins, workout_plans=workout_plans, equipment=equipment)
    else:
        return redirect(url_for('login'))

@app.route('/add_equipment_page')
def add_equipment_page():
    message = request.args.get('message', None)
    return render_template('add_equipments.html', message=message)

@app.route('/add_equipment', methods=['POST'])
def add_equipment():
    if 'user_id' in session and 'username' in session and 'role' in session and session['role'] == 'admin':
        equipment_id = request.form['equipment_id']
        equipment_name = request.form['equipment_name']
        quantity = request.form['quantity']
        purchase_date = request.form['purchase_date']
        cursor = mysql.connection.cursor()

        cursor.execute("SELECT * FROM equipment WHERE equipment_id = %s", (equipment_id,))
        existing_equipment = cursor.fetchone()

        if existing_equipment:
            if (str(existing_equipment[1]) == str(equipment_name)) and (str(existing_equipment[0]) == str(equipment_id)):
                new_quantity = int(existing_equipment[2]) + int(quantity)
                cursor.execute("UPDATE equipment SET quantity = %s, purchase_date = %s WHERE equipment_id = %s",
                               (new_quantity, purchase_date, equipment_id))
                mysql.connection.commit()
                message = "Added succesfully"
                return redirect(url_for('add_equipment_page', message=message))
            else:
                message = "Wrong name/equipment ID"
                return redirect(url_for('add_equipment_page', message=message))
        else:
            cursor.execute("INSERT INTO equipment (equipment_id, equipment_name, quantity, purchase_date) VALUES (%s, %s, %s, %s)",
                           (equipment_id, equipment_name, quantity, purchase_date))

        mysql.connection.commit()
        cursor.close()

        message = "Equipment added successfully"
        return redirect(url_for('add_equipment_page', message=message))
    else:
        return redirect(url_for('login'))

@app.route('/assign_trainer', methods=['POST'])
def assign_trainer():
    if 'user_id' in session and 'username' in session and 'role' in session and session['role'] == 'admin':
        member_id = request.form['member_id']
        trainer_id = request.form['trainer_id']

        cursor = mysql.connection.cursor()

        cursor.execute("SELECT * FROM members WHERE member_id = %s", (member_id,))
        member = cursor.fetchone()

        cursor.execute("SELECT * FROM trainers WHERE trainer_id = %s", (trainer_id,))
        trainer = cursor.fetchone()

        if member and trainer:
            cursor.execute("SELECT * FROM trainer_member_relationship WHERE member_id = %s", (member_id,))
            existing_assignment = cursor.fetchone()

            if existing_assignment:
                cursor.execute("UPDATE trainer_member_relationship SET trainer_id = %s WHERE member_id = %s", (trainer_id, member_id))
            else:
                cursor.execute("INSERT INTO trainer_member_relationship (member_id, trainer_id) VALUES (%s, %s)", (member_id, trainer_id))

            mysql.connection.commit()
            cursor.close()

            message = "Trainer assigned successfully"
            return redirect(url_for('assign_trainer_page', message=message))
        else:
            message = "Invalid Member ID or Trainer ID"
            return redirect(url_for('assign_trainer_page', message=message))
    else:
        return redirect(url_for('login'))

@app.route('/assign_trainer_page')
def assign_trainer_page():
    message = request.args.get('message', None)
    return render_template('assign_trainer.html', message=message)

@app.route('/receptionist_dashboard')
def receptionist_dashboard():
    if 'user_id' in session and 'username' in session and 'role' in session and session['role'] == 'receptionist':
        return render_template('receptionist_dashboard.html')
    else:
        return redirect(url_for('login'))

@app.route('/view_receptionist_profile')
def view_receptionist_profile():
    if 'user_id' in session and 'username' in session and 'role' in session and session['role'] == 'receptionist':
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM receptionist WHERE recep_id = %s", (session['user_id'],))
        receptionist = cursor.fetchone()
        cursor.close()
        return render_template('view_receptionist_profile.html', receptionist=receptionist)
    else:
        return redirect(url_for('login'))


@app.route('/trainer_dashboard')
def trainer_dashboard():
    if 'user_id' in session and 'username' in session and 'role' in session and session['role'] == 'trainer':
        return render_template('trainer_dashboard.html')
    else:
        return redirect(url_for('login'))

@app.route('/add_workout_plan', methods=['GET', 'POST'])
def add_workout_plan():
    if 'user_id' in session and 'username' in session and 'role' in session and session['role'] == 'trainer':
        if request.method == 'POST':
            plan_name = request.form['plan_name']
            monday = request.form['monday']
            tuesday = request.form['tuesday']
            wednesday = request.form['wednesday']
            thursday = request.form['thursday']
            friday = request.form['friday']
            saturday = request.form['saturday']


            cursor = mysql.connection.cursor()

            cursor.execute("SELECT * FROM workout_plans WHERE plan_name = %s", (plan_name,))
            existing_plan = cursor.fetchone()

            if existing_plan:
                message = "Workout plan with the same name already exists. Please choose a different name."
                cursor.close()
                return render_template('add_workout_plan.html', message=message)

            cursor.execute("INSERT INTO workout_plans (plan_name, monday, tuesday, wednesday, thursday, friday, saturday) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                           (plan_name, monday, tuesday, wednesday, thursday, friday, saturday))
            mysql.connection.commit()
            cursor.close()

            message = "Workout plan added successfully"
            return render_template('add_workout_plan.html', message=message)

        return render_template('add_workout_plan.html')
    else:
        return redirect(url_for('login'))

@app.route('/view_clients')
def view_clients():
    if 'user_id' in session and 'username' in session and 'role' in session and session['role'] == 'trainer':
        trainer_id = session['user_id']

        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM members WHERE member_id IN (SELECT member_id FROM trainer_member_relationship WHERE trainer_id = %s)", (trainer_id,))
        clients = cursor.fetchall()
        cursor.close()

        return render_template('view_clients.html', clients=clients)
    else:
        return redirect(url_for('login'))

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'crimedetectionproject@gmail.com'
app.config['MAIL_PASSWORD'] = 'pyrv xlfs zalm syxy'
app.config['MAIL_DEFAULT_SENDER'] = 'crimedetectionproject@gmail.com'
mail = Mail(app)

@app.route('/send_reminder_emails')
def send_reminder_emails():
    if 'user_id' in session and 'username' in session and 'role' in session and session['role'] == 'receptionist':
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT member_id, email_id, start_date FROM members WHERE DATE_ADD(start_date, INTERVAL 30 DAY) <= NOW()")
        members_to_notify = cursor.fetchall()
        
        for member in members_to_notify:
            member_id, email, start_date = member
            subject = 'Membership Renewal Reminder'
            body = f"Dear Member,\n\nYour 30-day membership is about to expire. Please renew your membership."
            message = Message(subject=subject, body=body, recipients=[email])
            mail.send(message)
            new_start_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            cursor.execute("UPDATE members SET start_date = %s WHERE member_id = %s", (new_start_date, member_id))
        
        mysql.connection.commit()
        cursor.close()
        message="Reminder emails sent successfully."
        return(render_template('receptionist_dashboard.html',message=message))

    return redirect(url_for('login'))

@app.route('/view_trainer_profile')
def view_trainer_profile():
    if 'user_id' in session and 'username' in session and 'role' in session and session['role'] == 'trainer':
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM trainers WHERE trainer_id = %s", (session['user_id'],))
        trainer = cursor.fetchone()
        cursor.close()
        return render_template('view_trainer_profile.html', trainer=trainer)
    else:
        return redirect(url_for('login'))


@app.route('/home')
def home():
    if session['role'] == 'admin':
        return redirect(url_for('admin_dashboard'))
    elif session['role'] == 'receptionist':
        return redirect(url_for('receptionist_dashboard'))
    elif session['role'] == 'trainer':
        return redirect(url_for('trainer_dashboard'))
    elif session['role'] == 'member':
        return redirect(url_for('member_dashboard'))
    


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
