#ファイルはアプリ直下に作成(views.py、models.pyと同階層)

from django.contrib.sessions.models import Session

from .models import Profile

def get_current_profile(request=None):
    if not request:
        return None

    session_key = request.session.session_key
    session = Session.objects.get(session_key=session_key).get_decoded()
    uid = session.get('_auth_user_id')

    return Profile.objects.get(id=uid)