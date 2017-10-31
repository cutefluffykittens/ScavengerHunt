import user

class Team(user.User):
    def __init__(self,n,u,p):
        self.name = n
        self.username = u
        self.password = p
