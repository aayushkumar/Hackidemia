import urlparse
from app import app
from app import db
from app import models
from app import db

from flask import jsonify
from flask import request
from flask import Flask
from flask import render_template
from flask import request

@app.route('/robots.txt')
def robots():
  res = app.make_response('User-agent: *\nAllow: /')
  res.mimetype = 'text/plain'
  return res

@app.route('/lesson')
def lesson():
  return render_template('lesson.html')

@app.route('/merchant')
def merchant():
  return render_template('merchant.html')

@app.route('/ajax', methods=["GET", "PUT", "POST"])
def for_db():
  data_dict = urlparse.parse_qs(request.data)
  print "data_dict: %s " % str(data_dict)
  print "type: %s" % data_dict['type'][0]
  print data_dict['type'][0] == 'get_material'
  if data_dict['type'][0] == 'new_material':
    name = data_dict['name'][0]
    url = data_dict.get('url')
    photo_url = data_dict.get('photo_url')
    material = models.Material(name, url, photo_url)
    db.session.add(material)
    db.session.commit()
    res = app.make_response(jsonify(data_dict))
    res.mimetype = 'text/plain'
    return res
  elif data_dict['type'][0] == 'get_material':
    material = models.Material.query.filter_by(name=data_dict['name'][0]).all() or ""
    if material != "":
      res = app.make_response("present")
    else:
      res = app.make_response(material)
    return res

@app.route('/search', methods=['GET'])
def search():
  data_dict = urlparse.parse_qs(request.data)
  query = ""
  min_age = ""
  max_age = ""

  lessons = models.Lesson.query.all()
  return render_template('index.html', lessons=lessons)


@app.route('/new_lesson', methods=['POST'])
def new_lesson():
  name = request.form['lesson_name']
  description = request.form['lesson_description']
  # TODO(aayushkumar): Error checking.
  lesson = models.Lesson(name, description)
  db.session.add(lesson)
  db.session.commit()

@app.route('/new_tutorial', methods=['POST'])
def new_tutorial():
  user_id = 1
  parent_id = 1
  cost = request.form['tutorial_cost']
  min_age = request.form['min_age']
  max_age = request.form['max_age']
  # TODO(aayushkumar): Error checking.
  lesson = models.Lesson(user_id, parent_id, cost, min_age, max_age)
  db.session.add(lesson)
  db.session.commit()

@app.route('/')
@app.route('/search')
def search():
  print request.args
  print request.args.get('result_only')
  class Result(object):
    img = 'http://lorempixel.com/400/200'
    url = '/lesson'
    title = 'Tutorial: Amorphus and Crystalline Solids?'
  results = [Result()] * 20
  chunked_results = []
  for i in xrange(0, len(results), 3):
    chunked_results.append(results[i:i+3])
  result_html = render_template('workshop-results.html', results=chunked_results)
  if request.args.get('result_only', None):
    return result_html
  return render_template('search.html', results=result_html)
