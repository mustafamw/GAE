from protorpc import messages

class Department(messages.Enum):
    ADMIN = 1
    MANAGEMENT = 2
    FLOOR = 3
    ACCOUNTS = 4
    
class Team(messages.Enum):
    BLUE = 1
    BLACK = 2
    RED = 3


class CompanyTypeHelper():
    
    @staticmethod
    def get_department_type(department_type):
        
        if department_type == 1:
            return Department.ADMIN
        elif department_type == 2:
            return Department.MANAGEMENT
        elif department_type == 3:
            return Department.FLOOR
        elif department_type == 4:
            return Department.ACCOUNTS
        
        return Department.ADMIN

    @staticmethod
    def get_team_type(team_type):
        
        if team_type == 1:
            return Team.BLUE
        elif team_type == 2:
            return Team.BLACK
        elif team_type == 3:
            return Team.RED
        
        return Team.BLUE