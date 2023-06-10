from flask import Flask, render_template,request,redirect
from flask_mysqldb import MySQL
from datetime import date
app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PORT'] = 3306
app.config['MYSQL_PASSWORD'] = 'mysqlloginword'
app.config['MYSQL_DB'] = 'hospitaldb'

mysql = MySQL(app)


@app.route('/')
def Home_page():
    return render_template('home.html')

@app.route('/loginasadmin')
def loginasadmin():
    return render_template('adminloginform.html',Flag=True)

@app.route('/loginaspatient')
def loginaspatient():
    return render_template('home.html')

@app.route('/loginasdoctor')
def loginasdoctor():
    return render_template('home.html')

# ------- To Add -------------------------

@app.route('/AddDocInfo',methods=["GET","POST"])
def AddDocInfo():
    cur = mysql.connection.cursor()
    flag = '**'
    if request.method=="POST":
        # print('******')
        doc_name = request.form["name"]
        joindate = request.form["JoinDate"]
        Phno = request.form["phno"]
        Depart = request.form["depspec"]

        cur.execute('''SELECT Specialization_id FROM Specialization;''')
        if Depart not in [ele[0] for ele in list(cur)]:
            flag = '*****'
        else:
            cur.execute('''SELECT doctor FROM Count_Total;''')
            temp = list(cur)[0][0]
            id = "Do@"+str(temp+1)
            cur.execute('''INSERT INTO Doctors VALUES(%s,%s,%s,%s,%s);''',(id,doc_name,Phno,joindate,Depart))
            cur.execute('''UPDATE Count_Total SET doctor = %s WHERE Sno = 1;''',(temp+1,))
            cur.execute('''commit;''')
    
    cur.execute('''SELECT * FROM Doctors;''')
    DocInfo = list(cur)
    cur.close()
    return render_template('adddoctors.html',todo=DocInfo,Flag=flag)

@app.route('/AddPatInfo',methods=["GET","POST"])
def AddPatInfo():
    cur = mysql.connection.cursor()
    if request.method=="POST":
        p_name = request.form["name"]
        dob = request.form["DateOfBirth"]

        birthday = date(int(dob[0:4]),int(dob[5:7]),int(dob[8:]))
        today = date.today()
        oneORzero = ((today.month,today.day)<(birthday.month,birthday.day))
        yeardiff = today.year - birthday.year
        age = yeardiff - oneORzero

        gender = request.form["gender"]
        Phno = request.form["phno"]

        cur.execute('''SELECT patient FROM Count_Total;''')
        temp = list(cur)[0][0]
        id = "Pa@"+str(temp+1)

        cur.execute('''INSERT INTO Patients VALUES(%s,%s,%s,%s,%s,%s);''',(id,p_name,dob,age,gender,Phno))
        cur.execute('''UPDATE Count_Total SET patient = %s WHERE Sno = 1;''',(temp+1,))
        cur.execute('''commit;''')
    
    cur.execute('''SELECT * FROM Patients;''')
    PatientInfo = list(cur)
    cur.close()
    return render_template('addpatients.html',todo=PatientInfo)

@app.route('/AddDepInfo',methods=["GET","POST"])
def AddDepInfo():
    cur = mysql.connection.cursor()
    if request.method=="POST":
        dep_name = request.form["name"]

        cur.execute('''SELECT spec FROM Count_Total;''')
        temp = list(cur)[0][0]
        id = "Sp@"+str(temp+1)

        cur.execute('''INSERT INTO Specialization VALUES(%s,%s);''',(id,dep_name))
        cur.execute('''UPDATE Count_Total SET spec = %s WHERE Sno = 1;''',(temp+1,))
        cur.execute('''commit;''')
    cur.execute('''SELECT * FROM Specialization;''')
    DepInfo = list(cur)
    cur.close()
    return render_template('adddepartments.html',todo = DepInfo)

