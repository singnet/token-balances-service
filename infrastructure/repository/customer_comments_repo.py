from infrastructure.repository.base_repository import BaseRepository
from infrastructure.models import UserComments, UserAccessDetails
from datetime import datetime


class CustomerComments(BaseRepository):
    def submit_comment(self, address, comment, email, name):

        user_comment = UserComments(wallet_address=address, comment=comment)
        user_access_log = UserAccessDetails(
            wallet_address=address,
            email=email,
            name=name,
            login_time=datetime.now(),
        )

        self.add_item(user_access_log)
        self.add_item(user_comment)
        return True
