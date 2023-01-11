from database import *

PASSWORD_MATCH_ERROR = "Passwords does not match"
MISSING_FIELD_ERROR = "You've missed one of fields"
LOGIN_EXISTS_ERROR = "Login already exists"
EMAIL_EXISTS_ERROR = "Email already exists"
USER_NOT_FOUND_ERROR = "User not found"
INVALID_PASSWORD_ERROR = "Invalid password"

MAIN_MENU = {
    "Developer": "developer", 
    "Analyst": "analyst",
    "QA": "qa",
    "UX/UI": "ui_ux", 
    "DevOps": "dev_ops", 
    "Product Manager": "product_manager", 
    "Data Scientist": "data_scientist"
}

DEV_MENU = {
    'C#': 'c_sharp',
    'С/C++': 'cpp',
    'Erlang': 'erlang',
    'Go': 'go',
    'HTML/CSS': 'html_css',
    'Java': 'java',
    'Java Script': 'java_script',
    'Kotlin': 'kotlin',
    'Node.js': 'node_js',
    'PHP': 'php',
    'Python': 'python',
    'Ruby': 'ruby',
    'IOS Developer': 'ios',
    'Android Developer': 'android',
}

ANAL_MENU = {
    "Systems": "systems",
    "Business": "business"
}

MENU = {
    "main": MAIN_MENU,
    "developer": DEV_MENU,
    "analyst":  ANAL_MENU
}

MATCHING = {
    "java": "Java Developer",
    "go": "Golang Developer",
    "html_css": "Frontend Developer",
    "cpp": "C/C++ Developer",
    "c_sharp": "C# Developer",
    "ios": "IOS Developer",
    "java_script": "JavaScript Developer",
    "kotlin": "Kotlin Developer",
    "ruby": "Ruby on Rails Developer",
    "data_scientist": "Data Scientist",
    "dev_ops": "DevOps Engineer",
    "erlang": "Erlang Developer",
    "html_css": "HTML/CSS Developer",
    "node_js": "Node.js developer",
    "product_manager": "Product manager",
    "ruby": "Ruby on Rails Developer",
    "go": "Go Developer",
    "qa": "QA Engineer",
    "ui_ux": "UX/UI Designer",
    "php": "PHP Developer",
    "python": "Python Developer",
    "systems": "Systems analyst",
    "business": "Business analyst",
    "android": "Android Developer",
}


class UserLogin:
    def fromDB(self, user_id):
        db_user = get_values("Employers", where={"email": user_id})
        if len(db_user) != 0:
            self.user = db_user[0]
        else:
            self.user = {"email": None}
        return self

    def create(self, user):
        self.user = user
        return self

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.user['email'])