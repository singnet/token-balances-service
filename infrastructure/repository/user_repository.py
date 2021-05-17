from infrastructure.repository.base_repository import BaseRepository
from infrastructure.models import User, Snapshots
from sqlalchemy import exc


class UserRepository(BaseRepository):
    def create_registration(self, wallet_address, signature, email):

        user_registration = User(wallet_address=wallet_address, signature=signature, email=email)
        self.add_item(user_registration)
        return True

    def check_agi_balance(self, address):
        try:
            result = (
                self.session.query(Snapshots)
                    .filter(Snapshots.address == address)
                    .first()
            )
            self.session.commit()
        except exc.SQLAlchemyError as e:
            self.session.rollback()
            raise e

        return result or None

    def is_registered_user(self, address):
        try:
            result = (
                self.session.query(User)
                    .filter(User.wallet_address == address)
                    .first()
            )
            self.session.commit()
        except exc.SQLAlchemyError as e:
            self.session.rollback()
            raise e

        return result or None
