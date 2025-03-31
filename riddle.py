from flask import Flask,request,jsonify
import random
from flask_sqlalchemy import SQLAlchemy


app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:uday51%40%24man@localhost/riddels'  # Replace with your MySQL credentials
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db=SQLAlchemy(app)

class Riddles_YT(db.Model):
   id=db.Column(db.Integer,primary_key=True,autoincrement=True)
   riddle=db.Column(db.String(10000), nullable=False)
   answer=db.Column(db.String(255), nullable=False)
   processed=db.Column(db.String(255), nullable=False)


 


with app.app_context():
  db.create_all()

@app.route('/add-riddle',methods=['POST'])
def addRiddle():
   data=request.get_json()
   new_riddle=Riddles_YT(riddle=data['riddle'], answer=data['answer'],processed=data['processed'] )
   db.session.add(new_riddle)
   db.session.commit()
   return jsonify("Riddle added Successfully")
   
@app.route('/get-riddle',methods=["GET"])
def getRiddle():
   riddles=Riddles_YT.query.filter_by(processed='no').all()
   if not riddles:
     return jsonify({"message":"no processed riddles"})
   random_riddle=random.choice(riddles)
   return jsonify({"id":random_riddle.id,"riddle":random_riddle.riddle,"answer":random_riddle.answer})
   
@app.route('/update-riddle/<int:id>' ,methods=['PUT'])
def update_riddle(id):
  riddle=Riddles_YT.query.get_or_404(id)
  data=request.get_json()
  riddle.processed=data.get('processed',riddle.processed)
  db.session.commit()
  return jsonify({"message":"Updated Riddle"})

@app.route('/delete-riddle/<int:id>',methods=['DELETE'])
def delete_riddle(id):
  riddle=Riddles_YT.query.get_or_404(id)
  db.session.delete(riddle)
  db.session.commit()
  return jsonify({"message":"Message Deleted"})
  



  
  
  
  
   

   


if __name__=="__main__":
   app.run(debug=True)
   
     
   
   
