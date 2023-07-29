from src.schemas.team_schema import TeamRequestData, TeamDetailsRequestData, TeamUpdateRequestData, UsersTeamsRequestData, TeamDetailsRequestData
from src.mysql_util.models import Teams, UsersTeams, Users
from src.log_conf import Logger
from src.mysql_util.models import sql_obj
from fastapi import HTTPException
from sqlalchemy import select, delete

LOGGER = Logger.get_logger(__name__)

class TeamBase:
    """
    Base interface implementation for API's to manage teams.
    For simplicity a single team manages a single project. And there is a separate team per project.
    Users can be
    """

    # create a team
    def create_team(payload: TeamRequestData) -> str:
        """
        :param request: A json string with the team details
        {
          "name" : "<team_name>",
          "description" : "<some description>",
          "admin": "<id of a user>"
        }
        :return: A json string with the response {"id" : "<team_id>"}

        Constraint:
            * Team name must be unique
            * Name can be max 64 characters
            * Description can be max 128 characters
        """
        try:
          LOGGER.info(f"#services #team_base #TeamBase #create_team payload: {payload}")
          session = sql_obj.Session()
          team_details = {"name": payload.name, "description": payload.description, 
          "admin_id": payload.admin}
          team_obj = Teams(**team_details)
          session.add(team_obj)
          session.commit()
          LOGGER.info(f"#services #user_base #UserBase #create_user team_id: {team_obj.id}")
          response = {"id": team_obj.id}
          return response
        except Exception as err:
          LOGGER.error(f"#services #user_base #UserBase #create_user Exception={str(err)}", exc_info=True)
          session.rollback()
          raise HTTPException(status_code=400, detail=f'400 Bad request error')

    # list all teams
    def list_teams() -> str:
        """
        :return: A json list with the response.
        [
          {
            "name" : "<team_name>",
            "description" : "<some description>",
            "creation_time" : "<some date:time format>",
            "admin": "<id of a user>"
          }
        ]
        """
        try:
          LOGGER.info(f"#services #user_base #TeamBase #list_teams starts...")
          session = sql_obj.Session()
          statement = select(Teams)
          LOGGER.info(f"#services #user_base #TeamBase #list_teams statement: {statement}...")
          team_obj = session.scalars(statement).all()

          LOGGER.info(f"#services #user_base #TeamBase #list_teams team_obj: {team_obj}")

          return team_obj
        except Exception as err:
          LOGGER.error(f"#services #user_base #TeamBase #list_teams Exception={str(err)}", exc_info=True)
          raise HTTPException(status_code=400, detail=f'400 Bad request error')

    # describe team
    def describe_team(payload: TeamDetailsRequestData) -> str:
        """
        :param request: A json string with the team details
        {
          "id" : "<team_id>"
        }

        :return: A json string with the response

        {
          "name" : "<team_name>",
          "description" : "<some description>",
          "creation_time" : "<some date:time format>",
          "admin": "<id of a user>"
        }

        """
        try:
          LOGGER.info(f"#services #user_base #TeamBase #describe_team starts...")
          session = sql_obj.Session()
          team_obj = session.query(Teams).filter(Teams.id==payload.id).first()
          LOGGER.info(f"#services #user_base #TeamBase #describe_team team_obj: {team_obj}")

          return team_obj
        except Exception as err:
          LOGGER.error(f"#services #user_base #TeamBase #describe_team Exception={str(err)}", exc_info=True)
          raise HTTPException(status_code=400, detail=f'400 Bad request error')

    # update team
    def update_team(payload: TeamUpdateRequestData) -> str:
        """
        :param request: A json string with the team details
        {
          "id" : "<team_id>",
          "team" : {
            "name" : "<team_name>",
            "description" : "<team_description>",
            "admin": "<id of a user>"
          }
        }

        :return:

        Constraint:
            * Team name must be unique
            * Name can be max 64 characters
            * Description can be max 128 characters
        """
        try:
          LOGGER.info(f"#services #team_base #TeamBase #update_team payload: {payload}")
          user_id = payload.id
          payload_team = payload.team
          session = sql_obj.Session()
          team = session.query(Teams).get(payload.id)
          if team:  
            team.name = payload_team.name if payload_team.name else ""
            team.description = payload_team.description if payload_team else ""
            team.admin_id = payload_team.admin if payload_team else ""
            session.commit()
            return {'success': True, "message": "Team updated successfully"}
          else:
            return {"success": False, "message": "Team does not exist"}
        except Exception as err:
          LOGGER.error(f"#services #team_base #TeamBase #update_team Exception={str(err)}", exc_info=True)
          raise HTTPException(status_code=400, detail=f'400 Bad request error')

    # add users to team
    def add_users_to_team(payload: UsersTeamsRequestData):
        """
        :param request: A json string with the team details
        {
          "id" : "<team_id>",
          "users" : ["user_id 1", "user_id2"]
        }

        :return:

        Constraint:
        * Cap the max users that can be added to 50
        """
        try:
            LOGGER.info(f"#services #team_base #TeamBase #add_users_to_team payload: {payload}")
            session = sql_obj.Session()
            payload_users = payload.users
            if payload_users:
                if len(payload_users) > 50:
                    payload_users = payload_users[:50]

                for user_id in payload_users:
                    exists = session.query(UsersTeams.id).filter(UsersTeams.team_id==payload.team_id, UsersTeams.user_id==user_id).first() is not None

                    LOGGER.info(f"#services #team_base #TeamBase #add_users_to_team exists: {exists}")
                    if not exists:
                        user_team_details = {"team_id": payload.team_id, "user_id": user_id}
                        user_team_obj = UsersTeams(**user_team_details)
                        session.add(user_team_obj)
                        session.commit()
                        LOGGER.info(f"#services #team_base #TeamBase #add_users_to_team team_id: {user_team_obj.id}")
                response = {"success": True}
                return response
            else:
                LOGGER.info(f"#services #team_base #TeamBase #add_users_to_team users list cannot be empty payload_users: {payload_users}")
                response = {"success": False, "message": "users list cannot be empty"}
                return response

        except Exception as err:
          LOGGER.error(f"#services #team_base #TeamBase #add_users_to_team Exception={str(err)}", exc_info=True)
          session.rollback()
          raise HTTPException(status_code=400, detail=f'400 Bad request error')

    # add users to team
    def remove_users_from_team(payload: UsersTeamsRequestData):
        """
        :param request: A json string with the team details
        {
          "id" : "<team_id>",
          "users" : ["user_id 1", "user_id2"]
        }

        :return:

        Constraint:
        * Cap the max users that can be added to 50
        """
        try:
            LOGGER.info(f"#services #team_base #TeamBase #remove_users_from_team payload: {payload}")
            session = sql_obj.Session()
            payload_users = payload.users
            if payload_users:
                for user_id in payload_users:
                    exists = session.query(UsersTeams.id).filter(UsersTeams.team_id==payload.team_id, UsersTeams.user_id==user_id).first() is not None

                    LOGGER.info(f"#services #team_base #TeamBase #add_users_to_team exists: {exists}")
                    if not exists:
                        continue

                    delete(UsersTeams).where(UsersTeams.team_id==payload.team_id, UsersTeams.user_id==user_id)
                    LOGGER.info(f"#services #team_base #TeamBase #add_users_to_team team_id: {payload.team_id}")
                response = {"success": True}
                return response
            else:
                LOGGER.info(f"#services #team_base #TeamBase #add_users_to_team users list cannot be empty payload_users: {payload_users}")
                response = {"success": False, "message": "users list cannot be empty"}
                return response

        except Exception as err:
          LOGGER.error(f"#services #team_base #TeamBase #add_users_to_team Exception={str(err)}", exc_info=True)
          session.rollback()
          raise HTTPException(status_code=400, detail=f'400 Bad request error')

    # list users of a team
    def list_team_users(payload: TeamDetailsRequestData):
        """
        :param request: A json string with the team identifier
        {
          "id" : "<team_id>"
        }

        :return:
        [
          {
            "id" : "<user_id>",
            "name" : "<user_name>",
            "display_name" : "<display name>"
          }
        ]
        """
        try:
            LOGGER.info(f"#services #team_base #TeamBase #remove_users_from_team payload: {payload}")
            session = sql_obj.Session()
            query = session.query(Users).join(UsersTeams, UsersTeams.user_id==Users.id).join(Teams, UsersTeams.team_id==Teams.id).filter(Teams.id == payload.id)
            LOGGER.info(f"#services #team_base #TeamBase #remove_users_from_team query: {query}")
            response = query.all()
            return response

        except Exception as err:
          LOGGER.error(f"#services #team_base #TeamBase #add_users_to_team Exception={str(err)}", exc_info=True)
          session.rollback()
          raise HTTPException(status_code=400, detail=f'400 Bad request error')


