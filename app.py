import os
from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
import psycopg2
from dotenv import load_dotenv

app = Flask(__name__)
load_dotenv()


def connect_to_db():
    conn = psycopg2.connect(
        dbname=os.environ.get("DB_NAME"),
        user=os.environ.get("DB_USER"),
        password=os.environ.get("DB_PASSWORD"),
        host=os.environ.get("DB_HOST"),
        port=os.environ.get("DB_PORT")
    )
    return conn

# Format the current date and time in 12-hour format
@app.route('/')
def hello_world():
   return render_template('index.html')

@app.route('/Products')
def Products():
    return render_template('Products.html')

@app.route('/Square', methods=['GET'])
def squarenumber():
    
    # If method is GET, check if  number is entered 
    # or user has just requested the page.
    # Calculate the square of number and pass it to 
    # answermaths method
    if request.method == 'GET':
        # If 'num' is None, the user has requested page the first time
        if request.args.get('num') == None:
            return render_template('squarenum.html')
        # If user clicks on Submit button without 
        # entering number display error
        elif request.args.get('num') == '':
            emptynum = "PLEASE ENTER SOMETHING!!!"
            return render_template('error.html', error=emptynum)
        elif not request.args.get('num').isdigit():
            notnum = "PLEASE ENTER A VALID NUMBER :("
            return render_template('error.html', error=notnum)
        else:
            # User has entered a number
            # Fetch the number from args attribute of 
            # request accessing its 'id' from HTML
            number = request.args.get('num')
            sq = int(number) * int(number)
            # pass the result to the answer HTML
            # page using Jinja2 template
            return render_template('answer.html', squareofnum=sq, num=number)

# Route for handling the form submission and inserting todo into database
@app.route('/add_todo', methods=['POST'])
def add_todo():
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')  # Ensure this matches the column name in your database

        if not title or not description:
            return render_template('error.html', error="Please enter both title and description.")

        conn = connect_to_db()
        cur = conn.cursor()

        try:
            now = datetime.now()
            Date_now = now.strftime("%d/%m/%Y %I:%M:%S %p")
            cur.execute("INSERT INTO alltodos (title, description, date_created) VALUES (%s, %s, %s)", (title, description, Date_now))
            conn.commit()
        
            success = "The todo has been added to the database successfully."
        except Exception as e:
            error = f"An error occurred: {str(e)}"
            return render_template('error.html', error=error)
        finally:
            conn.close()

        return redirect(url_for('MyTodos'))  # Redirect to the todos route after adding a todo

@app.route('/add_todo', methods=['GET'])
def add_todo1():
    return render_template('Todo.html')

@app.route('/Delete/<int:SrNo>')
def Delete(SrNo):
    conn = connect_to_db()
    cur = conn.cursor()
    try:
        cur.execute("DELETE FROM alltodos WHERE \"SrNo\" = (%s)", (SrNo,))
        conn.commit()
    except Exception as e:
        error = f"An error occurred: {str(e)}"
        return render_template('error.html', error=error)
    finally:
        conn.close()

    return redirect(url_for('MyTodos'))

@app.route('/Update/<int:SrNo>')
def Update(SrNo):
    conn = connect_to_db()
    cur = conn.cursor()
    try:
        cur.execute("DELETE FROM alltodos WHERE \"SrNo\" = (%s)", (SrNo,))
        conn.commit()
    except Exception as e:
        error = f"An error occurred: {str(e)}"
        return render_template('error.html', error=error)
    finally:
        conn.close()

    return redirect(url_for('MyTodos'))
    

# Route for displaying todos
@app.route('/MyTodos')
def MyTodos():
    conn = connect_to_db()
    cur = conn.cursor()

    try:
        cur.execute("SELECT * FROM alltodos")
        todos = cur.fetchall()
    except Exception as e:
        error = f"An error occurred: {str(e)}"
        return render_template('error.html', error=error)
    finally:
        conn.close()

    return render_template('MyTodos.html', todos=todos)

if __name__ == '__main__':
    app.run(debug=True)
