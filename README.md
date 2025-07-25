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

CREATE TABLE course (
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

CREATE TABLE assigned_course (
    id INT AUTO_INCREMENT PRIMARY KEY,
    learner_id INT,
    course_id INT,
    status ENUM('assigned', 'in-progress', 'completed') DEFAULT 'assigned',
    assigned_by INT,
    FOREIGN KEY (learner_id) REFERENCES users(id),
    FOREIGN KEY (course_id) REFERENCES course(id),
    FOREIGN KEY (assigned_by) REFERENCES users(id)
);


