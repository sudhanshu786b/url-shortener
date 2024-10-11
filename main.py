from flask import Flask, request, redirect, render_template
import pymysql
import random
import string

app = Flask(__name__)

# Database connection (assuming MySQL is set up)
def get_db_connection():
    return pymysql.connect(host='127.0.0.1',
                           user='root',
                           password='root@786$',
                           db='url_db',
                           port=3306,
                           cursorclass=pymysql.cursors.DictCursor)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        long_url = request.form.get('url')  # Get the URL from the form
        short_code = generate_short_code(long_url)  # Generate short code (to be implemented)
        save_to_db(long_url, short_code)  # Save to database (to be implemented)
        return f"Short URL: http://localhost:5001/{short_code}"
    return render_template('index.html')  # Simple HTML form

@app.route('/<short_code>')
def redirect_url(short_code):
    long_url = get_long_url(short_code)  # Retrieve long URL from DB (to be implemented)
    if long_url:
        return redirect(long_url)
    else:
        return "URL not found", 404

def generate_short_code(url):
    # Logic to generate short code
    return "abc321"  # Example code (to be improved later)

def save_to_db(long_url, short_code):
    connection = get_db_connection()
    with connection.cursor() as cursor:
        sql = "INSERT INTO urls (long_url, short_code) VALUES (%s, %s)"
        cursor.execute(sql, (long_url, short_code))
        connection.commit()

def get_long_url(short_code):
    connection = get_db_connection()
    with connection.cursor() as cursor:
        sql = "SELECT long_url FROM urls WHERE short_code = %s"
        cursor.execute(sql, (short_code,))
        result = cursor.fetchone()
        return result['long_url'] if result else None

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=5001)
