# from flask_wtf import FlaskForm
# from wtforms import StringField, PasswordField, SubmitField, BooleanField
# from wtforms.validators import DataRequired, Length, Email, EqualTo
from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import keras
from keras.models import load_model
import numpy as np
import math
from flask import Flask, render_template, request, redirect, url_for, session, flash
from functools import wraps
from flask_mysqldb import MySQL
from tensorflow import keras
app = Flask(__name__)

app.secret_key = 'your secret key'

# Config MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'bank_database'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

# init MYSQL
mysql = MySQL(app)

def get_model():
    global model
    model = keras.models.load_model('ml/cnn.h5') 
    print("model loaded")



# home page 
@app.route('/')
def index():
    return render_template('index.html')





################# LOGIN - LOGOUT  RELATED ############################################################################################################
# login
@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email_given = request.form['email']
        password_given = request.form['password']

        cur = mysql.connection.cursor()

        result = cur.execute("SELECT * FROM `login` where email = %s", [email_given])
        result1 = cur.execute("SELECT * FROM `login_bank` where email = %s", [email_given])

        if result>0:
            result = cur.execute("SELECT * FROM `login` where email = %s", [email_given])
            data = cur.fetchone()

            
            password_db = data['password']

            if password_given == password_db:
                print("PASSWORD MATCHED!")
                session['logged_in'] = True
                session['email'] = email_given
                session['role'] = 'customer'
                session['bank_id'] = data['bank_id']
                return redirect(url_for('user'))

            else:
                print("PASSWORD NOT MATCHED!")
                error = 'Incorrect password!'
                return render_template('login.html', error = error)
            
        if result1>0:
            result1 = cur.execute("SELECT * FROM `login_bank` where email = %s", [email_given])
            data = cur.fetchone()
            password_db = data['password']
            if password_given == password_db:
                print("PASSWORD MATCHED!")
                session['logged_in'] = True
                session['email'] = email_given
                session['role'] = 'admin'
                
                return redirect(url_for('admin_dashboard'))

            else:
                print("PASSWORD NOT MATCHED!")
                error = 'Incorrect password!'
                return render_template('login.html', error = error)
        else:
            print("NO USER FOUND!")
            error = 'No user found for this email!'
            return render_template('login.html', error = error)

    return render_template('login.html')
# Check if user logged in
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, Please login', 'danger')
            return redirect(url_for('login'))
    return wrap

# logout 
@app.route('/logout') 
@is_logged_in
def logout():
    session.clear()
    flash('You are now logged out!', 'success')
    return redirect(url_for('login'))







#####################################################################################################################################################
################BANK ADMIN PART######################################################################################################################
#####################################################################################################################################################
#####################################################################################################################################################








######################################################################################################################################################





@app.route('/admin_dashboard')
@is_logged_in
def admin_dashboard():
    return render_template('admin_dashboard.html')







#####################################################################################################################################################












@app.route('/fetch_transactions')
@is_logged_in
def transactions_display():
    cur = mysql.connection.cursor()
    result = cur.execute(
    "SELECT * from transaction_details as t,user_details as u  where t.bank_id = u.bank_id ;")
    if result > 0:
        transactions = cur.fetchall()
        return render_template('fetch_transactions.html', transactions = transactions)
    else:
        msg = 'No transactions found!'
        return render_template('fetch_transactions.html', msg=msg)
    # Close connection
    cur.close()

@app.route('/transaction_details/<string:id>/')
@is_logged_in
def transaction_display(id):
    cur = mysql.connection.cursor()
    result = cur.execute(
    "SELECT * from transaction_details as t,repayment_status as r,bill_statement as b,previous_payment as p,user_details as u  where t.bank_id=u.bank_id and t.txn_id = r.txn_id and t.txn_id = b.txn_id and t.txn_id = p.txn_id and t.txn_id = %s;",(id,))
    if result > 0:
        transaction = cur.fetchone()
        return render_template('transaction_details.html', transaction = transaction)
    else:
        msg = 'Unable process request, try again later!'
        return render_template('transaction_details.html', msg=msg)
    # Close connection
    cur.close()










#####################################################################################################################################################










@app.route('/credibility_admin')
@is_logged_in
def eligibility():

        return render_template('credibility_admin.html')







###############neural network deployment part##################################



