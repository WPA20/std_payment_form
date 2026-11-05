
from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector

app = Flask(__name__)
app.secret_key = '1cde44dad35d95b240f542545c139234e60040d073eafec81ed120145f4ec82b'

db_config = {
    'host': 'mysql_db',
    'port': 3306,
    'user': 'root',
    'password': 'temp',
    'database': 'mysql_db'
}

@app.route('/', methods=['GET', 'POST'])
def student_form():

    if request.method == 'POST':

        name = request.form.get('Name', '').strip()
        class_name = request.form.get('Class', '').strip()
        amount = request.form.get('Amount', '').strip()
        address = request.form.get('Address', '').strip()
        payment = request.form.get('Payment', '').strip()
        contact = request.form.get('Contact', '').strip()

        if not all([name, class_name, amount, address, payment, contact]):
            flash("Please fill in all required fields.", "error")
            return redirect(url_for('student_form'))

        conn = None
        cursor = None

        try:
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor()

            query = """
                INSERT INTO std
                (Name, Class, Amount, Address, Payment, Contact)
                VALUES (%s, %s, %s, %s, %s, %s)
            """

            values = (
                name, class_name, amount,
                address, payment, contact
            )

            cursor.execute(query, values)
            conn.commit()

            flash("Data successfully saved to database!", "success")

        except Exception as e:
            app.logger.exception("Database error")
            flash(f"Database error: {str(e)}", "error")

        finally:
            if cursor is not None:
                cursor.close()

            if conn is not None and conn.is_connected():
                conn.close()

        return redirect(url_for('student_form'))

    return render_template('index.html')


@app.route('/test-flash')
def test_flash():
    flash("Flash message is working!", "success")
    return redirect(url_for('student_form'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
