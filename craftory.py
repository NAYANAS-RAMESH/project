from flask import *
from DBConnection import *
db=Database()
app = Flask(__name__)
app.secret_key='action'


@app.route('/')
def login():
    return render_template("loginindex.html")

@app.route('/login_post', methods=['POST'])
def login_post():
    username=request.form['textfield']
    password=request.form['textfield2']
    print(username,password)
    db=Database()
    qry="SELECT*FROM `login`WHERE username='"+username+"' AND PASSWORD='"+password+"'"
    res=db.selectOne(qry)
    print(res)
    if res is not None:
        session['lid']=res['login_id']
        if res['type']=='admin':
            return redirect('/home')
        elif res['type']=='artist':
            return redirect('/artist_home')
        else:
            return '''<script> alert('no match found');window.location='/'</script>'''
    else:
            return '''<script> alert('no match found');window.location='/'</script>'''


@app.route('/logout')
def logout():
    session['lid']=""
    return redirect('/')

@app.route('/add_category')
def add_category():
    if session['lid']!='':
        return render_template('admin/add_category.html')
    else:
        return '''<script>alert("You Are Logout");window.location='/'</script>'''

@app.route('/add_categorypost',methods=['POST'])
def add_categorypost():
    if session['lid'] != '':
        category=request.form['textfield']

        db=Database()
        qry="INSERT INTO`category`(`categoryname`)VALUES('"+category+"')"
        res=db.insert(qry)
        return '''<script>alert("success");window.location='/add_category'</script>'''

    else:
        return '''<script>alert("You Are Logout");window.location='/'</script>'''

@app.route('/view_category')
def view_category():
    if session['lid'] != '':
        db=Database()
        qry="SELECT * FROM `category`"
        res=db.select(qry)
        return render_template('admin/view_category.html',data=res)
    else:
        return '''<script>alert("You Are Logout");window.location='/'</script>'''


@app.route('/edit_category/<cid>')
def edit_category(cid):
    if session['lid'] != '':
        db = Database()
        qry = "SELECT * FROM `category` where category_id='"+cid+"'"
        res = db.selectOne(qry)
        return render_template('admin/edit_category.html',data=res)
    else:
        return '''<script>alert("You Are Logout");window.location='/'</script>'''

@app.route('/edit_categorypost',methods=['POST'])
def edit_categorypost():
    if session['lid'] != '':
        categoryname=request.form['textfield']
        category_id=request.form['category_id']
        db=Database()
        qry="UPDATE`category`SET categoryname='"+categoryname+"' WHERE category_id='"+category_id+"'"
        res=db.update(qry)
        return '''<script>alert("updated");window.location='/view_category'</script>'''
    else:
        return '''<script>alert("You Are Logout");window.location='/'</script>'''


@app.route('/delete_category/<id>')
def delete_category(id):
    if session['lid'] != '':
        db=Database()
        qry="DELETE FROM `category` WHERE `category_id`='"+id+"'"
        res=db.delete(qry)
        return '''<script>alert("Deleted");window.location='/view_category'</script>'''
    else:
        return '''<script>alert("You Are Logout");window.location='/'</script>'''


@app.route('/change_password')
def change_password():
    if session['lid'] != '':
        return render_template('admin/change_password.html')
    else:
        return '''<script>alert("You Are Logout");window.location='/'</script>'''

@app.route('/change_passwordpost',methods=['POST'])
def change_passwordpost():
    if session['lid'] != '':
        currentpassword=request.form['textfield']
        newpassword=request.form['textfield2']
        confirmpassword=request.form['textfield3']
        db=Database()
        qry = "SELECT*FROM `login`WHERE login_id='" + str(session['lid']) + "' AND PASSWORD='" + currentpassword + "'"
        res = db.selectOne(qry)
        if res is not None:
            if newpassword==confirmpassword:
                qry="UPDATE login SET PASSWORD='"+confirmpassword+"' WHERE login_id='"+str(session['lid'])+"'"
                res=db.update(qry)
                return '''<script> alert('password changed');window.location='/'</script>'''
            else:
                return '''<script> alert('confirm password does not match');window.location='/change_password'</script>'''
        else:
            return '''<script> alert('current password does not match');window.location='/change_password'</script>'''

    else:
        return '''<script>alert("You Are Logout");window.location='/'</script>'''
@app.route('/home')
def home():
    if session['lid'] != '':
        return render_template('admin/aindex.html')
    else:
        return '''<script>alert("You Are Logout");window.location='/'</script>'''


@app.route('/approveartist/<id>')
def approveartist(id):
    if session['lid'] != '':
        db=Database()
        qry="UPDATE `artist` SET STATUS='approved' WHERE login_id='"+id+"'"
        res=db.update(qry)
        return '''<script> alert('approved');window.location='/view_artist_approve'</script>'''
    else:
        return '''<script>alert("You Are Logout");window.location='/'</script>'''


@app.route('/rejectartist/<id>')
def rejectartist(id):
    if session['lid'] != '':
        db=Database()
        qry="UPDATE `artist` SET STATUS='rejected' WHERE login_id='"+id+"'"
        res=db.update(qry)
        return '''<script> alert('rejected');window.location='/view_artist_approve'</script>'''
    else:
        return '''<script>alert("You Are Logout");window.location='/'</script>'''


@app.route('/view_artist_approve')
def view_artist_approve():
    if session['lid'] != '':
        db=Database()
        qry="SELECT * FROM `artist` WHERE `status`='pending'"
        res=db.select(qry)
        return render_template('admin/view_artist&approve.html',data=res)
    else:
        return '''<script>alert("You Are Logout");window.location='/'</script>'''


