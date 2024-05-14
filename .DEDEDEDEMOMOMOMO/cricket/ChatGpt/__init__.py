from flask import Blueprint

bp = Blueprint('floor_incharge', __name__)  # Create a Blueprint object

@bp.route('/floor_incharge')
def floor_incharge():
    return 'Floor Incharge Page'
