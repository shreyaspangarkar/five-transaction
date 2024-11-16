from flask import Flask, request, render_template
import mysql.connector


app = Flask(__name__)

# Database configuration
DB_CONFIG = {
    'host': 'localhost',          # Your MySQL server host
    'user': 'monsterzero',        # Your MySQL user
    'password': 'Monsterzero@8910', # Your MySQL password
    'database': 'dbrs',           # Your MySQL database name
    'port': 3306                  # MySQL default port
}

@app.route('/')
def index():
    # Render the form with all sections
    return render_template('form.html')

@app.route('/submit1', methods=['POST'])
def handle_submit1():
    id_param = request.form['id']
    date_from = request.form['date_from']
    date_to = request.form['date_to']
    
    query1 = """
        SELECT TRAN_DATE, TRAN_ID, account_name,
               DR_AMT AS total_debit, CR_AMT AS total_credit
        FROM detail_member_trans a
        LEFT JOIN mast_account b ON a.acc_id = b.account_id
        WHERE tran_date >= %s AND tran_date <= %s AND mbr_id = %s
        ORDER BY tran_date, tran_ID;
    """

    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cur = conn.cursor()
        cur.execute(query1, (date_from, date_to, id_param))
        results1 = cur.fetchall()
        
        cur.close()
        conn.close()

        return render_template('result.html', results1=results1)

    except mysql.connector.Error as err:
        return f"An error occurred: {err}"

@app.route('/submit2', methods=['POST'])
def handle_submit2():
    date_from = request.form['date_from']
    date_to = request.form['date_to']
    
    query2 = """
        SELECT tran_date, tran_id, C.member_name, account_name,
               dr_amt, cr_amt 
        FROM detail_member_trans a
        LEFT JOIN mast_account B ON a.acc_id = B.account_id
        LEFT JOIN mast_member C ON a.mbr_id = C.member_id
        WHERE tran_date >= %s AND tran_date <= %s
        ORDER BY tran_date, tran_ID;
    """

    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cur = conn.cursor()
        cur.execute(query2, (date_from, date_to))
        results2 = cur.fetchall()
        cur.close()
        conn.close()

        return render_template('result.html', results2=results2)

    except mysql.connector.Error as err:
        return f"An error occurred: {err}"

@app.route('/submit3', methods=['POST'])
def handle_submit3():
    date_from = request.form['date_from']
    date_to = request.form['date_to']
    
    query3 = """
        SELECT a.tran_date, a.tran_id, a.tran_sr_id, b.account_name, a.dr_amt, a.cr_amt
        FROM journal_entries a
        LEFT JOIN mast_account b ON a.account_id = b.account_id
        WHERE a.tran_date >= %s AND a.tran_date <= %s
        ORDER BY a.tran_date, a.tran_id;
    """

    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cur = conn.cursor()
        cur.execute(query3, (date_from, date_to))
        results3 = cur.fetchall()
        cur.close()
        conn.close()

        return render_template('result.html', results3=results3)

    except mysql.connector.Error as err:
        return f"An error occurred: {err}"
    
@app.route('/submit4' ,methods=['POST'])
def handle_submit4():
    account_id_param = request.form['account_id']
    date_from = request.form['date_from']
    date_to = request.form['date_to']

    query4 = """
        SELECT a.tran_date, a.tran_id, a.tran_sr_id, b.account_name, a.dr_amt, a.cr_amt
            FROM journal_entries a
        LEFT JOIN mast_account b ON a.account_id = b.account_id
        WHERE a.tran_date >= %s AND 
        a.tran_date <= %s AND 
        a.account_id = %s
        ORDER BY a.tran_date, a.tran_id;
    """

    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cur = conn.cursor()
        cur.execute(query4 , (date_from, date_to, account_id_param))
        results4 = cur.fetchall()
        cur.close()
        conn.close()

        return render_template('result.html', results4=results4)
    
    except mysql.connector.Error as err:
        return f"An error occurred: {err}"


#################################################################
@app.route('/submit5', methods=['GET', 'POST'])
def handle_submit5():
    if request.method == 'POST':
        loan_type = request.form.get('loan_type')
        meeting_date_from = request.form.get('meeting_date_from')
        meeting_date_to = request.form.get('meeting_date_to')

        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor(dictionary=True)

        query = """
            SELECT 
                a.member_id, b.member_name,
                LOWER(b.gaurdian_relation) AS gaurdian_relation, b.gaurdian_name,
                a.loan_id, a.loan_amount, a.app_loan_amt,
                a.adj_loan_amt, a.loan_date,
                a.member_id AS surity1_id, b.member_name AS surity1_name,
                a.member_id AS surity2_id, b.member_name AS surity2_name,
                a.member_id AS surity3_id, b.member_name AS surity3_name,
                a.member_id AS surity4_id, b.member_name AS surity4_name
            FROM mast_loan a
            JOIN mast_member b ON a.member_id = b.member_id
            WHERE a.canceled = 0
              AND a.loan_type = %s
              AND a.meating_date >= %s
              AND a.meating_date < %s
            ORDER BY a.member_id
        """
    
        cursor.execute(query, (loan_type, meeting_date_from, meeting_date_to))
        results5 = cursor.fetchall()

        cursor.close()
        connection.close()

        return render_template('result.html', results5=results5)
        
    
#############################################################

if __name__ == '__main__':
    app.run(debug=True)
















