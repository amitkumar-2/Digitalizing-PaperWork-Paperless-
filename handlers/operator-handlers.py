from flask import request
from flask_restful import Resource
from Database.models import *
import logging



class Register(Resource):
    @staticmethod
    def post():
        try:
            user = Operator(
                mobile= request.form["mobile"],
                first_name= request.form["first_name"],
                last_name= request.form["last_name"],
            )
            print(user.mobile)
            print(user.first_name)
            print(user.last_name)
        except Exception as why:
            logging.info("Either mobile number or password is wrong. " + str(why))
            return error.INVALID_INPUT_422
        if user.mobile is None:
                return error.INVALID_INPUT_422
        user_q = User.query.filter_by(mobile=user.mobile).first()
        if user_q is not None:
            return error.ALREADY_EXIST
        otp = random.randrange(0, 9999,4)
        send_otp(str(otp),user.mobile)
        unr_user = UnregisterdUser.query.filter_by(mobile=user.mobile).first()
        if unr_user is not None:
            unr_user.otp = otp
        else:
            unr_user = UnregisterdUser(mobile=user.mobile, first_name=user.first_name, last_name=user.last_name,otp=otp)
            db.session.add(unr_user)
        if request.form["dob"] != "":
            dob = request.form["dob"]
            unr_user.dob = datetime.strptime(dob, "%m/%d/%Y")
        db.session.commit()
        return {"status": "OTP sent sucsussfully to: " + str(unr_user.mobile), "mobile": str(unr_user.mobile)}