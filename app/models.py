from app import db

class User(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(80))
  email = db.Column(db.String(120), unique=True)
  tutorials = db.relationship('Tutorial', backref='user',
                              lazy='dynamic')

  def __init__(self, name, email):
    self.name = name
    self.email = email

  def __repr__(self):
    return '<Name %r>' % self.name

tutorial_materials = db.Table('tutorial_materials',
    db.Column('material_id', db.Integer, db.ForeignKey('material.id')),
    db.Column('tutorial_id', db.Integer, db.ForeignKey('tutorial.id'))
)

class Material(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(80))
  url = db.Column(db.String(80))
  photo_url = db.Column(db.String(80))
  upcs = db.relationship('UPCCode', backref='material',
                         lazy='dynamic')
  tutorials = db.relationship('Tutorial', secondary=tutorial_materials,
        backref=db.backref('materials', lazy='dynamic'))

  def __init__(self, name, url, photo_url):
    self.name = name
    self.url = url
    self.photo_url = photo_url

  def __repr__(self):
    return '<Name %r>' % self.name

class UPCCode(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  code = db.Column(db.Integer, unique=True)
  material_id = db.Column(db.Integer, db.ForeignKey('material.id'))

  def __init__(self, code, material_id):
    self.code = code
    self.material_id = material_id

  def __repr__(self):
    return '<Code %r>' % self.code

class Lesson(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(200), unique=True)
  description = db.Column(db.String(5000), unique=True)
  tutorials = db.relationship('Tutorial', backref='lesson',
                              lazy='dynamic')

  def __init__(self, name, description):
    self.name = name
    self.description = description

  def __repr__(self):
    return '<Name %r>' % self.name

class Topic(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(200), unique=True)
  tutorial_id = db.Column(db.Integer, db.ForeignKey('tutorial.id'))
  content = db.String(999999)
  multimedias = db.relationship('Multimedia', backref='topic',
                                lazy='dynamic')

  def __init__(self, name, tutorial_id, content):
    self.name = name
    self.tutorial_id = tutorial_id
    self.content = content


class Multimedia(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  url = db.Column(db.String(2000), unique=True)
  topic_id = db.Column(db.Integer, db.ForeignKey('topic.id'))

  def __init__(self, url, topic_id):
    self.url = url
    self.topic_id = topic_id


class Tutorial(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
  parent_id = db.Column(db.Integer, db.ForeignKey('lesson.id'))
  topics = db.relationship('Topic', backref='tutorial',
                           lazy='dynamic')
  cost = db.Column(db.Integer)
  min_age = db.Column(db.Integer)
  max_age = db.Column(db.Integer)

  def __init__(self, user_id, parent_id, cost, min_age, max_age):
    self.user_id = user_id
    self.parent_id = parent_id
    self.cost = cost
    self.min_age = min_age
    self.max_age = max_age