@app.route('/view_artist_approve_post', methods=['POST'])
def view_artist_approve_post():
    if session['lid'] != '':
        name=request.form['textfield']
        db = Database()
        qry = "SELECT * FROM `artist` WHERE `status`='pending' and name like '%"+name+"%'"
        res = db.select(qry)
        return render_template('admin/view_artist&approve.html', data=res)
    else:
        return '''<script>alert("You Are Logout");window.location='/'</script>'''


@app.route('/view_artistapprove')
def view_artistapprove():
    if session['lid'] != '':
        db=Database()
        qry="SELECT * FROM `artist` WHERE `status`='approved'"
        res=db.select(qry)
        return render_template('admin/view_artistapprove.html',data=res)
    else:
        return '''<script>alert("You Are Logout");window.location='/'</script>'''


@app.route('/view_artistapprove_post', methods=['POST'])
def view_artistapprove_post():
    if session['lid'] != '':
        name=request.form['textfield']
        db = Database()
        qry = "SELECT * FROM `artist` WHERE `status`='approved' AND name like '%"+name+"%'"
        res = db.select(qry)
        return render_template('admin/view_artistapprove.html', data=res)
    else:
        return '''<script>alert("You Are Logout");window.location='/'</script>'''


@app.route('/view_artistrejected')
def view_artistrejected():
    if session['lid'] != '':
        db=Database()
        qry="SELECT * FROM `artist` WHERE `status`='rejected'"
        res=db.select(qry)
        return render_template('admin/view_artistrejected.html',data=res)
    else:
        return '''<script>alert("You Are Logout");window.location='/'</script>'''


@app.route('/view_artistrejected_post', methods=['POST'])
def view_artistrejected_post():
    if session['lid'] != '':
        name=request.form['textfield']
        db = Database()
        qry = "SELECT * FROM `artist` WHERE `status`='rejected' AND name like '%"+name+"%'"
        res = db.select(qry)
        return render_template('admin/view_artistrejected.html', data=res)
    else:
        return '''<script>alert("You Are Logout");window.location='/'</script>'''


@app.route('/view_camplaint')
def view_camplaint():
    if session['lid'] != '':
        db=Database()
        qry = "SELECT * FROM complaint INNER JOIN `user` ON user.login_id=complaint.user_lid"
        res=db.select(qry)
        return render_template('admin/view_camplaints&replay.html',data=res)
    else:
        return '''<script>alert("You Are Logout");window.location='/'</script>'''


@app.route('/view_camplaint_post',methods=['POST'])
def view_camplaint_post():
    if session['lid'] != '':
        Fromdate=request.form['textfield']
        Todate=request.form['textfield2']
        db = Database()
        qry = "SELECT * FROM complaint INNER JOIN `user` ON user.login_id=complaint.user_lid where date between '"+Fromdate+"' and '"+Todate+"'"
        res = db.select(qry)
        return render_template('admin/view_camplaints&replay.html',data=res)
    else:
        return '''<script>alert("You Are Logout");window.location='/'</script>'''


@app.route('/send_reply/<id>')
def send_reply(id):
    if session['lid'] != '':
        return render_template('admin/send_reply.html',id=id)
    else:
        return '''<script>alert("You Are Logout");window.location='/'</script>'''


@app.route('/send_reply_post', methods=['POST'])
def send_complaint_post():
    if session['lid'] != '':
        db=Database()
        id=request.form['id']
        reply=request.form['textarea']
        qry="UPDATE `complaint` SET`replay`='"+reply+"',`status`='replied' WHERE `complaint_id`='"+id+"'"
        res=db.update(qry)
        return '''<script>alert("send");window.location='/view_camplaint_replay'</script>'''

    else:
        return '''<script>alert("You Are Logout");window.location='/'</script>'''


@app.route('/view_highlightsartist')
def view_highlightsartist():
    if session['lid'] != '':
        db=Database()
        qry  ="SELECT * FROM `highlights work` INNER JOIN WORK ON work.work_id=`highlights work`.work_id INNER JOIN `artist`ON artist.login_id=work.artist_lid"
        res=db.select(qry)
        return render_template('admin/view_highlightsartist.html',data=res)
    else:
        return '''<script>alert("You Are Logout");window.location='/'</script>'''


@app.route('/view_highlightsartist_post', methods=['POST'])
def view_highlightsartist_post():
    if session['lid'] != '':
        name=request.form['textfield']
        db = Database()
        qry = "SELECT * FROM `highlights work` INNER JOIN WORK ON work.work_id=`highlights work`.work_id INNER JOIN `artist`ON artist.login_id=work.artist_lid where name like '%"+name+"%'"
        res = db.select(qry)
        return render_template('admin/view_highlightsartist.html', data=res)
    else:
        return '''<script>alert("You Are Logout");window.location='/'</script>'''


@app.route('/view_feedback')
def view_feedback():
    if session['lid'] != '':
        db=Database()
        qry="SELECT *FROM `feedback`INNER JOIN USER ON user.login_id=feedback.user_lid"
        res=db.select(qry)
        return render_template('admin/view_feedback.html',data=res)
    else:
        return '''<script>alert("You Are Logout");window.location='/'</script>'''


@app.route('/view_feedbackpost',methods=['POST'])
def view_feedbackpost():
    if session['lid'] != '':
        Fromdate=request.form['textfield']
        Todate=request.form['textfield2']
        db = Database()
        qry = "SELECT *FROM `feedback`INNER JOIN USER ON user.login_id=feedback.user_lid where date between '"+Fromdate+"' and '"+Todate+"'"
        res = db.select(qry)
        return render_template('admin/view_feedback.html', data=res)
    else:
        return '''<script>alert("You Are Logout");window.location='/'</script>'''


