from src.schemas.project_board import ProjectBoardRequestData, TaskCreateRequestData, TaskUpdateRequestData, TaskListRequestData, ExportProjectBoardRequestData
from src.mysql_util.models import ProjectBoards, Tasks, sql_obj, Teams, UsersTeams, Users
from src.log_conf import Logger
from fastapi import HTTPException
from sqlalchemy import select
from datetime import datetime
from uuid import uuid4

LOGGER = Logger.get_logger(__name__)


class ProjectBoardBase:
    """
    A project board is a unit of delivery for a project. Each board will have a set of tasks assigned to a user.
    """

    # create a board
    def create_board(payload: ProjectBoardRequestData):
        """
        :param request: A json string with the board details.
        {
            "name" : "<board_name>",
            "description" : "<description>",
            "team_id" : "<team id>"
            "creation_time" : "<date:time when board was created>"
        }
        :return: A json string with the response {"id" : "<board_id>"}

        Constraint:
         * board name must be unique for a team
         * board name can be max 64 characters
         * description can be max 128 characters
        """
        try:
            LOGGER.info(f"#services #project_board #ProjectBoard #create_board payload: {payload}")
            session = sql_obj.Session()
            team_details = {"name": payload.name, "description": payload.description,
                                 "team_id": payload.team_id}
            team_obj = ProjectBoards(**team_details)
            session.add(team_obj)
            session.commit()
            LOGGER.info(f"#services #project_board #ProjectBoard #create_board team id: {team_obj.id}")
            return {"id": team_obj.id}
        except Exception as err:
            LOGGER.error(f"#services #project_board #ProjectBoard #create_board error: {str(err)}")
            session.rollback()
            raise HTTPException(status_code=400, detail=f'400 Bad request error')


    # close a board
    def close_board(self, request: str) -> str:
        """
        :param request: A json string with the user details
        {
          "id" : "<board_id>"
        }

        :return:

        Constraint:
          * Set the board status to CLOSED and record the end_time date:time
          * You can only close boards with all tasks marked as COMPLETE
        """
        try:
            LOGGER.info(f"#services #project_board #ProjectBoard #create_board payload: {payload}")

            session = sql_obj.Session()
            project_board = session.query(ProjectBoards).get(payload.id)
            if project_board:
                project_board.status = 0

            session.commit()

            LOGGER.info(f"#services #project_board #ProjectBoard #create_board team id: {team_obj.id}")
            return {"id": team_obj.id}
        except Exception as err:
            LOGGER.error(f"#services #project_board #ProjectBoard #create_board error: {str(err)}")
            session.rollback()
            raise HTTPException(status_code=400, detail=f'400 Bad request error')


    # add task to board
    def add_task(payload: TaskCreateRequestData) -> str:
        """
        :param request: A json string with the task details. Task is assigned to a user_id who works on the task
        {
            "title" : "<board_name>",
            "description" : "<description>",
            "user_id" : "<team id>"
            "creation_time" : "<date:time when task was created>"
        }
        :return: A json string with the response {"id" : "<task_id>"}

        Constraint:
         * task title must be unique for a board
         * title name can be max 64 characters
         * description can be max 128 characters

        Constraints:
        * Can only add task to an OPEN board
        """
        try:
            LOGGER.info(f"#services #project_board #ProjectBoard #add_task payload: {payload}")
            session = sql_obj.Session()
            is_project_open = session.query(ProjectBoards.id).filter(ProjectBoards.id==payload.project_board_id, ProjectBoards.status==1).first() is not None
            if is_project_open:
                task_already_exists = session.query(Tasks.id).filter(Tasks.title==payload.title, Tasks.description == payload.description, Tasks.user_id == payload.user_id, Tasks.project_board_id == payload.project_board_id).first() is not None
                if not task_already_exists:
                    session = sql_obj.Session()
                    user_details = {"title": payload.title, "description": payload.description, 
                    "user_id": payload.user_id, "project_board_id": payload.project_board_id}
                    task_obj = Tasks(**user_details)
                    session.add(task_obj)
                    session.commit()
                    LOGGER.info(f"#services #project_board #ProjectBoard #add_task task_id: {task_obj.id}")
                    response = {"id": task_obj.id}
                    return response
                else:
                    response = {"success": False, "message": "Task already exists"}
                    return response

            else:
                response = {"success": False, "message": "Tasks cannot be added on Project board which is closed."}
                return response

        except Exception as err:
            LOGGER.error(f"#services #project_board #ProjectBoard #add_task Exception={str(err)}", exc_info=True)
            session.rollback()
            raise HTTPException(status_code=400, detail=f'400 Bad request error')

    # update the status of a task
    def update_task_status(payload: TaskUpdateRequestData):
        """
        :param request: A json string with the user details
        {
            "id" : "<task_id>",
            "status" : "OPEN | IN_PROGRESS | COMPLETE"
        }
        """
        try:
            LOGGER.info(f"#services #project_board #ProjectBoard #update_task_status payload: {payload}")
            task_id = payload.task_id
            tasks_statuses = ["Closed", "Open", "In Progress"]
            session = sql_obj.Session()
            task = session.query(Tasks).get(task_id)
            if task:  
                task.status = tasks_statuses.index(payload.status)
                session.commit()
                return {'success': True, "message": "Task Status updated successfully"}
            else:
                return {"success": False, "message": "Task does not exist"}
        except Exception as err:
            LOGGER.error(f"#services #project_board #ProjectBoard #update_task_status Exception={str(err)}", exc_info=True)
            raise HTTPException(status_code=400, detail=f'400 Bad request error')

    # list all open boards for a team
    def list_boards(payload: TaskListRequestData) -> str:
        """
        :param request: A json string with the team identifier
        {
          "id" : "<team_id>"
        }

        :return:
        [
          {
            "id" : "<board_id>",
            "name" : "<board_name>"
          }
        ]
        """
        try:
          LOGGER.info(f"#services #project_board #ProjectBoard #list_boards payload: {payload}...")
          session = sql_obj.Session()
          statement = select(ProjectBoards).filter(ProjectBoards.team_id==payload.task_id)
          LOGGER.info(f"#services #user_base #ProjectBoard #list_boards statement: {statement}...")
          project_board_obj = session.scalars(statement).all()

          LOGGER.info(f"#services #user_base #ProjectBoard #list_boards project_board_obj: {project_board_obj}")

          return project_board_obj
        except Exception as err:
          LOGGER.error(f"#services #user_base #ProjectBoard #create_user Exception={str(err)}", exc_info=True)
          raise HTTPException(status_code=400, detail=f'400 Bad request error')

    def export_board(payload: ExportProjectBoardRequestData) -> str:
        """
        Export a board in the out folder. The output will be a txt file.
        We want you to be creative. Output a presentable view of the board and its tasks with the available data.
        :param request:
        {
          "id" : "<board_id>"
        }
        :return:
        {
          "out_file" : "<name of the file created>"
        }
        """
        try:
            import csv 
            fields = ['User Name', 'User Display Name', 'User Bio', 'Created At'] 
            LOGGER.info(f"#services #team_base #TeamBase #remove_users_from_team payload: {payload}")
            session = sql_obj.Session()
            # query = session.query(ProjectBoards).join(ProjectBoards, ProjectBoards.team_id==Teams.id).join(Teams, UsersTeams.team_id==Teams.id).join(Users, UsersTeams.user_id==Users.id).filter(ProjectBoards.id == payload.project_board_id)
            query = session.query(Users).join(UsersTeams, UsersTeams.user_id==Users.id).join(Teams, UsersTeams.team_id==Teams.id).join(ProjectBoards, ProjectBoards.team_id==Teams.id).join(Tasks, Tasks.user_id==Users.id).filter(ProjectBoards.id == payload.project_board_id)
            LOGGER.info(f"#services #team_base #TeamBase #remove_users_from_team query: {query}")
            responses = query.all()
            csv_rows = []
            for response in responses:
                csv_rows.append([response.name, response.display_name, response.description, response.created_at])
            unique_id = datetime.now().strftime('%Y%m-%d%H-%M%S-') + str(uuid4())
            exported_filename = f"src/out/project-board-export-{unique_id}.csv"
            with open(exported_filename, 'w') as csvfile: 
                csvwriter = csv.writer(csvfile) 
                csvwriter.writerow(fields) 
                csvwriter.writerows(csv_rows)
            LOGGER.info(f"#services #team_base #TeamBase #remove_users_from_team response: {responses}")
            return {"success": True, "out_file": exported_filename}
        except Exception as err:
          LOGGER.error(f"#services #team_base #TeamBase #add_users_to_team Exception={str(err)}", exc_info=True)
          session.rollback()
          raise HTTPException(status_code=400, detail=f'400 Bad request error')
