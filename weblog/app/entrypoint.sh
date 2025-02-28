#!/bin/bash

set -e

DB_INIT_FLAG="/var/lib/mysql/.db_initialized"
FLASK_PORT=5000

initialize_mariadb() {
    if [ ! -d "/var/lib/mysql/mysql" ]; then
        echo "Initializing MariaDB data directory..."
        mysql_install_db --user=mysql --ldata=/var/lib/mysql
    else
        echo "MariaDB data directory already initialized."
    fi
}

start_mariadb() {
    echo "Starting MariaDB..."
    mysqld_safe --datadir=/var/lib/mysql &
    sleep 5
}

initialize_database() {
    if [ ! -f "$DB_INIT_FLAG" ]; then
        echo "Setting up database and user..."
        mysql -uroot <<EOF
CREATE DATABASE IF NOT EXISTS ${MYSQL_DATABASE};
CREATE USER IF NOT EXISTS 'flaskuser'@'localhost' IDENTIFIED BY 'flaskpassword';
GRANT ALL PRIVILEGES ON ${MYSQL_DATABASE}.* TO 'flaskuser'@'localhost';
FLUSH PRIVILEGES;

USE ${MYSQL_DATABASE};
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    role ENUM('user', 'admin') DEFAULT 'user'
);

CREATE TABLE IF NOT EXISTS blog_posts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    content TEXT NOT NULL,
    author VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert users and blog posts
INSERT IGNORE INTO users (username, password, email, role)
VALUES 
('admin', MD5('admin_password'), 'admin@example.com', 'admin'),
('user1', MD5('user_password'), 'user1@example.com', 'user');

INSERT IGNORE INTO blog_posts (title, content, author)
VALUES
('Example', 'Example post', 'admin');
EOF
        touch "$DB_INIT_FLAG"
        echo "Database setup completed."
    else
        echo "Database already initialized. Skipping setup."
    fi
}

check_port() {
    echo "Checking if port $FLASK_PORT is in use..."
    if lsof -i:"$FLASK_PORT" -t > /dev/null 2>&1; then
        echo "Port $FLASK_PORT is in use. Attempting to kill the conflicting process..."
        lsof -i:"$FLASK_PORT" -t | xargs kill -9 || true
        echo "Conflicting process terminated. Continuing..."
    else
        echo "Port $FLASK_PORT is free."
    fi
}

start_flask() {
    echo "Starting Flask app on port $FLASK_PORT..."
    exec python app.py --host=0.0.0.0 --port="$FLASK_PORT"
}

main() {
    initialize_mariadb
    start_mariadb
    initialize_database
    check_port
    start_flask
}

main