@app.route('/eligibilitycheck',methods=['GET', 'POST'])
@is_logged_in
def eligibilitycheck():
    if request.method == "POST":
        bank_id =request.form['bank_id']
        cur = mysql.connection.cursor()
        result = cur.execute(
        "SELECT * from transaction_details as t,repayment_status as r,bill_statement as b,previous_payment as p, user_details as u  where  t.txn_id = r.txn_id and t.txn_id = b.txn_id and t.txn_id = p.txn_id and t.bank_id = u.bank_id and t.bank_id = %s;",(bank_id))
        if result > 0:
            row = cur.fetchone()
            LIMIT_BAL= row['current_credit']
            pay_0 = row['pay_0']
            pay_2 = row['pay_2']
            pay_3 = row['pay_3']
            pay_4 = row['pay_4']
            pay_5 = row['pay_5']
            pay_6 = row['pay_6']
            bill_amt1 = row['bill_amt1']
            bill_amt2 = row['bill_amt2']
            bill_amt3 = row['bill_amt3']
            bill_amt4 = row['bill_amt4']
            bill_amt5 = row['bill_amt5']
            bill_amt6 = row['bill_amt6']
            pay_amt1 = row['pay_amt1']
            pay_amt2 = row['pay_amt2']
            pay_amt3 = row['pay_amt3']
            pay_amt4 = row['pay_amt4']
            pay_amt5 = row['pay_amt5']
            pay_amt6 = row['pay_amt6']
            SEX = row['sex']
            EDUCATION = row['education']
            MARRIAGE = row['marital_status']
            AGE = row['age']
            


            print('loading model')
            get_model()
            userdetails = [LIMIT_BAL,SEX,EDUCATION,MARRIAGE,AGE,pay_0,pay_2,pay_3,pay_4,pay_5,pay_6,bill_amt1,bill_amt2,bill_amt3,bill_amt4,bill_amt5,bill_amt6,pay_amt1,pay_amt2,pay_amt3,pay_amt4,pay_amt5,pay_amt6]
            ud = [float(i) for i in userdetails]
            prediction  = model.predict( np.array( [ud,] )  ).tolist()[0]
            print(prediction)

            a = []
            result =cur.execute("SELECT * from user_details where bank_id = %s ;", (bank_id))
            row = cur.fetchone()
            name= row['name']
            
            prediction=prediction[0]
            return render_template('credibility_result_admin.html',prediction = prediction,name = name, bank_id = bank_id)


    cur.close()



#####################################################################################################################################################




@app.route("/user_requests")
@is_logged_in
def user_requests():
            
        cur = mysql.connection.cursor()
        result =cur.execute("SELECT * FROM customer_request as c ,user_details as u where c.bank_id = u.bank_id")
        if result > 0:
            request = cur.fetchall()
            return render_template('user_request_display.html', requests = request)
        else:
            msg = 'No requests found!'
            return render_template('user_request_display.html', msg=msg)
        # Close connection
        cur.close()





@app.route('/request_details/<string:id>/')
@is_logged_in
def request_details(id):
    cur = mysql.connection.cursor()
    result =cur.execute("SELECT * FROM  customer_request as c, user_details as u where c.bank_id= u.bank_id  and c.request_id = %s" ,[id])
    print(result)
    if result > 0:
        details = cur.fetchone()
        bank_id = details['bank_id']
        result1 = cur.execute(
        "SELECT * from transaction_details as t,repayment_status as r,bill_statement as b,previous_payment as p, user_details as u  where  t.txn_id = r.txn_id and t.txn_id = b.txn_id and t.txn_id = p.txn_id and t.bank_id = u.bank_id and t.bank_id = %s;",[bank_id])
        txn_details = cur.fetchone()

        if details['credibility'] == 0:
             result2 =cur.execute("SELECT * FROM  credit_approval where request_id = %s" ,[id])
             print(result2)
             if result2 >0:
                
                credit_approval_details = cur.fetchone()
                return render_template('request_details.html', user_request = details, txn_details = txn_details , credit_approval_details = credit_approval_details , flag =0)
             else:
                 return render_template('request_details.html', user_request = details, txn_details = txn_details, flag= 1)
                
        else:
            return render_template('request_details.html', user_request = details, txn_details = txn_details, flag= 1)


        
    else:
        msg = 'No'
        return render_template('request_details.html', msg=msg)

    cur.close()


######################################################################################################################################################

