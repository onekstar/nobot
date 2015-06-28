# encoding:utf-8
from models.base import metadata
from models.novel import Novel
from models.chapter import Chapter 
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import sys


def main():
    e = create_engine(sys.argv[1], echo=True)
    metadata.drop_all(e)
    metadata.create_all(e)

# python create_tables.py mysql://root:123456@localhost:3306/thrall
if __name__ == "__main__":
    main()
