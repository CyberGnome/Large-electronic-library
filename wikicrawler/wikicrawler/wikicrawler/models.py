# -*- coding: utf-8 -*-

from datetime import datetime

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship

DeclarativeBase = declarative_base()


articles_categories_table = Table(
    'articles_categories', DeclarativeBase.metadata,
    Column('article_id', Integer, ForeignKey('article.id')),
    Column('title', String, ForeignKey('category.title')))


class WikiArticle(DeclarativeBase):
    __tablename__ = 'wiki_article'

    id = Column(Integer, primary_key=True)
    url = Column('url', String, nullable=False)
    article = Column(Integer, ForeignKey('article.id'))

    created_date = Column('created_date', DateTime, nullable=False,
                          default=datetime.utcnow)


class Article(DeclarativeBase):
    __tablename__ = 'article'

    id = Column(Integer, primary_key=True)
    title = Column('title', String, nullable=False)
    text = Column('text', String, nullable=False)
    file = Column('file', String, nullable=False)
    categories = relationship('Category', uselist=True, secondary=articles_categories_table, back_populates='articles')

    created_date = Column('created_date', DateTime, nullable=False,
                          default=datetime.utcnow)


class Category(DeclarativeBase):
    __tablename__ = 'category'

    title = Column('title', String, primary_key=True)
    article = relationship('Article', secondary=articles_categories_table, back_populates='categories')