@app.route('/customer_info')
@is_logged_in
def customer_info():
    cur = mysql.connection.cursor()
    result = cur.execute("SELECT * from user_details")
    if result > 0:
        customers = cur.fetchall()
        return render_template('customers_display.html', customers = customers)
    else:
        return render_template('customers_display.html', msg = 'no customers found')








####################################################################################################################################################
####################################################################################################################################################
#########USER PART##################################################################################################################################
####################################################################################################################################################
####################################################################################################################################################



#####################################################################################################################################################


@app.route("/user_dashboard")
@is_logged_in
def user():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * from  user_details where  bank_id = %s" ,(str(session['bank_id'])),)
    row = cur.fetchone() 
   


    
    return render_template('user_dashboard.html' ,row = row)
    


#####################################################################################################################################################

# home page 
@app.route('/aboutus')
def about():
    return render_template('about_us.html')

#####################################################################################################################################################



@app.route("/transaction")
@is_logged_in
def transaction_history():
            
        cur = mysql.connection.cursor()
        result =cur.execute("SELECT * from transaction_details as t,repayment_status as r,bill_statement as b,previous_payment as p, user_details as u  where  t.txn_id = r.txn_id and t.txn_id = b.txn_id and t.txn_id = p.txn_id and t.bank_id = %s" ,(str(session['bank_id'])),)
        print(result)
        print("B")
        if result > 0:
            transactions = cur.fetchone()
            return render_template('transaction.html', transaction = transactions)
            print(transaction)
            print("A")
        else:
            msg = 'No transactions found!'
            return render_template('transaction.html', msg=msg)
        # Close connection
        cur.close()







######################################################################################################################################################






@app.route("/request_history")
@is_logged_in
def request_history():
            
        cur = mysql.connection.cursor()
        result =cur.execute("SELECT * FROM customer_request where bank_id = %s" ,(str(session['bank_id'])),)
        if result > 0:
            history = cur.fetchall()
            return render_template('request_history.html', history = history )
        else:
            msg = 'No requests found!'
            return render_template('request_history.html', msg=msg)
        # Close connection
        cur.close()




@app.route('/request_history_details/<string:id>/')
@is_logged_in
def request_history_details(id):
    cur = mysql.connection.cursor()
    result =cur.execute("SELECT * FROM credit_approval where  request_id = %s",[id])
    print(result)
    if result > 0:
        details = cur.fetchone()
        return render_template('request_history_details.html', details = details)
    else:
        msg = 'No'
        return render_template('request_history_details.html', msg=msg)

    cur.close()





#####################################################################################################################################################






@app.route("/req_verification", methods=['GET','POST'])
@is_logged_in
def req_verification():
    if request.method == 'POST' :
        cur = mysql.connection.cursor()
        result = cur.execute("SELECT * FROM `login` where bank_id = %s", (str(session['bank_id'])),)
        row = cur.fetchone()  
        if row['password'] == request.form['password']:
            return redirect(url_for('requestinfo'))
        else:
            msg = 'Wrong password'
            return render_template('customer_request.html', msg=msg)
    
    return render_template('customer_request.html')










#####################################################################################################################################################










