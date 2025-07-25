# Smart Learning & Development Platform
 
A comprehensive enterprise-level Learning and Development (L&D) platform built with Flask that enables organizations to manage training programs across multiple technical domains. The platform supports role-based access control for learners, instructors, and administrators.
 
## 🚀 Features
 
### 👨‍🎓 Learner Features
- **Personalized Dashboard**: View assigned courses by field of expertise
- **Multi-format Learning**: Access videos, documents, and assignments
- **Progress Tracking**: Mark courses as completed and track learning progress
- **Streaming Video Player**: In-browser video playback for training content
- **File Downloads**: Download documents and assignments for offline access
 
### 👨‍🏫 Instructor Features
- **Course Creation**: Create and upload training materials (videos, documents, assignments)
- **Content Management**: Edit, update, and delete course content
- **Multi-field Support**: Create courses for Software Engineering, AI/ML, and UI/UX domains
- **File Organization**: Automatic file organization by content type
 
### 👨‍💼 Admin Features
- **Course Assignment**: Assign specific courses to learners based on their field
- **Progress Monitoring**: Track learner progress and completion status
- **Field-based Management**: Manage learners and courses within specific domains
- **Assignment Oversight**: View all course assignments and their status
 
## 🛠️ Technology Stack
 
- **Backend**: Flask (Python)
- **Database**: MySQL
- **Frontend**: HTML5, CSS3, JavaScript
- **File Handling**: Werkzeug secure file uploads
- **Authentication**: Session-based authentication
- **Environment Management**: python-dotenv
 
## 📋 Prerequisites
 
- Python 3.8+
- MySQL Server
- Web browser (Chrome, Firefox, Safari, Edge)
 
## ⚙️ Installation
 
### 1. Clone the Repository
```bash
git clone <repository-url>
cd smart_ld_platform
```
 
### 2. Set Up Virtual Environment
```bash
python -m venv hackathon
# On Windows:
hackathon\Scripts\activate
# On macOS/Linux:
source hackathon/bin/activate
```
 
### 3. Install Dependencies
```bash
pip install -r requirements.txt
```
 
### 4. Database Setup
 
#### Create MySQL Database:
```sql
CREATE DATABASE lnd_platform;
USE lnd_platform;
 
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100) UNIQUE,
    password VARCHAR(100),
    role ENUM('learner', 'instructor', 'admin'),
    field ENUM('software engineer', 'AI/ML', 'ui-ux')
);
 
CREATE TABLE courses (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255),
    description TEXT,
    type ENUM('video', 'document', 'assignment'),
    field ENUM('software engineer', 'AI/ML', 'ui-ux'),
    filename VARCHAR(255),
    instructor_id INT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (instructor_id) REFERENCES users(id)
);
 
CREATE TABLE assigned_courses (
    id INT AUTO_INCREMENT PRIMARY KEY,
    learner_id INT,
    course_id INT,
    status ENUM('assigned', 'in-progress', 'completed') DEFAULT 'assigned',
    assigned_by INT,
    FOREIGN KEY (learner_id) REFERENCES users(id),
    FOREIGN KEY (course_id) REFERENCES courses(id),
    FOREIGN KEY (assigned_by) REFERENCES users(id)
);
```
 
### 5. Configuration
 
#### Update `config.py`:
```python
DB_HOST = "localhost"
DB_USER = "your_mysql_username"
DB_PASSWORD = "your_mysql_password"
DB_NAME = "lnd_platform"
```
 
#### Create `.env` file:
```env
SECRET_KEY=your_secret_key_here
```
 
### 6. Create Directory Structure
```bash
mkdir -p course_materials/videos
mkdir -p course_materials/documents
mkdir -p course_materials/assignments
mkdir -p uploads
```
 
## 🏃‍♂️ Running the Application
 
```bash
python app.py
```
 
The application will be available at `http://localhost:5000`
 
## 🎯 Usage Guide
 
### Getting Started
 