@app.route('/AddAppInfo',methods=["GET","POST"])
def AddAppInfo():
    cur = mysql.connection.cursor()
    flag = '**'
    if request.method=="POST":
        patientid = request.form["patid"]
        doctorid = request.form["docid"]

        cur.execute('''SELECT Patient_id FROM Patients;''')
        pats = list(cur)
        cur.execute('''SELECT Doctor_id FROM Doctors;''')
        docs = list(cur)
        if(patientid not in [ele[0] for ele in pats]) or (doctorid not in [ele[0] for ele in docs]):
            flag = '*****'
        else:
            cur.execute('''SELECT appl from Count_Total;''')
            temp = list(cur)[0][0]
            id = "Ap@"+str(temp+1)
            cur.execute('''INSERT INTO Appointments VALUES(%s,%s,%s);''',(id,patientid,doctorid))
            cur.execute('''UPDATE Count_Total SET appl = %s WHERE Sno = 1;''',(temp+1,))
            cur.execute('''commit;''')

    cur.execute('''SELECT * FROM Appointments;''')
    appinfo = list(cur)
    cur.close()
    return render_template('addappointments.html',todo = appinfo,Flag = flag)

# -------------------------------------------

@app.route('/adminloginform',methods=["GET","POST"])
def adminloginform():
    
    # here got the values from the table -----
    cur = mysql.connection.cursor()
    cur.execute('''SELECT * FROM Registration_Admin;''')
    result = list(cur)
    mysql.connection.commit()
    cur.close()

    for ele in result:
        if ele == (request.form["AdminID"],request.form["AdminPassword"]):
            return render_template('adminauthority.html')
    
    return render_template('adminloginform.html',Flag=False)

# --------------- To Update ------------------------ 

@app.route('/Updatepatient/<id>',methods=["GET","POST"])
def Updatepatient(id):
    cur = mysql.connection.cursor()
    if request.method=="POST":

        dob = request.form['DateOfBirth']
        birthday = date(int(dob[0:4]),int(dob[5:7]),int(dob[8:]))
        today = date.today()
        oneORzero = ((today.month,today.day)<(birthday.month,birthday.day))
        yeardiff = today.year - birthday.year
        age = yeardiff - oneORzero

        cur.execute('''UPDATE Patients SET Pat_name = %s WHERE Patient_id = %s;''',(request.form['name'],id))
        cur.execute('''UPDATE Patients SET Birthday = %s WHERE Patient_id = %s;''',(dob,id))
        cur.execute('''UPDATE Patients SET Gender = %s WHERE Patient_id = %s;''',(request.form['gender'],id))
        cur.execute('''UPDATE Patients SET Ph_num = %s WHERE Patient_id = %s;''',(request.form['phno'],id))
        cur.execute('''UPDATE Patients SET Age = %s WHERE Patient_id = %s;''',(age,id))
        cur.execute('''commit;''')
        cur.execute('''SELECT * FROM Patients;''')
        PatientInfo = list(cur)
        cur.close()
        return render_template('addpatients.html',todo=PatientInfo)
            
    cur.execute('''SELECT * FROM Patients WHERE Patient_id = %s''',(id,))
    result = list(cur)[0]
    cur.close()
    return render_template('updatepatient.html',todo=result)

@app.route('/Updatedepartment/<id>',methods=["GET","POST"])
def Updatedepartment(id):
    cur = mysql.connection.cursor()
    if request.method=="POST":
        cur.execute('''UPDATE Specialization SET Spec_name = %s WHERE Specialization_id = %s;''',(request.form['name'],id))
        cur.execute('''commit;''')
        cur.execute('''SELECT * FROM Specialization;''')
        SpecInfo = list(cur)
        cur.close()
        return render_template('adddepartments.html',todo=SpecInfo)
            
    cur.execute('''SELECT * FROM Specialization WHERE Specialization_id = %s''',(id,))
    result = list(cur)[0]
    cur.close()
    return render_template('updatedepartment.html',todo=result)