@app.route('/view_workartist')
def view_workartist():
    if session['lid'] != '':
        db=Database()
        qry="SELECT * FROM  WORK  INNER JOIN `artist`ON artist.login_id=work.artist_lid"
        res=db.select(qry)
        return render_template('admin/view_workartist.html',data=res)
    else:
        return '''<script>alert("You Are Logout");window.location='/'</script>'''


@app.route('/view_workartist_post', methods=['POST'])
def view_workartist_post():
    if session['lid'] != '':
        name=request.form['textfield']
        db = Database()
        qry = "SELECT * FROM  WORK  INNER JOIN `artist`ON artist.login_id=work.artist_lid where workname like'%"+name+"%'"
        res = db.select(qry)
        return render_template('admin/view_workartist.html', data=res)
    else:
        return '''<script>alert("You Are Logout");window.location='/'</script>'''


@app.route('/view_user')
def view_user():
    if session['lid'] != '':
        db=Database()
        qry="SELECT *FROM`user`"
        res=db.select(qry)
        return render_template('admin/view_user.html',data=res)
    else:
        return '''<script>alert("You Are Logout");window.location='/'</script>'''


@app.route('/view_user_post', methods=['POST'])
def view_user_post():
    if session['lid'] != '':
        name=request.form['textfield']
        db = Database()
        qry = "SELECT *FROM`user` where name like '%"+name+"%'"
        res = db.select(qry)
        return render_template('admin/view_user.html', data=res)

    else:
        return '''<script>alert("You Are Logout");window.location='/'</script>'''


####################################################################
@app.route('/artist_home')
def artist_home():
    if session['lid'] != '':
        return  render_template("artist/tindex.html")
    else:
        return '''<script>alert("You Are Logout");window.location='/'</script>'''


@app.route('/artist_signup')
def artist_signup():
    return render_template("artist/sign_index.html")


@app.route('/and_signup', methods=['POST'])
def and_signup():
    photo=request.files['Photo']
    name=request.form['name']
    DOB=request.form['dob']
    category=request.form['category']
    gender=request.form['RadioGroup1']
    phoneno=request.form['phoneno']
    email=request.form['email']
    housename=request.form['textfield']
    place=request.form['textfield2']
    post=request.form['textfield3']
    district=request.form['textfield4']
    state=request.form['textfield5']
    pincode=request.form['textfield6']
    password=request.form['textfield7']
    confirmpassword=request.form['textfield8']
    from datetime import datetime
    date=datetime.now().strftime('%Y%m%d-%H%M%S')
    photo.save("C:\\Users\\User\\PycharmProjects\\craftory\\static\\artist image\\"+date+".jpg")
    path="/static/artist image/"+date+".jpg"
    db=Database()
    qry="INSERT INTO login (`username`,PASSWORD,TYPE)VALUES('"+email+"','"+password+"','artist')"
    res=db.insert(qry)
    qry2="INSERT INTO artist(`login_id`,`status`,`name`,`phoneno`,`email`,`DOB`,`place`,`category`,`photo`,`gender`,`pincode`,`housename`,`post`,`district`,`state`)VALUES('"+str(res)+"','pending','"+name+"','"+phoneno+"','"+email+"','"+DOB+"','"+place+"','"+category+"','"+path+"','"+gender+"','"+pincode+"','"+housename+"','"+post+"','"+district+"','"+state+"')"
    res2=db.insert(qry2)
    return '''<script>alert("success");window.location='/'</script>'''

@app.route('/artist_addwork')
def artist_addwork():
    if session['lid'] != '':
        return render_template("artist/addwork_management.html")
    else:
        return '''<script>alert("You Are Logout");window.location='/'</script>'''


@app.route('/and_addwork_post', methods=['POST'])
def and_addwork_post():
    if session['lid'] != '':
        workname=request.form['textfield']
        worktype=request.form['textfield2']
        description=request.form['textarea']
        photo=request.files['fileField']
        price=request.form['textfield3']
        from datetime import datetime
        date = datetime.now().strftime('%Y%m%d-%H%M%S')
        photo.save("C:\\Users\\User\\PycharmProjects\\craftory\\static\\workimg\\" + date + ".jpg")
        path = "/static/workimg/" + date + ".jpg"
        db=Database()
        qry="INSERT INTO WORK(`artist_lid`,`workname`,`worktype`,`description`,`photo`,'price')VALUES('"+str(session['lid'])+"','"+workname+"','"+worktype+"','"+description+"','"+path+"','"+price+"')"
        res=db.insert(qry)
        return '''<script>alert("success");window.location='/artist_addwork'</script>'''
    else:
        return '''<script>alert("You Are Logout");window.location='/'</script>'''



@app.route('/and_viewwork')
def and_viewwork():
    if session['lid'] != '':
        db=Database()
        qry="SELECT * FROM `work` WHERE artist_lid='"+str(session['lid'])+"'"
        res=db.select(qry)
        return render_template("artist/view_work_mngmt.html",data=res)
    else:
        return '''<script>alert("You Are Logout");window.location='/'</script>'''


@app.route('/edit_work/<id>')
def edit_work(id):
    if session['lid'] != '':
        db=Database()
        qry="SELECT * FROM `work` WHERE `work_id`='"+id+"'"
        res=db.selectOne(qry)
        return render_template("artist/edit_work.html",data=res)

    else:
        return '''<script>alert("You Are Logout");window.location='/'</script>'''


@app.route('/and_editwork_post', methods=['POST'])
def and_editwork_post():
    if session['lid'] != '':
        id = request.form['id']
        workname = request.form['textfield']
        worktype = request.form['textfield2']
        description = request.form['textarea']
        price=request.form['price']
        if 'fileField' in request.files:
            photo = request.files['fileField']
            if photo.filename!="":
                from datetime import datetime
                date = datetime.now().strftime('%Y%m%d-%H%M%S')
                photo.save("C:\\Users\\User\\PycharmProjects\\craftory\\static\\workimg\\" + date + ".jpg")
                path = "/static/workimg/" + date + ".jpg"
                db = Database()
                qry = "UPDATE `work` SET  `workname`='" + workname + "',`worktype`='" + worktype + "',`description`='" + description + "',`photo`='" + path + "',`price`='"+price+"' where work_id='" + id + "' "
                res = db.update(qry)
                return '''<script>alert("success");window.location='/and_viewwork'</script>'''
            else:
                db = Database()
                qry = "UPDATE `work` SET  `workname`='" + workname + "',`worktype`='" + worktype + "',`description`='" + description +  "',`price`='"+price+"' where work_id='" + id + "' "
                res = db.update(qry)
                return '''<script>alert("success");window.location='/and_viewwork'</script>'''
        else:
            db = Database()
            qry = "UPDATE `work` SET  `workname`='" + workname + "',`worktype`='" + worktype + "',`description`='" + description + "',`price`='"+price+"' where work_id='" + id + "' "
            res = db.update(qry)
            return '''<script>alert("success");window.location='/and_viewwork'</script>'''

    else:
        return '''<script>alert("You Are Logout");window.location='/'</script>'''


@app.route('/and_deletework/<id>')
def and_deletework(id):
    if session['lid'] != '':
        db = Database()
        qry = "DELETE FROM`work`WHERE `work_id`='"+id+"'"
        res = db.delete(qry)
        return '''<script>alert("Deleted");window.location='/and_viewwork'</script>'''
    else:
        return '''<script>alert("You Are Logout");window.location='/'</script>'''


@app.route('/add_highlights_work')
def add_highlights_work():
    if session['lid'] != '':
        db=Database()
        qry="select * from `work`"
        res=db.select(qry)
        return render_template("artist/highlights_work.html",data=res)
    else:
        return '''<script>alert("You Are Logout");window.location='/'</script>'''


@app.route('/and_addhighlightsofwork', methods=['POST'])
def and_addhighlightsofwork():
    if session['lid'] != '':
        work=request.form['select']
        date=request.form['textfield']
        description=request.form['textarea']
        db=Database()
        qry="INSERT INTO `highlights work`(`work_id`,`date`,`description`)VALUES('"+work+"','"+date+"','"+description+"')"
        res=db.insert(qry)
        return '''<script>alert("success");window.location='/add_highlights_work'</script>'''

    else:
        return '''<script>alert("You Are Logout");window.location='/'</script>'''


@app.route('/and_viewhighlightsofwork')
def and_viewhighlightsofwork():
    if session['lid'] != '':
        db=Database()
        qry="SELECT * FROM `highlights work` JOIN `work` ON `highlights work`.`work_id`=`work`.`work_id`"
        res=db.select(qry)
        return render_template("artist/view_highlightswork.html",data=res)

    else:
        return '''<script>alert("You Are Logout");window.location='/'</script>'''


#
# @app.route('/delete_hightlights_work/<id>')
# def delete_hightlights_work(id):
#     db=Database()
#     qry=""
#     res=db.delete(qry)
#     return '''<script>alert("Deleted");window.location='/and_viewhighlightsofwork'</script>'''



@app.route('/and_viewprofile')
def and_viewprofileandmanage():
    if session['lid'] != '':
        db=Database()
        qry="SELECT * FROM artist WHERE login_id='"+str(session['lid'])+"'"
        res=db.selectOne(qry)
        return render_template("artist/view_profile.html",data=res)
    else:
        return '''<script>alert("You Are Logout");window.location='/'</script>'''


@app.route('/edit_profile')
def edit_profile():
    if session['lid'] != '':
        db=Database()
        qry="SELECT * FROM `artist` WHERE `login_id`='"+str(session['lid'])+"'"
        res=db.selectOne(qry)
        return render_template("artist/edit_profile.html",data=res)

    else:
        return '''<script>alert("You Are Logout");window.location='/'</script>'''


@app.route('/and_editprofile', methods=['POST'])
def and_editprofile():
    if session['lid'] != '':
        name = request.form['name']
        DOB = request.form['dob']
        category = request.form['category']
        gender = request.form['RadioGroup1']
        phoneno = request.form['phoneno']
        email = request.form['email']
        housename = request.form['textfield']
        place = request.form['textfield2']
        post = request.form['textfield3']
        district = request.form['textfield4']
        state = request.form['textfield5']
        pincode = request.form['textfield6']
        if 'fileField'in request.files:
            photo = request.files['Photo']
            if photo.filename!='':
                from datetime import datetime
                date = datetime.now().strftime('%Y%m%d-%H%M%S')
                photo.save("C:\\Users\\User\\PycharmProjects\\craftory\\static\\artist image\\" + date + ".jpg")
                path = "/static/artist image/" + date + ".jpg"
                db = Database()
                qry = "UPDATE `artist` SET `name`='" + name + "',`phoneno`='" + phoneno + "',`email`='" + email + "',`DOB`='" + DOB + "',`place`='" + place + "',`category`='" + category + "',`photo`='" + path + "',`gender`='" + gender + "',`pincode`='" + pincode + "',`housename`='" + housename + "',`post`='" + post + "',`district`='" + district + "',`state`='" + state + "' where login_id='" + str(
                    session['lid']) + "'"
                res = db.update(qry)
                return '''<script>alert("success");window.location='/and_viewprofile'</script>'''
            else:
                db = Database()
                qry = "UPDATE `artist` SET `name`='" + name + "',`phoneno`='" + phoneno + "',`email`='" + email + "',`DOB`='" + DOB + "',`place`='" + place + "',`category`='" + category  + "',`gender`='" + gender + "',`pincode`='" + pincode + "',`housename`='" + housename + "',`post`='" + post + "',`district`='" + district + "',`state`='" + state + "' where login_id='" + str(
                    session['lid']) + "'"
                res = db.update(qry)
                return '''<script>alert("success");window.location='/and_viewprofile'</script>'''
        else:
            db = Database()
            qry = "UPDATE `artist` SET `name`='" + name + "',`phoneno`='" + phoneno + "',`email`='" + email + "',`DOB`='" + DOB + "',`place`='" + place + "',`category`='" + category + "',`gender`='" + gender + "',`pincode`='" + pincode + "',`housename`='" + housename + "',`post`='" + post + "',`district`='" + district + "',`state`='" + state + "' where login_id='" + str(
                session['lid']) + "'"
            res = db.update(qry)
            return '''<script>alert("success");window.location='/and_viewprofile'</script>'''

    else:
        return '''<script>alert("You Are Logout");window.location='/'</script>'''


@app.route('/and_viewbooking')
def and_viewbooking():
    if session['lid'] != '':
        db = Database()
        qry = "SELECT * FROM `booking` JOIN `user`ON `booking`.`user_lid`=`user`.`login_id`JOIN `work`ON `booking`.`work_id`=`work`.`work_id` WHERE `status`='pending'"
        res = db.select(qry)
        return render_template("artist/view_booking.html",data=res)

    else:
        return '''<script>alert("You Are Logout");window.location='/'</script>'''


@app.route('/and_booking', methods=['POST'])
def and_bookin():
    if session['lid'] != '':
        db=Database()
        lid=request.form['lid']
        work_id=request.form['work_id']
        qry="INSERT INTO `booking`(`user_lid`,`work_id`,`status`,`date`)VALUES('"+lid+"','"+work_id+"','pending',CURDATE())"
        res=db.insert(qry)
        return jsonify(status="ok")
    else:
        return '''<script>alert("You Are Logout");window.location='/'</script>'''


# @app.route('/approve_booking/<id>')
# def approve_booking(id):
#     db=Database()
#     qry="UPDATE `booking` SET `status`='approve' WHERE `booking_id`='"+id+"'"
#     res=db.update(qry)
#     return '''<script>alert("Approve");window.location='/and_viewbooking'</script>'''


@app.route('/approve_booking/<id>')
def approve_booking(id):
    if session['lid'] != '':
        return render_template("artist/")

    else:
        return '''<script>alert("You Are Logout");window.location='/'</script>'''


@app.route('/and_view_approved_booking')
def and_viewapprovedbooking():
    if session['lid'] != '':
        db = Database()
        qry = "SELECT * FROM `booking` JOIN `user`ON `booking`.`user_lid`=`user`.`login_id`JOIN `work`ON `booking`.`work_id`=`work`.`work_id` WHERE booking.`status`='approve'"
        res = db.select(qry)
        return render_template("artist/view_approved_booking.html",data=res)

    else:
        return '''<script>alert("You Are Logout");window.location='/'</script>'''


@app.route('/add_offer')
def add_offer():
    if session['lid'] != '':
        db=Database()
        qry="SELECT * FROM `work`"
        res=db.select(qry)
        qry2="SELECT * FROM `payment`"
        res2=db.select(qry2)
        return render_template("artist/add_offer_management.html",data=res,data1=res2)

    else:
        return '''<script>alert("You Are Logout");window.location='/'</script>'''


@app.route('/and_addoffer', methods=['POST'])
def and_addoffer():
    if session['lid'] != '':
        work=request.form['select']
        payment=request.form['select2']
        date=request.form['textfield']
        description=request.form['textarea']
        db = Database()
        qry = "INSERT INTO `offer`(`work_id`,`payment_id`,`date`,`description`)VALUES('"+work+"','"+payment+"','"+date+"','"+description+"') "
        res = db.insert(qry)
        return '''<script>alert("Success");window.location='/add_offer'</script>'''
    else:
        return '''<script>alert("You Are Logout");window.location='/'</script>'''


@app.route('/and_viewoffer')
def and_viewoffer():
    if session['lid'] != '':
        db = Database()
        qry = "SELECT  `offer`.*,`work`.`workname`,`payment`.`amount` FROM `offer` JOIN `work` ON `offer`.`work_id`=`work`.`work_id` JOIN `payment` ON `offer`.`payment_id`=`payment`.`payment_id`"
        res = db.select(qry)
        return render_template("artist/view_offer_management.html",data=res)
    else:
        return '''<script>alert("You Are Logout");window.location='/'</script>'''


@app.route('/edit_offer/<id>')
def edit_offer(id):
    if session['lid'] != '':
        db=Database()
        qry= "SELECT  `offer`.*,`work`.`workname`,`payment`.`amount` FROM `offer` JOIN `work` ON `offer`.`work_id`=`work`.`work_id` JOIN `payment` ON `offer`.`payment_id`=`payment`.`payment_id` WHERE `offer_id`='" + id + "'"
        res = db.selectOne(qry)
        qry2 = "SELECT * FROM `work`"
        res2 = db.select(qry2)
        qry3 = "SELECT * FROM `payment`"
        res3 = db.select(qry3)
        return render_template("artist/edit_offer_management.html",data=res,data2=res2,data3=res3)

    else:
        return '''<script>alert("You Are Logout");window.location='/'</script>'''


@app.route('/and_editoffer_post', methods=['POST'])
def and_editoffer_post():
    if session['lid'] != '':
        offer_id=request.form['offer_id']
        work = request.form['select']
        payment = request.form['select2']
        date = request.form['textfield']
        description = request.form['textarea']
        db = Database()
        qry="UPDATE `offer` SET `work_id`='"+work+"',`payment_id`='"+payment+"',`date`='"+date+"',`description`='"+description+"' WHERE `offer_id`='"+offer_id+"'"
        res = db.update(qry)
        return '''<script>alert("updated");window.location='/and_viewoffer'</script>'''
    else:
        return '''<script>alert("You Are Logout");window.location='/'</script>'''


@app.route('/and_deleteoffer/<id>')
def and_deleteoffer(id):
    if session['lid'] != '':
        db = Database()
        qry = "DELETE FROM `offer`WHERE `offer_id`='"+id+"'"
        res = db.delete(qry)
        return '''<script>alert("Deleted");window.location='/and_viewoffer'</script>'''

    else:
        return '''<script>alert("You Are Logout");window.location='/'</script>'''


@app.route('/artist_send_notification/<id>')
def artist_send_notification(id):
    if session['lid'] != '':
        db = Database()
        qry1 = "update booking set status='approve' WHERE booking_id='"+str(id)+"'"
        res1 = db.update(qry1)
        qry = "SELECT * FROM `booking` JOIN `user`ON `booking`.`user_lid`=`user`.`login_id`JOIN `work`ON `booking`.`work_id`=`work`.`work_id` WHERE booking.booking_id='"+str(id)+"'"
        res = db.selectOne(qry)
        return render_template("artist/send_paymnt_notification.html",data=res)
    else:
        return '''<script>alert("You Are Logout");window.location='/'</script>'''


@app.route('/and_sendpaynotification', methods=['POST'])
def and_sendpaynotification():
    if session['lid'] != '':
        notification=request.form['textarea']
        id=request.form['id']
        db = Database()
        qry = "INSERT INTO `notification`(`notification`,`date`,`artist_lid`,`status`,`booking_id`) VALUES('"+notification+"',CURDATE(),'"+str(session['lid'])+"','pending','"+str(id)+"')"
        res = db.insert(qry)
        # qry="UPDATE `notification` SET `notification`='"+notification+"',`status`='sending' WHERE `notification_id`='"+id+"'"
        # res=db.update(qry)
        return '''<script>alert("success");window.location='/and_viewbooking'</script>'''

    else:
        return '''<script>alert("You Are Logout");window.location='/'</script>'''


@app.route('/and_viewpayment')
def and_viewpayment():
    if session['lid'] != '':
        db = Database()
        qry="SELECT `payment`.*,`user`.*,`booking`.`date`FROM `payment`JOIN`booking`ON `payment`.`booking_id`=`booking`.`booking_id`JOIN `user`ON `payment`.`user_lid`=`user`.`login_id`"
        res = db.select(qry)
        return render_template("artist/view_payments.html",data=res)
    else:
        return '''<script>alert("You Are Logout");window.location='/'</script>'''


@app.route('/artist_change_password')
def artist_change_password():
    if session['lid'] != '':
        return render_template("artist/change_password.html")
    else:
        return '''<script>alert("You Are Logout");window.location='/'</script>'''


@app.route('/and_changepassword', methods=['POST'])
def and_changepassword():
    if session['lid'] != '':
        currentpassword=request.form['textfield']
        newpassword=request.form['textfield2']
        confirm=request.form['textfield3']

        db = Database()
        qry = "SELECT * FROM `login` WHERE `password`='"+currentpassword+"'AND login_id='"+str(session['lid'])+"'"
        res = db.selectOne(qry)
        if res is not None:
            if newpassword==confirm:
                db=Database()
                qry="UPDATE `login` SET `password`='"+confirm+"' WHERE `login_id`='"+str(session['lid'])+"'"
                res=db.update(qry)
                return '''<script>alert("changed");window.location='/'</script>'''
            else:
                return '''<script>alert("not found");window.location='/'</script>'''
        else:
            return '''<script>alert("changed");window.location='/'</script>'''


    else:
        return '''<script>alert("You Are Logout");window.location='/'</script>'''


###################################################android####################################################







@app.route('/and_user_login',methods=['POST'])
def and_user_login():
    username = request.form['username']
    password = request.form['password']
    db = Database()
    qry = "SELECT * FROM `login` WHERE `username`='"+username+"' AND `password`='"+password+"'"
    res = db.selectOne(qry)
    if res is not None:
        return jsonify(status="ok",lid=res['login_id'], type=res['type'])
    else:
        return jsonify(status="not ok")
    
@app.route('/and_user_signup',methods=['POST'])
def and_user_signup():
    photo = request.form['photo']
    name = request.form['name']
    dob = request.form['dob']
    # category = request.form['category']
    gender = request.form['gender']
    phoneno = request.form['phoneno']
    email = request.form['email']
    housename = request.form['housename']
    place = request.form['place']
    post = request.form['post']
    password = request.form['password']
    confirm = request.form['confirm']
    pincode = request.form['pincode']
    import time,datetime
    import base64
    a=base64.b64decode(photo)
    timestr=time.strftime("%Y%m%d-%H%M%S")
    fh=open("C:\\Users\\Acer\\New folder\\craftory\\static\\user\\"+timestr+".jpg","wb")
    path="/static/user/"+timestr+".jpg"
    fh.write(a)
    fh.close()
    db=Database()
    if password==confirm:
        qry="INSERT INTO `login`(`username`,`password`,`type`)VALUES('"+email+"','"+confirm+"','user')"
        res=db.insert(qry)
        qry1="INSERT INTO `user`(`login_id`,`photo`,`name`,`phoneno`,`email`,`pincode`,`gender`,`DOB`,`housename`,`place`,`post`) VALUES('"+str(res)+"','"+path+"','"+name+"','"+phoneno+"','"+email+"','"+pincode+"','"+gender+"','"+dob+"','"+housename+"','"+place+"','"+post+"') "
        res1=db.insert(qry1)
        return jsonify(status="ok")
    else:
        return jsonify(status='no')
    
    
    
