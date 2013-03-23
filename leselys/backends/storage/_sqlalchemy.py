# -*- coding: utf-8 -*-
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from sqlalchemy.pool import QueuePool

from sqlalchemy import Column, String, Integer
from sqlalchemy import Boolean, ForeignKey, PickleType

from _storage import Storage

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String)
    password = Column(String)

    def __repr__(self):
        return "<User('%s', '%s')>" % (self.username, self.password)

class Feed(Base):
    __tablename__ = "feeds"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    url = Column(String)
    last_update = Column(PickleType)

    def __repr__(self):
        return "<Feed('%s', '%s')>" % (self.title, self.url)

class Story(Base):
    __tablename__ = "stories"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    url = Column(String)
    description = Column(String)
    published = Column(PickleType)
    last_update = Column(PickleType)
    read = Column(Boolean)
    feed_id = Column(ForeignKey('feeds.id'))

    def __repr__(self):
        return "<Story('%s', '%s')>" % (self.title, self.url)

class Setting(Base):
    __tablename__ = "settings"
    id = Column(Integer, primary_key=True)
    key = Column(String)
    value = Column(PickleType)

    def __init__(self, key, value):
        self.key = key
        self.value = value

    def __repr__(self):
        return "<Setting('%s', '%s')>" % (self.key, self.value)

class Sqlalchemy(Storage):

    def __init__(self, **kwargs):
        if not kwargs.get('uri'):
            raise Exception('SQLAlchemy backend need uri option')
        self.uri = kwargs['uri']
        self.engine = create_engine(self.uri, echo=False, convert_unicode=True)

        Base.metadata.create_all(self.engine)

        self.session = scoped_session(sessionmaker(bind=self.engine, autoflush=False))

        Base.query = self.session.query_property()

    def get_setting(self, key):
        r = self.session.query(Setting.value).filter_by(key=key).first()
        if r is None:
            return []
        else:
            return r[0]

    def set_setting(self, key, value):
        setting = Setting(key=key, value=value)
        self.session.add(setting)
        self.session.commit()

    def add_user(self, username, password):
        user = User(username=username, password=password)
        self.session.add(user)
        self.session.commit()

    def get_users(self):
        r = self.session.query(User.username).all()
        res = []
        for user in r:
            res.append(user[0])
        return res

    def remove_user(self, username):
        user = self.session.query(User).filter_by(username=username).first()
        self.session.delete(user)
        self.session.commit()

    def get_password(self, username):
        user = self.session.query(User.password).filter_by(username=username).first()
        if user:
            return user[0]

    def set_password(self, username, password):
        user = self.session.query(User).filter_by(username=username).first()
        user.password = password
        self.session.commit()

    def get_feeds(self):
        feeds = self.session.query(Feed).all()
        res = []
        for feed in feeds:
            feed = {'title': feed.title, 
                    'url': feed.url,
                    'last_update': feed.last_update,
                    '_id': str(feed.id)}
            res.append(feed)
        return res

    def get_feed_by_title(self, title):
        title = unicode(title)
        feed = self.session.query(Feed).filter(Feed.title == title).first()
        if feed:
            feed = {'title': feed.title,
                    'url': feed.url,
                    'last_update': feed.last_update,
                    '_id': str(feed.id)}
            return feed
        else:
            return False

    def get_feed_by_id(self, feed_id):
        feed = self.session.query(Feed).filter(Feed.id == feed_id).first()
        if feed:
            feed = {'title': feed.title,
                    'url': feed.url,
                    'last_update': feed.last_update,
                    '_id': str(feed.id)}
            return feed
        else:
            return False

    def add_feed(self, content):
        feed = Feed(url=content['url'], last_update=content['last_update'], title=content['title'])
        self.session.add(feed)
        self.session.commit()
        return str(feed.id)

    def remove_feed(self, feed_id):
        stories = self.session.query(Story).join(Feed).filter(Story.feed_id == feed_id)
        feed = self.session.query(Feed).filter(Feed.id == feed_id).first()
        for story in stories:
            self.session.delete(story)
        self.session.delete(feed)
        self.session.commit()

    def add_story(self, content):
        story = Story(
            title=content['title'],
            url=content['url'],
            description=content['description'],
            published=content['published'],
            last_update=content['last_update'],
            feed_id=content['feed_id'],
            read=content['read'])
        self.session.add(story)
        self.session.commit()
        return str(story.id)

    def remove_story(self, story_id):
        story = self.session.query(Story).filter(Story.id == story_id).first()
        self.session.delete(story)
        self.session.commit()

    def get_stories(self, feed_id):
        stories = self.session.query(Story).join(Feed).filter(Feed.id == feed_id).all()
        if stories:
            res = []
            for story in stories:
                print(story.feed_id)
                story = {'title': story.title,
                         'url': story.url,
                         'description': story.description,
                         'published': story.published,
                         'last_update': story.last_update,
                         'feed_id': feed_id,
                         'read': story.read,
                         '_id': str(story.id)}
                res.append(story)
            return res
        else:
            return []

    def get_story_by_id(self, story_id):
        story = self.session.query(Story).filter(Story.id == story_id).first()
        if story:
            story = {'title': story.title,
                     'url': story.url,
                     'description': story.description,
                     'published': story.published,
                     'last_update': story.last_update,
                     'feed_id': story.feed_id,
                     'read': story.read,
                     '_id': str(story.id)}
            return story
        else:
            return False

    def update_story(self, story_id, content):
        story = self.session.query(Story).filter(Story.id == story_id).first()
        if story:
            story.title = content['title']
            story.url = content['url']
            story.description = content['description']
            story.published = content['published']
            story.last_update = content['last_update']
            story.read = content['read']
            self.session.commit()
        else:
            return False

    def get_feed_unread(self, feed_id):
        feeds = self.session.query(Story).join(Feed).filter(Feed.id == feed_id).filter(Story.read == False)
        if feeds:
            res = []
            for feed in feeds:
                feed = {'_id': str(feed.id),
                        'title': feed.title,
                        'url': feed.url,
                        'last_update': feed.last_update}
                res.append(feed)
            return res
        else:
            return []

    #  WIP
    def get_settings(self):
        settings = self.session.query(Setting).all()
        if settings:
            res = {}
            for setting in settings:
                setting = {'key': setting.key,
                           'value': setting.value}
                res.update(setting)
            return res
        else:
            return {}
