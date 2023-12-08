from flask_restful import Api
from handlers.operatorHandlers import Home, Register, Reference

def generate_routes(app):
    
    # create API.
    api = Api(app)
    #add all routes resources.
    #default page
    api.add_resource(Home, "/")
    
    # Register Page
    api.add_resource(Register, "/register")
    
    # Reference Page
    api.add_resource(Reference, "/reference")