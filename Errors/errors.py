#!/usr/bin/python
# -*- coding: utf-8 -*-

SERVER_ERROR_500 = ({"message": "An error occured."}, 500)
NOT_FOUND_404 = ({"message": "Resource could not be found."}, 404)
NO_INPUT_400 = ({"message": "No input data provided."}, 400)
INVALID_INPUT_422 = ({"message": "Invalid input."}, 422)
INVALID_DEVICE_ID_422 = ({"message": "Invalid device ID."}, 422)
INVALID_OTP_422 = ({"message": "Invalid otp"}, 422)
INVALID_SALE_422 = ({"message": "Missing sales data"}, 422)
INVALID_USER_422 = ({"message": "User does not exist!"}, 422)
ALREADY_EXIST = ({"message": "Already exists."}, 409)
LIMIT_REACHED_409 = ({"message": "Limit reached, please upgrade your plan"}, 409)
UNAUTHORIZED = ({"message": "Wrong credentials."}, 401)
DOES_NOT_EXIST = ({"message": "Does not exists."}, 409)
NOT_ADMIN = ({"message": "Admin permission denied."}, 999)
HEADER_NOT_FOUND = ({"message": "Header does not exists."}, 999)
