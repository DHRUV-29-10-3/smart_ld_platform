from flask import Flask, render_template, request, redirect, session, url_for
import mysql.connector
from werkzeug.utils import secure_filename
import os
from dotenv import load_dotenv
from config import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME
from flask import send_from_directory

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def connect_db():
    return mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )


@app.route('/')
def home():
    return redirect('/register')


# ------------------------ REGISTER ------------------------
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        role = request.form['role']
        field = request.form['field']

        conn = connect_db()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        if cursor.fetchone():
            conn.close()
            return "User already exists. <a href='/login'>Login here</a>"

        cursor.execute("INSERT INTO users (name, email, password, role, field) VALUES (%s, %s, %s, %s, %s)",
                       (name, email, password, role, field))
        conn.commit()
        conn.close()
        return redirect('/login')

    return render_template('register.html')


# ------------------------ LOGIN ------------------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        conn = connect_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE email = %s AND password = %s", (email, password))
        user = cursor.fetchone()
        conn.close()

        if user:
            session['user'] = user
            return redirect(f"/dashboard/{user['role']}")
        return "Invalid credentials"
    return render_template('login.html')


# ------------------------ INSTRUCTOR DASHBOARD ------------------------
@app.route('/dashboard/instructor', methods=['GET', 'POST'])
def instructor_dashboard():
    if 'user' not in session or session['user']['role'] != 'instructor':
        return redirect('/login')

    conn = connect_db()
    cursor = conn.cursor(dictionary=True)

    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        course_type = request.form['type']  # 'video', 'document', or 'assignment'
        file = request.files['file']
        field = request.form['field']

        filename = None
        if file and file.filename:
            filename = secure_filename(file.filename)
            # Determine folder based on course_type
            if course_type == 'video':
                folder = os.path.join('course_materials', 'videos')
            elif course_type == 'document':
                folder = os.path.join('course_materials', 'documents')
            elif course_type == 'assignment':
                folder = os.path.join('course_materials', 'assignments')
            else:
                folder = 'uploads'  # fallback

            os.makedirs(folder, exist_ok=True)
            file.save(os.path.join(folder, filename))

        cursor.execute(
            "INSERT INTO courses (title, description, type, field, filename, instructor_id) VALUES (%s, %s, %s, %s, %s, %s)",
            (title, description, course_type, field, filename, session['user']['id'])
        )
        conn.commit()

    cursor.execute("SELECT * FROM courses WHERE instructor_id = %s", (session['user']['id'],))
    courses = cursor.fetchall()
    conn.close()
    return render_template("instructor_dashboard.html", user=session['user'], courses=courses)


# # ------------------------ DELETE COURSE ------------------------
# @app.route('/delete_course/<int:course_id>')
# def delete_course(course_id):
#     if 'user' not in session or session['user']['role'] != 'instructor':
#         return redirect('/login')

#     conn = connect_db()
#     cursor = conn.cursor()

#     cursor.execute("DELETE FROM courses WHERE id = %s AND instructor_id = %s",
#                    (course_id, session['user']['id']))
#     conn.commit()
#     conn.close()

#     return redirect('/dashboard/instructor')

@app.route('/delete_course/<int:course_id>')
def delete_course(course_id):
    if 'user' not in session or session['user']['role'] != 'instructor':
        return redirect('/login')

    conn = connect_db()
    cursor = conn.cursor()

    try:
        # Step 1: Remove all course assignments (due to FK constraint)
        cursor.execute("DELETE FROM assigned_courses WHERE course_id = %s", (course_id,))
        
        # Step 2: Now delete from course table
        cursor.execute("DELETE FROM courses WHERE id = %s AND instructor_id = %s",
                       (course_id, session['user']['id']))
        
        conn.commit()
    except mysql.connector.Error as err:
        conn.rollback()
        print("Error:", err)
        return f"❌ Error deleting course: {err}"
    finally:
        conn.close()

    return redirect('/dashboard/instructor')


# ------------------------ EDIT COURSE ------------------------
# @app.route('/edit_course/<int:course_id>', methods=['GET', 'POST'])
# def edit_course(course_id):
#     if 'user' not in session or session['user']['role'] != 'instructor':
#         return redirect('/login')

#     conn = connect_db()
#     cursor = conn.cursor(dictionary=True)

#     if request.method == 'POST':
#         title = request.form['title']
#         description = request.form['description']
#         course_type = request.form['type']
#         field = request.form['field']
#         file = request.files.get('file')

#         if file and file.filename:
#             filename = secure_filename(file.filename)
#             file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

#             cursor.execute("""
#                 UPDATE courses 
#                 SET title=%s, description=%s, type=%s, field=%s, filename=%s 
#                 WHERE id=%s AND instructor_id=%s
#             """, (title, description, course_type, field, filename, course_id, session['user']['id']))
#         else:
#             cursor.execute("""
#                 UPDATE courses 
#                 SET title=%s, description=%s, type=%s, field=%s 
#                 WHERE id=%s AND instructor_id=%s
#             """, (title, description, course_type, field, course_id, session['user']['id']))

