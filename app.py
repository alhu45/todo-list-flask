#importing flask to 
from flask import Flask, render_template, url_for, request, redirect

#databases
from flask_sqlalchemy import SQLAlchemy
#https://stackoverflow.com/questions/73961938/flask-sqlalchemy-db-create-all-raises-runtimeerror-working-outside-of-applicat
#The above link is used to fix the error that was occuring when creating the database

from datetime import datetime

#reference this file
app = Flask(__name__)

#tell the code where the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

#creating class for the database that holds id, content, completed, and date created
class Todo(db.Model):
  #creates an id for each task
  id = db.Column(db.Integer, primary_key = True)

  #holds each task
  content = db.Column(db.String(200), nullable = False)

  completed = db.Column(db.Integer, default = 0)

  #everytime a new task is created, date is created automatically
  data_created = db.Column(db.DateTime, default = datetime.utcnow)

#returns the task and the idfro 
  def __repr__(self):
    return '<Task %r>' % self.id
  
with app.app_context():
    db.create_all()

#Created a route for the index page to call the methods POST and GET
#Post is used to send data to the server to create/update a resource i.e logging into website
#Get is used to request data from a specified resource i.e getting bank statement from bank website from web server
@app.route('/', methods = ['POST', 'GET'])
def index():

  if request.method == 'POST':
    #gets the content from the form (where the user enters the task)
    task_content = request.form['content']

    #creating object of the class Todo
    new_task = Todo(content = task_content)

    try:
        #adds the new task to the database
        db.session.add(new_task)

        #commits the changes to the database
        db.session.commit()
        
        #redirects back to the index page to where the user enters the task
        return redirect('/')
    except:
        return 'There was an issue adding your task'
  else: 
    #returns all the tasks in the database from newest to oldest
    tasks = Todo.query.order_by(Todo.data_created).all()

    #returns the index.html file, passing its data in the form of tasks variable to the HTML file to the user
    return render_template('index.html', tasks = tasks)
  
@app.route('/delete/<int:id>')
def delete(id):
    #gets the task from the database
    task_to_delete = Todo.query.get_or_404(id)

    try:
        #deletes the task from the database
        db.session.delete(task_to_delete)

        #commits the changes to the database
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting that task'
    
#updates the tasks, need to call the methods POST and GET to update the task    
@app.route("/edit/<int:id>", methods = ['GET', 'POST'])
def edit(id):
    
    #gets the task from the database
    task = Todo.query.get_or_404(id)

    if request.method == 'POST':
       #updates the task in the database
       task.cotntent = request.form['content']
       try:
           #commits the changes to the database
           db.session.commit()
           return redirect('/')
       except:
           return 'There was an issue updating your task'
    else:
        return render_template('edited.html', task = task)


#runs the app
if __name__ == '__main__':
  app.run(debug = True)
