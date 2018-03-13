"""AlayaNotes

Usage:
  main.py [run]
  main.py initdb
"""
from flask import Flask, g
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine,Column,Integer,String,ForeignKey
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from docopt import docopt
import subprocess
import os

app = Flask(__name__)
engine = create_engine('sqlite:////tmp/alayatodo.db', convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))

db = SQLAlchemy(app)
Base = declarative_base()

Base.query = db_session.query_property()

from alayatodo import app
from alayatodo import models


class ExampleTable(Base):
	__tablename__ ='ExampleTable'
	id = Column('i',Integer,primary_key=True)

class Todo(db.Model):
    __tablename__ = "todos"
 
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer,default=None, nullable=True)
    description=db.Column(db.String,default=None, nullable=True)
    completed=db.Column(db.Integer,default=0,nullable=True)
    def __repr__(self):
	    return 'new to do table is be ini'

def _run_sql(filename):
    try:
        subprocess.check_output(
            "sqlite3 %s < %s" % (app.config['DATABASE'], filename),
            stderr=subprocess.STDOUT,
            shell=True
        )
    except subprocess.CalledProcessError, ex:
        print ex.output
        os.exit(1)

if __name__ == '__main__':
    args = docopt(__doc__)
     
    if args['initdb']:
        _run_sql('resources/database.sql')
        _run_sql('resources/fixtures.sql')
        print "AlayaTodo: Database initialized."
    else:
        app.run(use_reloader=True)
