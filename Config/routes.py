from flask_restful import Api
from handlers.operatorHandlers import Register

def generate_routes(app):
    
    # create API.
    api = Api(app)
    #add all routes resources.
    #default page
    api.add_resource(Register, "/register")