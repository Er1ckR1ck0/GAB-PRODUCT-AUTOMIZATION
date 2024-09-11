import http

from seam import Seam
from lock import locks
from app.models.event import Event

seam = Seam(api_key="seam_2HLW2Eme_6Xwzbq2nN9GvQXiKzRqJgQYi")

def create_access_code(event: Event, user: ):
    if
    lock_list = ((locks[lock] for lock in locks if locks[lock] == event.DATA.branch_id)
                if event.DATA.branch_id in locks else raise http.HTTPStatus.NOT_FOUND)
    try:


