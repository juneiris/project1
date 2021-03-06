#!/usr/bin/env python2.7

"""
Columbia W4111 Intro to databases
Example webserver

To run locally

    python server.py

Go to http://localhost:8111 in your browser


A debugger such as "pdb" may be helpful for debugging.
Read about it online.
"""

import os
from datetime import datetime,date
from sqlalchemy import *
from sqlalchemy.pool import NullPool
from flask import Flask, request, render_template, g, redirect, Response

tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=tmpl_dir)


# configuration
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'

#
# The following uses the sqlite3 database test.db -- you can use this for debugging purposes
# However for the project you will need to connect to your Part 2 database in order to use the
# data
#
# XXX: The URI should be in the format of: 
#
#     postgresql://USER:PASSWORD@w4111db.eastus.cloudapp.azure.com/username
#
# For example, if you had username ewu2493, password foobar, then the following line would be:
#
#     DATABASEURI = "postgresql://ewu2493:foobar@w4111db.eastus.cloudapp.azure.com/ewu2493"
#
#DATABASEURI = "sqlite:///test.db"

DATABASEURI = "postgresql://cx2178:RDATHT@w4111db.eastus.cloudapp.azure.com/cx2178"



#
# This line creates a database engine that knows how to connect to the URI above
#
engine = create_engine(DATABASEURI)


#
# START SQLITE SETUP CODE
#
# after these statements run, you should see a file test.db in your webserver/ directory
# this is a sqlite database that you can query like psql typing in the shell command line:
# 
#     sqlite3 test.db
#
# The following sqlite3 commands may be useful:
# 
#     .tables               -- will list the tables in the database
#     .schema <tablename>   -- print CREATE TABLE statement for table
# 
# The setup code should be deleted once you switch to using the Part 2 postgresql database
#
#engine.execute("""DROP TABLE IF EXISTS test;""")
#engine.execute("""CREATE TABLE IF NOT EXISTS test (
#  id serial,
#  name text
#);""")
#engine.execute("""INSERT INTO test(name) VALUES ('grace hopper'), ('alan turing'), ('ada lovelace');""")
#
# END SQLITE SETUP CODE
#

uid = '111111'

@app.before_request
def before_request():
  """
  This function is run at the beginning of every web request 
  (every time you enter an address in the web browser).
  We use it to setup a database connection that can be used throughout the request

  The variable g is globally accessible
  """
  try:
    g.conn = engine.connect()
  except:
    print "uh oh, problem connecting to database"
    import traceback; traceback.print_exc()
    g.conn = None

@app.teardown_request
def teardown_request(exception):
  """
  At the end of the web request, this makes sure to close the database connection.
  If you don't the database could run out of memory!
  """
  try:
    g.conn.close()
  except Exception as e:
    pass


#
# @app.route is a decorator around index() that means:
#   run index() whenever the user tries to access the "/" path using a GET request
#
# If you wanted the user to go to e.g., localhost:8111/foobar/ with POST or GET then you could use
#
#       @app.route("/foobar/", methods=["POST", "GET"])
#
# PROTIP: (the trailing / in the path is important)
# 
# see for routing: http://flask.pocoo.org/docs/0.10/quickstart/#routing
# see for decorators: http://simeonfranklin.com/blog/2012/jul/1/python-decorators-in-12-steps/
#
@app.route('/')
def index():
  """
  request is a special object that Flask provides to access web request information:

  request.method:   "GET" or "POST"
  request.form:     if the browser submitted a form, this contains the data in the form
  request.args:     dictionary of URL arguments e.g., {a:1, b:2} for http://localhost?a=1&b=2

  See its API: http://flask.pocoo.org/docs/0.10/api/#incoming-request-data
  """

  # DEBUG: this is debugging code to see what request looks like
  #print request.args


  #
  # example of a database query
  #


  #cursor = g.conn.execute("SELECT * FROM users")
  #names = []
  #for result in cursor:
    #names.append(result['username'])  # can also be accessed using result[0]
  #cursor.close()

  #
  # Flask uses Jinja templates, which is an extension to HTML where you can
  # pass data to a template and dynamically generate HTML based on the data
  # (you can think of it as simple PHP)
  # documentation: https://realpython.com/blog/python/primer-on-jinja-templating/
  #
  # You can see an example template in templates/index.html
  #
  # context are the variables that are passed to the template.
  # for example, "data" key in the context variable defined below will be 
  # accessible as a variable in index.html:
  #
  #     # will print: [u'grace hopper', u'alan turing', u'ada lovelace']
  #     <div>{{data}}</div>
  #     
  #     # creates a <div> tag for each element in data
  #     # will print: 
  #     #
  #     #   <div>grace hopper</div>
  #     #   <div>alan turing</div>
  #     #   <div>ada lovelace</div>
  #     #
  #     {% for n in data %}
  #     <div>{{n}}</div>
  #     {% endfor %}
  #
  #context = dict(data = names)


  #
  # render_template looks in the templates/ folder for files.
  # for example, the below file reads template/index.html
  #
  return render_template("index.html")

#
# This is an example of a different path.  You can see it at
# 
#     localhost:8111/another
#
# notice that the functio name is another() rather than index()
# the functions for each app.route needs to have different names
#
@app.route('/another',methods=['GET', 'POST'])
def another():
    error=None
    shopid=request.args.get('shopid')
    print shopid

    #write comments
    if request.method=='POST':
        if request.form["submit"]=="Write a comment":
            cmtwrt=request.form['comments']
            print cmtwrt

            if uid=='111111':
                print "ye"
                error='Please login first'
                return render_template('anotherfile.html', error=error)
            else:
                cmttime=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                print cmttime
                v_funnynum=0
                v_coolnum=0
                v_useful=0
                q="SELECT MAX(labelnum) FROM comments WHERE shopid='%s'"%shopid
                #print q
                lastlabel=g.conn.execute(q)
                #label=[]
                for result in lastlabel:
                #    print result
                    if result[0]== None:
                        label=1
                    else:
                        label=result[0]+1
                lastlabel.close()

                args=(label,shopid,uid,cmttime,cmtwrt,v_funnynum,v_coolnum,v_useful)
                qi="INSERT INTO comments VALUES(%s,%s,%s,%s,%s,%s,%s,%s)"
                g.conn.execute(qi, args)
                #return redirect('/')

        if request.form["submit"]=="Like it":
            if uid=='111111':
                print "ye"
                error='Please login first'
                return render_template('anotherfile.html', error=error)
            else:
                # check if the record has already existed
                cur1=g.conn.execute("SELECT userid from likes")
                existuser=[]
                for result in cur1:
                    existuser.append(result[0])
                cur1.close()
                print existuser

                if uid in existuser:
                    cur2=g.conn.execute("SELECT shopid from likes WHERE userid='%s'"%uid)
                    existshop=[]
                    for result in cur2:
                        existshop.append(result[0])
                    cur2.close()
                    print existshop
                    if shopid in existshop:
                        error='You have liked this shop!'
                        return render_template('anotherfile.html', shopid=shopid,error=error)

                # insert new record
                ltime=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                print ltime
                args=(uid,shopid,ltime)
                qi="INSERT INTO likes VALUES(%s,%s,%s)"
                g.conn.execute(qi, args)

                q="SELECT DISTINCT u.username FROM likes l, users u WHERE u.userid<>'%s'"%uid +" AND u.userid=l.userid AND l.shopid='%s'"%shopid
                print q
                lpeople=g.conn.execute(q)
                people=[]
                flag=0
                for result in lpeople:
                    flag=1
                    people.append(result[0]+"  ")
                if flag==0:
                    people.append("No other people liked this shop yet... You are the first!")
                lpeople.close()
                #print people
                q2="SELECT DISTINCT s.shopname FROM likes l, shops s WHERE s.shopid<>'%s'"%shopid +" AND s.shopid=l.shopid AND l.userid='%s'"%uid
                print q2
                lh=g.conn.execute(q2)
                hist=[]
                for result in lh:
                        hist.append(result[0]+"  ")
                lh.close()
                return render_template("like.html", data=people,lhist=hist)


        if request.form["submit"]=="Reserve it":
            if uid=='111111':
                print "ye"
                error='Please login first'
                return render_template('anotherfile.html', error=error)
            else:

                #deal with input error
                num=str(request.form['pnum'])

                try:
                    num=int(num)
                except:
                    error='Please input people number as a number'
                    return render_template('anotherfile.html',shopid=shopid,error=error)

                rtime=datetime.now()
                d=request.form['rdate']
                t=request.form['rtime']
                if d=='' or t=='' or num=='':
                    error='Please input your reservation time and people number'
                    return render_template('anotherfile.html',shopid=shopid,error=error)
                dtime=str(d+' '+t)
                djudge=datetime.strptime(d, "%Y-%m-%d")

                if (djudge-rtime).seconds<1800 or (djudge-rtime).days<0:
                    error="reservation time is invalid, it's too close from now. Please input again"
                    return render_template('anotherfile.html',shopid=shopid,error=error)

                sh=g.conn.execute("SELECT starthour from shops WHERE shopid='%s'"%shopid)
                for result in sh:
                    starthour=str(result[0])
                sh.close()
                eh=g.conn.execute("SELECT closehour from shops WHERE shopid='%s'"%shopid)
                for result in eh:
                    endhour=str(result[0])
                eh.close()
                print "query business hour complete"

                starthour=datetime.strptime(starthour, "%H:%M:%S")
                endhour=datetime.strptime(endhour, "%H:%M:%S")
                t=datetime.strptime(t, "%H:%M:%S")
                print starthour,endhour,t
                if starthour<endhour:
                    if t<starthour or t>endhour:
                        error="The time you reserve is not the shop's business hour!"
                        return render_template('anotherfile.html',shopid=shopid,error=error)
                else:
                    if t<starthour and t>endhour:
                        error="The time you reserve is not the shop's business hour!"
                        return render_template('anotherfile.html',shopid=shopid,error=error)


                #print rtime
                #deal with existed record in database
                cur1=g.conn.execute("SELECT userid from reserve")
                existuser=[]
                for result in cur1:
                    existuser.append(result[0])
                cur1.close()
                print existuser
                if uid in existuser:
                    cur2=g.conn.execute("SELECT DISTINCT shopid from reserve WHERE userid='%s'"%uid+" AND rdate='%s'"%dtime)
                    existshop=[]
                    for result in cur2:
                        existshop.append(result[0])
                    cur2.close()
                    print existshop
                    if shopid in existshop:
                        error='You have reserved this shop for that time!'
                        return render_template('anotherfile.html', shopid=shopid,error=error)

                # insert new record
                args=(uid,shopid,dtime,num)
                qi="INSERT INTO reserve VALUES(%s,%s,%s,%s)"
                g.conn.execute(qi, args)

                #show relevant info
                q="SELECT DISTINCT u.username FROM reserve r, users u WHERE u.userid<>'%s'"%uid +" AND u.userid=r.userid AND r.shopid='%s'"%shopid
                print q
                rpeople=g.conn.execute(q)
                people=[]
                flag=0
                for result in rpeople:
                    flag=1
                    people.append(result[0]+"  ")
                if flag==0:
                    people.append("No other people reserved this shop yet...")
                rpeople.close()
                #print people
                q2="SELECT DISTINCT s.shopname FROM reserve r, shops s WHERE s.shopid<>'%s'"%shopid +" AND s.shopid=r.shopid AND r.userid='%s'"%uid
                print q2
                rh=g.conn.execute(q2)
                hist=[]
                for result in rh:
                        hist.append(result[0]+"  ")
                rh.close()
                return render_template("reserve.html", data=people,rhist=hist)

        if request.form["submit"]=="Rate it":
            if uid=='111111':
                print "ye"
                error='Please login first'
                return render_template('anotherfile.html', error=error)
            else:

                #deal with input error
                rscore=str(request.form["score"])
                try:
                    rscore=float(rscore)
                    if rscore>5:
                        error='Your rating score should be smaller than 5'
                        return render_template('anotherfile.html',shopid=shopid,error=error)
                except:
                    error='Please input your rating score as a number smaller than 5'
                    return render_template('anotherfile.html',shopid=shopid,error=error)

                print rscore

                # deal with existed record in database
                cur1=g.conn.execute("SELECT userid from rate")
                existuser=[]
                for result in cur1:
                    existuser.append(result[0])
                cur1.close()
                print existuser
                if uid in existuser:
                    cur2=g.conn.execute("SELECT shopid from rate WHERE userid='%s'"%uid)
                    existshop=[]
                    for result in cur2:
                        existshop.append(result[0])
                    cur2.close()
                    print existshop
                    if shopid in existshop:
                        error='You have rated this shop before!'
                        return render_template('anotherfile.html', shopid=shopid,error=error)

                #insert new record
                ratetime=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                args=(uid,shopid,ratetime,rscore)
                qi="INSERT INTO rate VALUES(%s,%s,%s,%s)"
                g.conn.execute(qi, args)

                #show relevant info
                q="SELECT u.username,r.score FROM rate r, users u WHERE u.userid<>'%s'"%uid +" AND u.userid=r.userid AND r.shopid='%s'"%shopid
                print q
                rpeople=g.conn.execute(q)
                people=[]
                flag=0
                for result in rpeople:
                    flag=1
                    people.append(result[0]+"  "+str(result[1]))
                if flag==0:
                    people.append("No other people rated this shop yet...")
                rpeople.close()
                return render_template("rate.html", data=people,score=rscore)


            #g.conn.execute('INSERT INTO test VALUES (NULL, ?)', name)
            #return redirect('/')

    # query and display
    q="SELECT s.shopname,s.rating_score,to_char(s.starthour,'HH24:MI:SS'),to_char(s.closehour,'HH24:MI:SS'),s.contactinfo,s.avg_cost,s.cusine_type,s.shoptype FROM shops s WHERE s.shopid='%s'"%shopid
    print q
    cur = g.conn.execute(q)
    shopinfo=[]
    for result in cur:
        shopinfo.append(result[0]+"   "+str(result[1])+"   "+result[2]+"   "+result[3]+"   "+result[4]+"   "+str(result[5])+"   "+result[6]+"   "+result[7])   # can also be accessed using result[0]

    cur.close()

    cur2=g.conn.execute("SELECT context FROM comments WHERE shopid='%s'"%shopid)
    comments=[]
    for result in cur2:
        comments.append(result[0])   # can also be accessed using result[0]

    cur2.close()

    cur3=g.conn.execute("SELECT l.aptnum,l.street,l.city,l.state,l.postcode FROM locate_in l WHERE l.shopid='%s'"%shopid)
    adds=[]
    for result in cur3:
        adds.append(result[0]+"   "+str(result[1])+"   "+result[2]+"   "+result[3]+"   "+result[4])   # can also be accessed using result[0]

    cur3.close()
    print adds



    return render_template("anotherfile.html",data=shopinfo,cmts=comments,address=adds,shopid=shopid)

# @app.route('/login')
# def login():
#     return render_template("login.html")
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
       username = request.form['username']
       passwords = g.conn.execute("SELECT password FROM users WHERE username='%s'"%username)
       error = 'No Such User'
       uids = g.conn.execute("SELECT userid FROM users WHERE username='%s'"%username)
       for id in uids:
           global uid
           uid = id[0]
#	   print uid
       for password in passwords:
	   getpassword = password[0]
           if request.form['password'] != getpassword:
                error = 'Login Error, Try Again'
           else:
#               session['logged_in'] = True
             	print 'You were logged in'
               	return redirect('/')
       passwords.close();
       uids.close();
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect('index.html')

@app.route('/createaccount')
def create_account():
    return render_template("createaccount.html")


# Example of adding new data to the database
@app.route('/add', methods=['POST'])
def add():
  name = request.form['name']
  g.conn.execute('INSERT INTO test VALUES (NULL, ?)', name)
  return redirect('/')


#show restuarants according to filter

reslist=[]
@app.route('/restlist', methods=['POST'])
def restlist():
  if request.form["submit"] == "Search nearby!" :
      neararea=request.form['Near']
      if neararea=="none":
          q="SELECT shopname,rating_score,shopid FROM shops ORDER BY rating_score DESC"
          print q
          cur = g.conn.execute(q)
      else:
          q="SELECT s.shopname,s.rating_score,s.shopid FROM shops s,locate_in l WHERE l.shopid=s.shopid AND l.postcode='%s' ORDER BY rating_score DESC"%neararea
          print q
          cur = g.conn.execute(q)

      names = []
      #rating=[]
      print cur
      for result in cur:
          names.append(result[0]+"   "+str(result[1])+"   "+result[2])   # can also be accessed using result[0]
          #rating.append(result[1])
      cur.close()
      context = dict(data = names)

  if request.form["submit"] == "Apply!" :
      type = request.form['Type']
      area = request.form['Area']
      take_out = request.form['Take_out']
      delivery = request.form['Delivery']
      sort=request.form['Sort']
      if sort=="none":
          ratingsort=""
      if sort=="DESC":
          ratingsort=" DESC"

      if type=="none" and area=="none" and take_out=="none" and delivery=="none":
          q="SELECT shopname,rating_score,shopid FROM shops ORDER BY rating_score"+ratingsort
          print q
          cur = g.conn.execute(q)
      else:
          w=" WHERE"
          if type=="none":
              stp=""
          else:
              stp=" s.shoptype='%s'"%type

          if area=="none":
              sa=""
              l=""
              alian=""
          else:
              alian=""
              sa=" l.shopid=s.shopid AND l.postcode='%s'"%area
              l=",locate_in l"
              if type!="none":
                  alian=" AND"

          if take_out=="none":
              stake=""
              tlian=""
          else:
              tlian=""
              stake=" s.s_takeout='%s'"%take_out
              if type!="none" or area!="none":
                  tlian=" AND"

          if delivery=="none":
              sd=""
              slian=""
          else:
              slian=""
              sd=" s.s_delivery='%s'"%delivery
              if type!="none" or area!="none" or take_out!="none":
                  slian=" AND"

          #cur = g.conn.execute('SELECT s.shopname FROM shops s,locate_in l WHERE s.shopid=l.shopid AND s.shoptype=type AND l.postcode=area AND s.s_takeout=take_out AND s.s_delivery=delievery')
          #q = 'SELECT s.shopname FROM shops s WHERE s.shoptype=%s AND s.s_takeout=%s'
          q="SELECT s.shopname,s.rating_score,s.shopid FROM shops s"+l+w+stp+alian+sa+tlian+stake+slian+sd+" ORDER BY s.rating_score"+ratingsort
          #q="SELECT s.shopname FROM shops s"+l+w+stp+alian+sa
          #q="SELECT s.shopname FROM shops s"+l+w+stp+tlian+stake

          print q
          cur = g.conn.execute(q)
          #cur = g.conn.execute(q,type,take_out)

      names = []
      #rating=[]
      print cur
      for result in cur:
          names.append(result[0]+"   "+str(result[1])+"   "+result[2])   # can also be accessed using result[0]
          #rating.append(result[1])
      cur.close()
      global reslist
      reslist=names
      context = dict(data = names)

  if request.form["submit"] == "Order History" :
      print uid
      shopnames = g.conn.execute("SELECT s.shopname FROM shops s, orders o WHERE s.shopid = o.shopid AND o.userid='%s'"%uid)
      shops = []
      for shopname in shopnames:
	    shops.append(shopname[0])
      shopnames.close()
      context = dict(data = shops)
#  elif  ( $_REQUEST['orderhistory'] )
  #g.conn.execute('INSERT INTO test VALUES (NULL, ?)', name)
  return render_template("index.html", **context)


#for n in reslist:
@app.route('/mVHrayj', methods=['GET'])
def detail():
    return render_template('mVHrayj.html')







if __name__ == "__main__":
  import click

  @click.command()
  @click.option('--debug', is_flag=True)
  @click.option('--threaded', is_flag=True)
  @click.argument('HOST', default='0.0.0.0')
  @click.argument('PORT', default=8111, type=int)
  def run(debug, threaded, host, port):
    """
    This function handles command line parameters.
    Run the server using

        python server.py

    Show the help text using

        python server.py --help

    """

    HOST, PORT = host, port
    #print "running on %s:%d" % (HOST, PORT)
    app.run(host=HOST, port=PORT, debug=debug, threaded=threaded)


  run()



