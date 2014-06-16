# -*- coding: utf-8 -*-
# Created by zhangyi on 14-3-14.
from sqlalchemy import Column, INTEGER, CHAR, TEXT, BIGINT, SMALLINT, VARCHAR, TIMESTAMP

from database import Base


class Machine(Base):
    __tablename__ = 'machine'
    __table_args__ = {}

    id = Column('id', BIGINT, primary_key=True, nullable=False)
    agent = Column('agent', TEXT())
    version = Column('version', INTEGER, nullable=False, default='0')
    cpu = Column('cpu', INTEGER, nullable=False, default='0')
    ip = Column('ip', CHAR(length=32), nullable=False, default='')
    memory = Column('memory', BIGINT, nullable=False)
    disk = Column('disk', BIGINT, nullable=False)
    idc = Column('idc', CHAR(length=32))
    switcher = Column('switcher', CHAR(length=32))
    frame = Column('frame', CHAR(length=32))
    network_id = Column('network_id', BIGINT)


class Network(Base):
    __tablename__ = 'network'
    __table_args__ = {}

    id = Column('id', BIGINT, primary_key=True, nullable=False)
    mask = Column('mask', SMALLINT, nullable=False)
    gateway = Column('gateway', CHAR(length=32), nullable=False)
    ip_pool = Column('ip_pool', TEXT())


class AppVersion(Base):
    __tablename__ = 'app_version'
    __table_args__ = {}

    id = Column('id', BIGINT, primary_key=True, nullable=False)
    app_id = Column('app_id', VARCHAR(length=50), nullable=False)
    version = Column('version', VARCHAR(length=250), nullable=False)
    app_file_id = Column('app_file_id', BIGINT, nullable=False)
    creation_date = Column('creation_date', TIMESTAMP, nullable=False)
    last_modified_date = Column('last_modified_date', TIMESTAMP, nullable=False)


class Instance(Base):
    __tablename__ = 'instance'
    __table_args__ = {}

    id = Column('id', BIGINT, primary_key=True, nullable=False)
    instance_id = Column('instance_id', VARCHAR(length=80))
    instance_group_id = Column('instance_group_id', BIGINT, nullable=False)
    app_id = Column('app_id', VARCHAR(length=50), nullable=False)
    app_version = Column('app_version', VARCHAR(length=250), nullable=False)
    instance_ip = Column('instance_ip', VARCHAR(length=15))
    agent_ip = Column('agent_ip', VARCHAR(length=15))
    instance_port = Column('instance_port', INTEGER)
    type = Column('type', INTEGER, nullable=False)
    status = Column('status', INTEGER, nullable=False)
    creation_date = Column('creation_date', TIMESTAMP, nullable=False)
    last_modified_date = Column('last_modified_date', TIMESTAMP, nullable=False)