@app.route('/and_user_viewprofile',methods=['POST'])
def and_user_viewprofile():
    lid=request.form['lid']
    db=Database()
    qry="SELECT * FROM `user` WHERE `login_id`='"+lid+"'"
    res=db.selectOne(qry)
    return jsonify(status="ok",data=res)

@app.route('/and_user_addprofile',methods=['post'])
def and_user_addprofile():
    lid = request.form['lid']
    photo = request.form['photo']
    name = request.form['name']
    dob = request.form['dob']
    # category = request.form['category']
    gender = request.form['gender']
    phoneno = request.form['phoneno']
    email = request.form['email']
    housename = request.form['housename']
    place = request.form['place']
    post = request.form['post']
    # district = request.form['district']
    # state = request.form['state']
    pincode = request.form['pincode']
    if len(photo) > 1:
        import time, datetime
        import base64
        a = base64.b64decode(photo)
        timestr = time.strftime("%Y%m%d-%H%M%S")
        fh = open("C:\\Users\\Acer\\New folder\\craftory\\static\\user\\" + timestr + ".jpg", "wb")
        path = "/static/user/" + timestr + ".jpg"
        fh.write(a)
        fh.close()
        db=Database()
        qry="UPDATE `user` SET `photo`='"+path+"', `name`='"+name+"' ,`phoneno`='"+phoneno+"' ,`email`='"+email+"', `pincode`='"+pincode+"', `gender`='"+gender+"' ,`DOB`='"+dob+"', `housename`='"+housename+"', `place`='"+place+"', `post`='"+post+"' WHERE `login_id`='"+lid+"'"
        res=db.update(qry)
        return jsonify(status="ok")
    else:
        db = Database()
        qry = "UPDATE `user` SET  `name`='" + name + "' ,`phoneno`='" + phoneno + "' ,`email`='" + email + "', `pincode`='" + pincode + "' ,`gender`='" + gender + "' ,`DOB`='" + dob + "' ,`housename`='" + housename + "', `place`='" + place + "', `post`='" + post + "' WHERE `login_id`='" + lid + "'"
        res = db.update(qry)
        return jsonify(status="ok")


@app.route('/and_user_makeorder',methods=['post'])
def and_user_makeorder():
     lid = request.form['lid']
     wlid = request.form['wlid']
     db=Database()
     qry="INSERT INTO `booking`(`user_lid`,`work_id`,`status`,`date`) VALUES('"+lid+"','"+wlid+"','pending',curdate())"
     res=db.insert(qry)
     return jsonify(status="ok")



@app.route('/and_user_view_highlightwork',methods=['post'])
def and_user_viewhighlightwork():
    wid=request.form['wid']
    db=Database()
    qry="SELECT * FROM `highlights work` JOIN `work` ON `highlights work`.`work_id`=`work`.`work_id`  WHERE  `work`.`work_id`='"+wid+"'"
    res=db.select(qry)
    return jsonify(status="ok",data=res)


@app.route('/and_user_viewworkmanaged',methods=['post'])
def and_user_viewworkmanaged():

    db=Database()
    qry="SELECT * FROM `work`JOIN`artist`ON`work`.`artist_lid`=`artist`.`login_id`"
    res=db.select(qry)
    return jsonify(status="ok",data=res)


@app.route('/and_user_viewpaymntnotification',methods=['post'])
def and_user_viewpaymntnotification():
    lid = request.form['lid']
    db=Database()
    qry="SELECT * FROM `payment`JOIN `booking`ON`payment`.`booking_id`=`booking`.`booking_id` WHERE `payment`.`user_lid`='"+lid+"'"
    res=db.select(qry)
    return jsonify(status="ok",data=res)


@app.route('/and_send_complaint', methods=['POST'])
def and_send_complaint():
    db=Database()
    complaint=request.form['complaint']
    lid=request.form['lid']
    qry="INSERT INTO `complaint`(`complaint`,`date`,`replay`,`user_lid`,`status`)VALUES('"+complaint+"',CURDATE(),'pending','"+lid+"','pending')"
    res=db.insert(qry)
    return jsonify(status="ok")

@app.route('/and_view_reply', methods=['POST'])
def and_view_reply():
    db=Database()
    lid=request.form['lid']
    qry="SELECT * FROM `complaint` WHERE `user_lid`='"+lid+"'"
    res=db.select(qry)
    return jsonify(status="ok",data=res)

@app.route('/and_send_feedback', methods=['POST'])
def and_send_feedback():
    db=Database()
    feedback=request.form['feedback']
    lid=request.form['lid']
    qry="INSERT INTO `feedback`(`user_lid`,`feedback`,`date`)VALUES('"+lid+"','"+feedback+"',CURDATE())"
    res=db.insert(qry)
    return jsonify(status="ok")


@app.route('/and_view_feedback', methods=['POST'])
def and_view_feedback():
    db=Database()
    qry="SELECT * FROM `feedback`"
    res=db.select(qry)
    return jsonify(status="ok",data=res)


@app.route('/and_view_artist', methods=['POST'])
def and_view_artist():
    db=Database()
    aid=request.form['aid']
    qry="SELECT *,`artist`.`photo` AS apic, `work`.* FROM `work` INNER JOIN `artist` ON `artist`.`login_id`=`work`.`artist_lid` WHERE artist.`login_id`='"+aid+"'"
    res=db.select(qry)
    return jsonify(status="ok",data=res)



# @app.route('/and_payment', methods=['POST'])
# def and_payment():
#     db=Database()
#     acctno=request.form['acctno']
#     holder=request.form['holder']
#     ifsc=request.form['ifsc']
#     pin=request.form['pin']
#     balance=request.form['balance']
#     qry="INSERT INTO `bank`(`account_no`,`acct_holder`,`ifsc`,`pin`,`balance`)VALUES('"+acctno+"','"+holder+"','"+ifsc+"','"+pin+"','"+balance+"')"
#     res=db.insert(qry)
#     return jsonify(status="ok")