@app.route("/requestinfo",methods=['GET', 'POST'])
@is_logged_in
def requestinfo():
    
        cur = mysql.connection.cursor()
        cur.execute("SELECT * from transaction_details as t,repayment_status as r,bill_statement as b,previous_payment as p, user_details as u  where  t.txn_id = r.txn_id and t.txn_id = b.txn_id and t.txn_id = p.txn_id and t.bank_id = u.bank_id and u.bank_id = %s" ,(str(session['bank_id'])),)
        row = cur.fetchone()
        txn_id =row['txn_id']  
        bank_id = row['bank_id']
        LIMIT_BAL= row['current_credit']
        pay_0 = row['pay_0']
        pay_2 = row['pay_2']
        pay_3 = row['pay_3']
        pay_4 = row['pay_4']
        pay_5 = row['pay_5']
        pay_6 = row['pay_6']
        bill_amt1 = row['bill_amt1']
        bill_amt2 = row['bill_amt2']
        bill_amt3 = row['bill_amt3']
        bill_amt4 = row['bill_amt4']
        bill_amt5 = row['bill_amt5']
        bill_amt6 = row['bill_amt6']
        pay_amt1 = row['pay_amt1']
        pay_amt2 = row['pay_amt2']
        pay_amt3 = row['pay_amt3']
        pay_amt4 = row['pay_amt4']
        pay_amt5 = row['pay_amt5']
        pay_amt6 = row['pay_amt6']

        
        SEX = row['sex']
        EDUCATION = row['education']
        MARRIAGE = row['marital_status']
        AGE = row['age']
        
        print('loading model')
        get_model()
        userdetails = [LIMIT_BAL,SEX,EDUCATION,MARRIAGE,AGE,pay_0,pay_2,pay_3,pay_4,pay_5,pay_6,bill_amt1,bill_amt2,bill_amt3,bill_amt4,bill_amt5,bill_amt6,pay_amt1,pay_amt2,pay_amt3,pay_amt4,pay_amt5,pay_amt6]
        ud = [float(i) for i in userdetails]
        prediction  = model.predict( np.array( [ud,] )  ).tolist()[0]

        cur = mysql.connection.cursor()
        if prediction[0]>=0.5:
            cur.execute("INSERT INTO customer_request(bank_id,txn_id,credibility) VALUES (%s,%s,%s)", (bank_id,txn_id,1))
            mysql.connection.commit()
            cur.close()
            print('success pos')
        else:
            cur.execute("INSERT INTO customer_request(bank_id,txn_id,credibility) VALUES (%s,%s,%s)", (bank_id,txn_id,0))
            mysql.connection.commit()
            cur.close()
            print('success neg')
        cur = mysql.connection.cursor()
        cur.execute("SELECT * from  user_details where  bank_id = %s" ,(str(session['bank_id'])),)
        row = cur.fetchone() 
       
        
        name   = row['name']
        
        return render_template('credibility_result.html',credibility = prediction[0] , name = name)












#######################################################################################################################################################











@app.route("/approval",methods=['GET', 'POST'])
@is_logged_in
def approval():
    prediction=[]
    if request.method == 'POST' :
        cur = mysql.connection.cursor()
        cur.execute("SELECT * from  user_details where  bank_id = %s" ,(str(session['bank_id'])),)
        row = cur.fetchone() 
        marital_status = row['marital_status']
        if marital_status == 2 or marital_status == 3:
            Married = 0
        else:
            Married = 1

        education = row['education']
        if education == 5 or education == 7:
            Education = 0
        else:
            Education = 1
        a = []
        name = row['name']
        Gender = row['sex']

        Income = request.form['Income']
        Coapplicant_Income = request.form['Coapplicant_Income']
        
        
        Dependent = request.form['Dependent']
        Self_Employed = request.form['Self_Employed']
        Credit_Amount = request.form['Credit_Amount']
        
        model1 = keras.models.load_model('ml/Credit_approval.h5') 
        userdetails = [Gender,Married,Dependent,Education,Self_Employed,Income,Coapplicant_Income,Credit_Amount,360,1]
        ud = [float(i) for i in userdetails]
        prediction  = model1.predict( np.array( [ud,] )  ).tolist()[0]
        print(prediction)


        cur.execute("SELECT * from customer_request where bank_id= %s order by rcreate_at DESC" ,(str(session['bank_id'])),)
        row = cur.fetchone()
        request_id=row['request_id']
        cur = mysql.connection.cursor()
        if prediction[0]>=0.5:
            cur.execute("INSERT INTO credit_approval(bank_id,request_id,dependent,self_employed,applicant_income,coapplicant_income,requested_credit,approved) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)", (str(session['bank_id']),request_id,Dependent,Self_Employed,Income,Coapplicant_Income,Credit_Amount,1))
            mysql.connection.commit()
            cur.close()
            print('success pos')
        else:
            cur.execute("INSERT INTO credit_approval(bank_id,request_id,dependent,self_employed,applicant_income,coapplicant_income,requested_credit,approved) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)", (str(session['bank_id']),request_id,Dependent,Self_Employed,Income,Coapplicant_Income,Credit_Amount,1))
            mysql.connection.commit()
            cur.close()
            print('success neg')


        a.append(Credit_Amount)
        a.append(prediction[0])
        print  (a)
        return render_template('limit_approval.html',prediction = prediction[0], credit_amount =Credit_Amount , name = name)
    return render_template('index.html')















#####################################################################################################################################################
#####################################################################################################################################################
#####################################################################################################################################################
#####################################################################################################################################################
# starting point of execution

if __name__ == '__main__':
    app.run(host='localhost', port='5000',debug=True)