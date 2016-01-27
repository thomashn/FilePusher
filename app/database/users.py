from .entries import User
from .connection import Basic
from .security import generateSalt,addSalt,doHash


class UserTable(Basic):
    def __init__(self,database):
        Basic.__init__(self,database)
    """Manages the user accounts for the web server.

    This class handles typical user account stuff; adding users,
    removing user and authenticating users."""

    def create(self):
        """Creates the table that holds the userdata"""
        cmd = ("CREATE TABLE users (id INTEGER PRIMARY KEY, "
            "username, password, salt)")
        self.cursor.execute(cmd)
        self.db.commit()
    
    def addUser(self,username,password):
        """Adds a user to the list"""
        # Hide password using a salt and hashing 
        password,salt = self.__hidePassword(password)
        # Add username, hidden password and the salt to the database
        cmd = ("INSERT INTO users (username, password, salt) VALUES (?,?,?)")
        self.cursor.execute(cmd,(username,password,salt)) 
        self.db.commit()

    def removeUserWithName(self,username):
        return None

    def getUserWithName(self,username):
        """Returns a User object that matches the given name"""
        cmd = ("SELECT * FROM users WHERE username=?")
        self.cursor.execute(cmd,(username,))
        result = self.cursor.fetchone()
        if result:
                return self.__parseUser(result)
        else: 
                return None
    
    def authenticateUser(self,username,password):
        """Returns true if a match is found"""
        # Returns the user id when given credentials are in the database
        user = self.getUserWithName(username)
        if user:
                saltyPassword = addSalt(password,user.salt)
                hashyPassword = doHash(saltyPassword)
                if user.password == hashyPassword:
                        return user
        return None

    # Utilities
    def __parseUser(self,entryTuple):
        if entryTuple:
                id,username,password,salt = entryTuple
                return User(id,username,password,salt)

    def __hidePassword(self,password):
        """Secures a password so it can be added to a database."""
        salt = generateSalt()
        saltedPassword = addSalt(password,salt)
        return (doHash(saltedPassword),salt)