1. **Registration**: Visit `/register` to create an account
   - Choose your role: Learner, Instructor, or Admin
   - Select your field: Software Engineer, AI/ML, or UI/UX
 
2. **Login**: Use your credentials to access your dashboard
 
### For Instructors
 
1. **Create Course**: 
   - Fill in course title and description
   - Select course type (Video/Document/Assignment)
   - Choose target field
   - Upload course materials
 
2. **Manage Courses**: 
   - Edit existing courses
   - Delete courses
   - Update course materials
 
### For Admins
 
1. **Assign Courses**:
   - Select learner from your field
   - Choose appropriate course
   - Monitor assignment status
 
2. **Track Progress**:
   - View all assignments
   - Monitor completion rates
   - Manage field-specific content
 
### For Learners
 
1. **Access Courses**:
   - View assigned courses on dashboard
   - Download documents and assignments
   - Stream videos directly in browser
 
2. **Track Progress**:
   - Mark courses as completed
   - Monitor learning status
 
## 📁 Project Structure
 
```
smart_ld_platform/
├── app.py                      # Main Flask application
├── config.py                   # Database configuration
├── requirements.txt            # Python dependencies
├── .env                       # Environment variables
├── static/
│   └── style.css              # CSS styling
├── templates/                 # HTML templates
│   ├── register.html
│   ├── login.html
│   ├── learner_dashboard.html
│   ├── instructor_dashboard.html
│   ├── admin_dashboard.html
│   ├── edit_course.html
│   └── watch_video.html
├── course_materials/          # Organized course content
│   ├── videos/
│   ├── documents/
│   └── assignments/
└── uploads/                   # General file uploads
```
 
## 🔒 Security Features
 
- **Role-based Access Control**: Strict permission checking for all routes
- **Secure File Uploads**: Werkzeug secure filename handling
- **Session Management**: Secure user session handling
- **Field-based Isolation**: Users can only access content within their field
- **SQL Injection Prevention**: Parameterized queries
 
## 🌟 Key Features Highlights
 
### Multi-Domain Support
- **Software Engineering**: Programming courses, development methodologies
- **AI/ML**: Machine learning algorithms, data science training
- **UI/UX**: Design principles, user experience courses
 
### Content Types
- **Videos**: Streaming support with in-browser player
- **Documents**: PDF, Word, and other document formats
- **Assignments**: Interactive tasks and projects
 
### Progress Tracking
- Real-time status updates
- Completion tracking
- Administrative oversight
 
## 🚀 Future Enhancements
 
- **Assessment Module**: Quizzes and tests integration
- **Discussion Forums**: Learner interaction and collaboration
- **Analytics Dashboard**: Detailed learning analytics
- **Mobile Application**: Native mobile app support
- **Single Sign-On**: LDAP/Active Directory integration
- **Advanced Reporting**: Comprehensive progress reports
- **Content Versioning**: Version control for course materials
- **Notification System**: Email and in-app notifications
 
## 🐛 Troubleshooting
 
### Common Issues
 
1. **Database Connection Error**:
   - Verify MySQL server is running
   - Check database credentials in `config.py`
   - Ensure database exists
 
2. **File Upload Issues**:
   - Check directory permissions
   - Verify upload folders exist
   - Ensure sufficient disk space
 
3. **Template Not Found**:
   - Verify templates directory structure
   - Check template file names
 
4. **Session Issues**:
   - Ensure SECRET_KEY is set in `.env`
   - Clear browser cookies
 
## 📞 Support
 
For technical support or questions:
- Create an issue in the repository
- Contact the development team
- Check the troubleshooting section
 
## 📝 License
 
This project is licensed under the MIT License - see the LICENSE file for details.
 
## 👥 Contributing
 
1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request
 
## 🙏 Acknowledgments
 
- Flask community for the excellent web framework
- MySQL for robust database support
- All contributors and testers
 
---
 
**Built with ❤️ for enterprise learning and development**
