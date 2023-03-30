from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
from datetime import datetime
from dbconfig import cnx

app = Flask(__name__)

@app.route('/')
def index():
    return redirect(url_for('member_list'))

@app.route('/member/add', methods=['GET', 'POST'])
def member_add():
    if request.method == 'POST':
        name = request.form['name']
        phone_number = request.form['phone_number']
        address = request.form['address']
        if not name:
            return render_template('member_add.html', error_message='名前は必須です。')
        # データベースに追加する
        cursor = cnx.cursor()
        query = "INSERT INTO members (name, phone_number, address) VALUES (%s, %s, %s)"
        data = (name, phone_number, address)
        cursor.execute(query, data)
        cnx.commit()
        cursor.close()
        return redirect(url_for('member_list'))
    else:
        return render_template('member_add.html')

@app.route('/member')
def member_list():
    # データベースから取得する
    cursor = cnx.cursor(dictionary=True)
    query = "SELECT * FROM members"
    cursor.execute(query)
    members = cursor.fetchall()
    cursor.close()
    return render_template('member_list.html', members=members)

@app.route('/payment')
def payment_list():
    # データベースから取得する
    cursor = cnx.cursor(dictionary=True)
    query = """
    SELECT payments.id, members.name, payments.paid_at
    FROM payments
    INNER JOIN members
    ON payments.member_id = members.id
    ORDER BY payments.paid_at DESC
    """
    cursor.execute(query)
    payments = cursor.fetchall()
    cursor.close()
    return render_template('payment_list.html', payments=payments)

@app.route('/payment/add', methods=['GET', 'POST'])
def payment_add():
    if request.method == 'POST':
        member_id = request.form['member_id']
        paid_at = datetime.now()
        # データベースに追加する
        cursor = cnx.cursor()
        query = "INSERT INTO payments (member_id, paid_at) VALUES (%s, %s)"
        data = (member_id, paid_at)
        cursor.execute(query, data)
        cnx.commit()
        cursor.close()
        return redirect(url_for('payment_list'))
    else:
        # メンバーのリストを取得する
        cursor = cnx.cursor(dictionary=True)
        query = "SELECT * FROM members"
        cursor.execute(query)
        members = cursor.fetchall()
        cursor.close()
        return render_template('payment_add.html', members=members)

if __name__ == '__main__':
    app.run(debug=True)