@app.route('/Updatedoctor/<id>',methods=["GET","POST"])
def Updatedoctor(id):
    cur = mysql.connection.cursor()
    if request.method=="POST":
        DeptId = request.form['dept']
        cur.execute('''SELECT Specialization_id FROM Specialization;''')
        specids = list(cur)
        if DeptId not in [ele[0] for ele in specids]:
            cur.execute('''SELECT * FROM Doctors WHERE Doctor_id = %s''',(id,))
            result = list(cur)[0]
            cur.close()
            return render_template('updatedoctor.html',todo=result,Flag=False)
        else:
            cur.execute('''UPDATE Doctors SET Doc_name = %s WHERE Doctor_id = %s;''',(request.form['name'],id))
            cur.execute('''UPDATE Doctors SET Ph_num = %s WHERE Doctor_id = %s;''',(request.form['phno'],id))
            cur.execute('''UPDATE Doctors SET Joining_date = %s WHERE Doctor_id = %s;''',(request.form['joid'],id))
            cur.execute('''UPDATE Doctors SET spec_id = %s WHERE Doctor_id = %s;''',(request.form['dept'],id))
            cur.execute('''commit;''')
            cur.execute('''SELECT * FROM Doctors;''')
            DocInfo = list(cur)
            cur.close()
            return render_template('adddoctors.html',todo=DocInfo)
            
    cur.execute('''SELECT * FROM Doctors WHERE Doctor_id = %s''',(id,))
    result = list(cur)[0]
    cur.close()
    return render_template('updatedoctor.html',todo=result,Flag=True)

@app.route('/Updateappointment/<id>',methods=["GET","POST"])
def Updateappointment(id):
    cur = mysql.connection.cursor()
    if request.method=="POST":
        patientId = request.form['pid']
        doctorId = request.form['did']
        cur.execute('''SELECT Patient_id FROM Patients;''')
        patids = list(cur)
        cur.execute('''SELECT Doctor_id FROM Doctors;''')
        docids = list(cur)
        if patientId not in [ele[0] for ele in patids] or doctorId not in [ele[0] for ele in docids]:
            cur.execute('''SELECT * FROM Appointments WHERE Appointment_id = %s''',(id,))
            result = list(cur)[0]
            cur.close()
            return render_template('updateappointment.html',todo=result,Flag=False)
        else:
            cur.execute('''UPDATE Appointments SET pat_id = %s WHERE Appointment_id = %s;''',(patientId,id))
            cur.execute('''UPDATE Appointments SET doc_id = %s WHERE Appointment_id = %s;''',(doctorId,id))
            cur.execute('''commit;''')
            cur.execute('''SELECT * FROM Appointments;''')
            AppInfo = list(cur)
            cur.close()
            return render_template('addappointments.html',todo=AppInfo)
            
    cur.execute('''SELECT * FROM Appointments WHERE Appointment_id = %s''',(id,))
    result = list(cur)[0]
    cur.close()
    return render_template('updateappointment.html',todo=result,Flag=True)
# --------------------------------------------------------------------------------
# ----------------------------- To Delete ----------------------------------------

@app.route('/Deletepatient/<id>')
def Deletepatient(id):
    cur = mysql.connection.cursor()
    cur.execute('''DELETE FROM Patients WHERE Patient_id = %s''',(id,))
    cur.execute('''commit;''')
    cur.execute('''SELECT * FROM Patients;''')
    PatientInfo = list(cur)
    cur.close()
    return render_template('addpatients.html',todo=PatientInfo)

@app.route('/Deletedoctor/<id>')
def Deletedoctor(id):
    cur = mysql.connection.cursor()
    cur.execute('''DELETE FROM Doctors WHERE Doctor_id = %s''',(id,))
    cur.execute('''commit;''')
    cur.execute('''SELECT * FROM Doctors;''')
    DoctorInfo = list(cur)
    cur.close()
    return render_template('adddoctors.html',todo=DoctorInfo)

@app.route('/Deletedepartment/<id>')
def Deletedepartment(id):
    cur = mysql.connection.cursor()
    cur.execute('''DELETE FROM Specialization WHERE Specialization_id = %s''',(id,))
    cur.execute('''commit;''')
    cur.execute('''SELECT * FROM Specialization;''')
    DepartmentInfo = list(cur)
    cur.close()
    return render_template('adddepartments.html',todo=DepartmentInfo)

@app.route('/Deleteappointment/<id>')
def Deleteappointment(id):
    cur = mysql.connection.cursor()
    cur.execute('''DELETE FROM Appointments WHERE Appointment_id = %s''',(id,))
    cur.execute('''commit;''')
    cur.execute('''SELECT * FROM Appointments;''')
    AppInfo = list(cur)
    cur.close()
    return render_template('addappointments.html',todo=AppInfo)
# -------------------------------------------------------------------------------------
# ------------------------------ To Read or query Info----------------------------------




# --------------------------------------------------------------------------------------

if __name__=='__main__':
    app.run(debug=True)