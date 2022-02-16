from app import db

class Upload(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(200), index=True)

    def __repr__(self):
        return f'<Upload {self.filename}>'
