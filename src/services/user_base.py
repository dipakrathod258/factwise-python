from src.schemas.user_schema import UserRequestData, UserDetailsRequestData, UserUpdateRequestData
from src.mysql_util.models import Users
from src.mysql_util.models import sql_obj
from src.log_conf import Logger
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.sql.expression import update

import json

LOGGER = Logger.get_logger(__name__)


class UserBase:
    """
    Base interface implementation for API's to manage users.
    """

    # create a user
    def create_user(payload: UserRequestData) -> str:
        """
        :param request: A json string with the user details
        {
          "name" : "<user_name>",
          "display_name" : "<display name>"
        }
        :return: A json string with the response {"id" : "<user_id>"}

        Constraint:
            * user name must be unique
            * name can be max 64 characters
            * display name can be max 64 characters
        """
        try:
          LOGGER.info(f"#services #user_base #UserBase #create_user payload: {payload}")
          session = sql_obj.Session()
          user_details = {"name": payload.name, "description": payload.description, 
          "display_name": payload.display_name}
          user_obj = Users(**user_details)
          session.add(user_obj)
          session.commit()
          LOGGER.info(f"#services #user_base #UserBase #create_user user_id: {user_obj.id}")
          response = {"id": user_obj.id}
          return response
        except Exception as err:
          LOGGER.error(f"#services #user_base #UserBase #create_user Exception={str(err)}", exc_info=True)
          session.rollback()
          raise HTTPException(status_code=400, detail=f'Error - {str(err)}')

    # list all users
    def list_users() -> str:
        """
        :return: A json list with the response
        [
          {
            "name" : "<user_name>",
            "display_name" : "<display name>",
            "creation_time" : "<some date:time format>"
          }
        ]
        """
        try:
          LOGGER.info(f"#services #user_base #UserBase #list_users starts...")
          session = sql_obj.Session()
          statement = select(Users)
          LOGGER.info(f"#services #user_base #UserBase #list_users statement: {statement}...")
          user_obj = session.scalars(statement).all()

          # users = session.query(Users).order_by(-Users.id)
          LOGGER.info(f"#services #user_base #UserBase #list_users user_obj: {user_obj}")

          return user_obj
        except Exception as err:
          LOGGER.error(f"#services #user_base #UserBase #create_user Exception={str(err)}", exc_info=True)
          raise HTTPException(status_code=400, detail=f'Error - {str(err)}')

    # describe user
    def describe_user(payload: UserDetailsRequestData) -> str:
        """
        :param request: A json string with the user details
        {
          "id" : "<user_id>"
        }

        :return: A json string with the response

        {
          "name" : "<user_name>",
          "description" : "<some description>",
          "creation_time" : "<some date:time format>"
        }

        """
        try:
          LOGGER.info(f"#services #user_base #UserBase #describe_user starts...")
          session = sql_obj.Session()
          user_obj = session.query(Users).filter(Users.id==payload.id).first()
          LOGGER.info(f"#services #user_base #UserBase #describe_user statement: {user_obj}...")
          # user_obj = session.scalars(statement).all()

          # users = session.query(Users).order_by(-Users.id)
          LOGGER.info(f"#services #user_base #UserBase #describe_user user_obj: {user_obj}")

          return user_obj
        except Exception as err:
          LOGGER.error(f"#services #user_base #UserBase #create_user Exception={str(err)}", exc_info=True)
          raise HTTPException(status_code=400, detail=f'Error - {str(err)}')

    # update user
    def update_user(payload: UserUpdateRequestData) -> str:
        """
        :param request: A json string with the user details
        {
          "id" : "<user_id>",
          "user" : {
            "name" : "<user_name>",
            "display_name" : "<display name>"
          }
        }

        :return:

        Constraint:
            * user name cannot be updated
            * name can be max 64 characters
            * display name can be max 128 characters
        """
        try:
          LOGGER.info(f"#services #user_base #UserBase #update_user payload: {payload}")
          user_id = payload.id
          payload_user = payload.user
          session = sql_obj.Session()
          user = session.query(Users).get(payload.id)
          if user:  
            user.name = payload_user.name if payload_user.name else ""
            user.display_name = payload_user.display_name if payload_user else ""
            user.description = payload_user.description if payload_user else ""
            session.commit()
            return {'success': True, "message": "User updated successfully"}
          else:
            return {"success": False, "message": "User does not exist"}
        except Exception as err:
          LOGGER.error(f"#services #user_base #UserBase #create_user Exception={str(err)}", exc_info=True)
          raise HTTPException(status_code=400, detail=f'400 Bad request error')

    def get_user_teams(self, request: str) -> str:
        """
        :param request:
        {
          "id" : "<user_id>"
        }

        :return: A json list with the response.
        [
          {
            "name" : "<team_name>",
            "description" : "<some description>",
            "creation_time" : "<some date:time format>"
          }
        ]
        """
        pass