#         conn.commit()
#         conn.close()
#         return redirect('/dashboard/instructor')

#     cursor.execute("SELECT * FROM courses WHERE id = %s AND instructor_id = %s", 
#                    (course_id, session['user']['id']))
#     course = cursor.fetchone()
#     conn.close()

#     if not course:
#         return "❌ Course not found or unauthorized access."

#     return render_template("edit_course.html", course=course)

@app.route('/edit_course/<int:course_id>', methods=['GET', 'POST'])
def edit_course(course_id):
    if 'user' not in session or session['user']['role'] != 'instructor':
        return redirect('/login')

    conn = connect_db()
    cursor = conn.cursor(dictionary=True)

    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        course_type = request.form['type']
        field = request.form['field']
        file = request.files.get('file')

        if file and file.filename:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            cursor.execute("""
                UPDATE courses 
                SET title=%s, description=%s, type=%s, field=%s, filename=%s 
                WHERE id=%s AND instructor_id=%s
            """, (title, description, course_type, field, filename, course_id, session['user']['id']))
        else:
            cursor.execute("""
                UPDATE courses 
                SET title=%s, description=%s, type=%s, field=%s 
                WHERE id=%s AND instructor_id=%s
            """, (title, description, course_type, field, course_id, session['user']['id']))

        conn.commit()
        conn.close()
        return redirect('/dashboard/instructor')

    cursor.execute("SELECT * FROM courses WHERE id = %s AND instructor_id = %s", 
                   (course_id, session['user']['id']))
    course = cursor.fetchone()
    conn.close()

    if not course:
        return "❌ Course not found or unauthorized access."

    return render_template("edit_course.html", course=course)



# ------------------------ LOGOUT ------------------------

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/login')


@app.route('/dashboard/admin', methods=['GET', 'POST'])
def admin_dashboard():
    if 'user' not in session or session['user']['role'] != 'admin':
        return redirect('/login')

    conn = connect_db()
    cursor = conn.cursor(dictionary=True)
    admin_field = session['user']['field']
    admin_id = session['user']['id']

    if request.method == 'POST':
        learner_id = request.form['learner_id']
        course_id = request.form['course_id']

        # Ensure field match between learner and admin
        cursor.execute("SELECT field FROM users WHERE id=%s AND role='learner'", (learner_id,))
        learner = cursor.fetchone()

        cursor.execute("SELECT field FROM courses WHERE id=%s", (course_id,))
        course = cursor.fetchone()

        if learner and course and learner['field'] == admin_field and course['field'] == admin_field:
            cursor.execute("INSERT INTO assigned_courses (learner_id, course_id, assigned_by) VALUES (%s, %s, %s)",
                           (learner_id, course_id, admin_id))
            conn.commit()

    # Fetch learners and courses only in admin's field
    cursor.execute("SELECT * FROM users WHERE role='learner' AND field=%s", (admin_field,))
    learners = cursor.fetchall()

    cursor.execute("SELECT * FROM courses WHERE field=%s", (admin_field,))
    courses = cursor.fetchall()

    cursor.execute("""
        SELECT ac.id, u.name AS learner_name, c.title AS course_title, ac.status
        FROM assigned_courses ac
        JOIN users u ON ac.learner_id = u.id
        JOIN courses c ON ac.course_id = c.id
        WHERE u.field = %s
    """, (admin_field,))
    assigned_courses = cursor.fetchall()

    conn.close()
    return render_template('admin_dashboard.html', learners=learners, courses=courses, assigned=assigned_courses)


# ------------------------ LEARNER DASHBOARD ------------------------# ...existing code...

# @app.route('/dashboard/learner', methods=['GET', 'POST'])
# def learner_dashboard():
#     if 'user' not in session or session['user']['role'] != 'learner':
#         return redirect('/login')

#     learner_id = session['user']['id']
#     conn = connect_db()
#     cursor = conn.cursor(dictionary=True)

#     if request.method == 'POST':
#         assignment_id = request.form['assignment_id']
#         cursor.execute("UPDATE assigned_courses SET status='completed' WHERE id=%s AND learner_id=%s",
#                        (assignment_id, learner_id))
#         conn.commit()

#     cursor.execute("""
#         SELECT ac.id, c.id AS course_id, c.title AS course_title, ac.status, c.filename, c.type
#         FROM assigned_courses ac
#         JOIN courses c ON ac.course_id = c.id
#         WHERE ac.learner_id = %s
#     """, (learner_id,))
#     assigned_courses = cursor.fetchall()

#     conn.close()
#     return render_template('learner_dashboard.html', assigned_courses=assigned_courses)




