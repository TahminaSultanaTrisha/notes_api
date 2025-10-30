from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Connect to a local SQLite database file
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///notes.db'
db = SQLAlchemy(app)

# Define a Note model (table)
class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    content = db.Column(db.String(500))

# Routes (API endpoints)
@app.route('/notes', methods=['GET'])
def get_notes():
    notes = Note.query.all()
    return jsonify([{'id': n.id, 'title': n.title, 'content': n.content} for n in notes])

@app.route('/notes', methods=['POST'])
def add_note():
    data = request.get_json()
    note = Note(title=data['title'], content=data['content'])
    db.session.add(note)
    db.session.commit()
    return jsonify({'message': 'Note added successfully!'}), 201

@app.route('/notes/<int:id>', methods=['PUT'])
def update_note(id):
    note = Note.query.get_or_404(id)
    data = request.get_json()
    note.title = data['title']
    note.content = data['content']
    db.session.commit()
    return jsonify({'message': 'Note updated successfully!'})

@app.route('/notes/<int:id>', methods=['DELETE'])
def delete_note(id):
    note = Note.query.get_or_404(id)
    db.session.delete(note)
    db.session.commit()
    return jsonify({'message': 'Note deleted successfully!'})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # create the database file if it doesn't exist
    app.run(debug=True)