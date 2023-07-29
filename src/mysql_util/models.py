from sqlalchemy import Column, Integer, String, JSON, Boolean, DateTime
from sqlalchemy.schema import ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from .connection import SQLAlchemyConnectionManager
from sqlalchemy.sql import func

sql_obj = SQLAlchemyConnectionManager()
Base = declarative_base()


class BaseModel:
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class Users(BaseModel, Base):
    __tablename__ = 'users'

    name = Column(String(64), unique=True, index=True, nullable=False)
    display_name = Column(String(64))
    description = Column(String(128))

    def __repr__(self):
        return f"users: {self.id}, name: {self.name}"


class Teams(BaseModel, Base):
    __tablename__ = 'teams'

    name = Column(String(64), unique=True, index=True, nullable=False)
    description = Column(String(128))
    status = Column(Boolean, default=True)
    admin_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    def __repr__(self):
        return f"teams: {self.id}, name: {self.name}"


class UsersTeams(BaseModel, Base):
    __tablename__ = 'users_teams'

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    team_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    def __repr__(self):
        return f"users_teams: {self.id}, users_id: {self.user_id} team_id: {self.team_id}"


class ProjectBoards(BaseModel, Base):
    __tablename__ = 'project_boards'

    name = Column(String(64), unique=True, index=True, nullable=False)
    description = Column(String(128))
    team_id = Column(Integer, ForeignKey("teams.id"), nullable=False)
    end_time = Column(DateTime(timezone=True))
    status = Column(Boolean, default=True)

    def __repr__(self):
        return f"project_boards: {self.id}, board_name: {self.name}"


class Tasks(BaseModel, Base):
    __tablename__ = 'tasks'

    title = Column(String(64), unique=True, index=True, nullable=False)
    description = Column(String(128))
    status = Column(Integer, default=1)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    project_board_id = Column(Integer, ForeignKey("project_boards.id"), nullable=False)

    def __repr__(self):
        return f"tasks: {self.id}, title: {self.title}"


Base.metadata.create_all(sql_obj.engine)