@app.route('/dashboard/learner', methods=['GET', 'POST'])
def learner_dashboard():
    if 'user' not in session or session['user']['role'] != 'learner':
        return redirect('/login')

    learner_id = session['user']['id']
    learner_field = session['user']['field']

    conn = connect_db()
    cursor = conn.cursor(dictionary=True)

    if request.method == 'POST':
        assignment_id = request.form['assignment_id']
        cursor.execute("UPDATE assigned_courses SET status='completed' WHERE id=%s AND learner_id=%s",
                       (assignment_id, learner_id))
        conn.commit()

    # Fetch assigned courses
    cursor.execute("""
        SELECT ac.id, c.id AS course_id, c.title AS course_title, ac.status, c.filename, c.type
        FROM assigned_courses ac
        JOIN courses c ON ac.course_id = c.id
        WHERE ac.learner_id = %s
    """, (learner_id,))
    assigned_courses = cursor.fetchall()

    # Get course IDs already assigned
    assigned_course_ids = [course['course_id'] for course in assigned_courses]
    format_strings = ','.join(['%s'] * len(assigned_course_ids)) if assigned_course_ids else 'NULL'

    # Fetch recommended courses (same field but not already assigned)
    if assigned_course_ids:
        cursor.execute(f"""
            SELECT * FROM courses
            WHERE field = %s AND id NOT IN ({format_strings})
        """, [learner_field] + assigned_course_ids)
    else:
        cursor.execute("""
            SELECT * FROM courses WHERE field = %s
        """, (learner_field,))
    
    recommended_courses = cursor.fetchall()

    conn.close()
    return render_template('learner_dashboard.html',
                           assigned_courses=assigned_courses,
                           recommended_courses=recommended_courses)




@app.route('/recommended')
def recommended_courses():
    if 'user' not in session or session['user']['role'] != 'learner':
        return redirect('/login')

    learner_field = session['user']['field']
    learner_id = session['user']['id']

    conn = connect_db()
    cursor = conn.cursor(dictionary=True)

    # Get course_ids already assigned
    cursor.execute("SELECT course_id FROM assigned_courses WHERE learner_id = %s", (learner_id,))
    assigned_course_ids = [row['course_id'] for row in cursor.fetchall()]

    if assigned_course_ids:
        format_strings = ','.join(['%s'] * len(assigned_course_ids))
        cursor.execute(f"""
            SELECT * FROM courses
            WHERE field = %s AND id NOT IN ({format_strings})
        """, [learner_field] + assigned_course_ids)
    else:
        cursor.execute("SELECT * FROM courses WHERE field = %s", (learner_field,))
    
    courses = cursor.fetchall()
    conn.close()

    return render_template("recommended_courses.html", courses=courses)




@app.route('/course/<int:course_id>')
def course_detail(course_id):
    if 'user' not in session or session['user']['role'] != 'learner':
        return redirect('/login')

    conn = connect_db()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM courses WHERE id = %s", (course_id,))
    course = cursor.fetchone()
    conn.close()

    if not course:
        return "❌ Course not found."

    return render_template("course_detail.html", course=course)









# ...existing code...

# @app.route('/download_material/<filetype>/<filename>')
# def download_material(filetype, filename):
#     if 'user' not in session or session['user']['role'] != 'learner':
#         return redirect('/login')

#     valid_types = {'video': 'videos', 'document': 'documents', 'assignment': 'assignments'}
#     if filetype not in valid_types:
#         return "❌ Invalid file type", 400

#     folder = os.path.join('course_materials', valid_types[filetype])
#     filepath = os.path.join(folder, filename)

#     if not os.path.isfile(filepath):
#         return f"❌ File not found: {filepath}", 404

#     return send_from_directory(folder, filename, as_attachment=True)

@app.route('/download_material/<filetype>/<filename>')
def download_material(filetype, filename):
    if 'user' not in session:
        return redirect('/login')

    folder_map = {
        'video': 'videos',
        'document': 'documents',
        'assignment': 'assignment'
    }

    if filetype not in folder_map:
        return "❌ Invalid file type", 400

    folder = os.path.join('course_materials', folder_map[filetype])
    filepath = os.path.join(folder, filename)

    if not os.path.isfile(filepath):
        return f"❌ File not found: {filepath}", 404

    return send_from_directory(folder, filename)



# @app.route('/watch_video/<filename>')
# def watch_video(filename):
#     if 'user' not in session or session['user']['role'] != 'learner':
#         return redirect('/login')
#     return render_template('watch_video.html', filename=filename)
@app.route('/watch_video/<filename>')
def watch_video(filename):
    if 'user' not in session:
        return redirect('/login')
    return render_template('watch_video.html', filename=filename)

# @app.route('/video/<filename>')
# def serve_video(filename):
#     if 'user' not in session or session['user']['role'] != 'learner':
#         return redirect('/login')

    # folder = os.path.join('course_materials', 'videos')
    # filepath = os.path.join(folder, filename)

    # if not os.path.isfile(filepath):
    #     return f"❌ File not found: {filepath}", 404

    # return send_from_directory(folder, filename)

@app.route('/video/<filename>')
def serve_video(filename):
    if 'user' not in session:
        return redirect('/login')

    folder = os.path.join('course_materials', 'videos')  # Typo as per your folder
    filepath = os.path.join(folder, filename)

    if not os.path.isfile(filepath):
        return f"❌ File not found: {filepath}", 404

    return send_from_directory(folder, filename)




if __name__ == '__main__':
    app.run(debug=True)