@app.route('/and_payment_one', methods=['POST'])
def and_payment_one():
    lid = request.form['lid']
    accnt_no = request.form['accno']
    ifsc = request.form['ifsc']
    pin = request.form['pin']
    amount = request.form['amt']
    bookingid=request.form['bookingid']
    # tot=0
    qry = "SELECT * FROM `bank` WHERE `account_no`='"+accnt_no+"' AND `IFSC`='"+ifsc+"' AND `pin`='"+pin+"'"
    db = Database()
    res = db.selectOne(qry)
    qry2="SELECT * FROM `booking` JOIN `work` ON `booking`.`work_id`=`work`.`work_id` WHERE `booking_id`='"+bookingid+"'"
    print(qry2)
    res2=db.selectOne(qry2)
    print(qry2)

    amount=res2['price']
    print(res)
    if res is not None:
        if float(res['balance'])>=float(amount):
            qry1="INSERT INTO `payment` (`booking_id`,`user_lid`,`amount`,`status`)VALUES('"+bookingid+"','"+lid+"','"+str(amount)+"','paid')"
            res1=db.insert(qry1)
            bal=float(res['balance'])-float(amount)
            qry3="UPDATE `bank` SET `balance`='"+str(bal)+"' WHERE `account_no`='"+accnt_no+"'"
            res3=db.update(qry3)
            return jsonify(status="ok")
        else:
            return jsonify(status="no")

    else:
        return jsonify(status="no")















@app.route('/and_view_payment_notification', methods=['POST'])
def and_view_payment_notification():
    db=Database()
    lid=request.form['lid']
    qry="SELECT *,`notification`.`date` AS ndate FROM `notification` JOIN `artist` ON `notification`.`artist_lid`=`artist`.`login_id` JOIN `booking` ON `notification`.`booking_id`=`booking`.`booking_id` WHERE `booking`.`user_lid`='"+lid+"'"
    res=db.select(qry)
    return jsonify(status="ok",data=res)









           # ----------------------------------------------CHAT-------------------------------------------------------#
@app.route("/chat")
def chat():
    return render_template("artist/fur_chat.html")

@app.route("/viewmsg/<senid>")  # refresh messages chatlist
def viewmsg(senid):
    uid = senid
    qry = "select from_id,message as msg,date from chat where (from_id='" + str(session['lid']) + "' and to_id='" + uid + "') or ((from_id='" + uid + "' and to_id='" + str(session['lid']) + "')) order by chat_id asc"
    db = Database()
    res = db.select(qry)
    print(res)
    qry = "SELECT * FROM `user` WHERE `login_id`='" + senid + "'"
    data = db.selectOne(qry)
    print(data, "---------------------------")
    return jsonify(data=res, name=data['name'], photo=data['photo'])

@app.route("/chatview", methods=['post'])
def chatview():
    db = Database()
    qry = "SELECT * FROM `user`"
    res = db.select(qry)
    return jsonify(data=res)

@app.route("/insert_chat/<senid>/<msg>")
def insert_chat(senid, msg):
    db = Database()

    qry="INSERT INTO `chat`(`from_id`,`to_id`,`message`,`date`)VALUES('"+str(session['lid'])+"','"+senid+"','"+msg+"',CURDATE())"
    db.insert(qry)
    return jsonify(status="ok")

@app.route('/and_view_order_status', methods=['POST'])
def and_view_order_status():
    db=Database()
    pid=request.form['lid']
    print(pid)
    qry="SELECT * FROM `booking` JOIN `work` ON `booking`.`work_id`=`work`.`work_id` WHERE booking.`status`='approve' AND booking.`user_lid`='"+pid+"'"
    res=db.select(qry)
    print(res)
    return jsonify(status="ok",data=res)





        # --------------------------------------------END OF CHAT--------------------------------------------------#


@app.route("/view_message",methods=['post'])  # refresh messages chatlist
def view_message():
    uid=request.form['fid']
    lastid=request.form['lastmsgid']
    db=Database()
    qry = "select chat_id,from_id,message as msg,date, to_id as toid from chat where ((from_id='0' and to_id='" + uid + "') or (from_id='" + uid + "' and to_id='0')) and chat_id>'"+lastid+"' order by chat_id desc"
    res = db.select(qry)
    return jsonify(data=res,status='ok',toid='0')

@app.route("/in_message", methods=['POST'])
def in_message():
    uid=request.form['fid']
    ta=request.form['msg']
    db=Database()
    qry="INSERT INTO `chat`(`from_id`,`to_id`,`message`,`date`)VALUES('"+uid+"','0','"+ta+"',CURDATE())"

    db.insert(qry)
    return jsonify(status='ok')



@app.route('/in_message2', methods=['POST'])
def in_message2():
    msg=request.form['msg']
    toid=request.form['toid']
    fromid=request.form['fromid']
    qry="INSERT INTO `chat`(`from_id`,`to_id`,`message`,`date`)VALUES('"+fromid+"','"+toid+"','"+msg+"',CURDATE())"
    db=Database()
    res=db.insert(qry)
    return jsonify(status='ok')


@app.route('/view_message2', methods=['POST'])
def view_message2():
    toid=request.form['toid']
    fid=request.form['fid']
    lastmsgid=request.form['lastmsgid']
    qry="SELECT * FROM chat WHERE ((`from_id`='"+fid+"' AND `to_id`='"+toid+"')OR(`from_id`='"+toid+"' AND `to_id`='"+fid+"')) AND `chat_id`>'"+lastmsgid+"' ORDER BY `chat_id` ASC"
    db=Database()
    res=db.select(qry)
    return jsonify(status='ok',data=res)


##################################################








if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')


