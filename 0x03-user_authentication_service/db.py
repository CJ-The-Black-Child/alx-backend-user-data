#!/usr/bin/python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session

from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=True)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """
        Adds a new user to the database.

        Args:
            email (str): The user's email.
            hashed_password (str): The user's hashed password.

        Returns:
            User: The newly added user.
        """
        # user = self._session.query(User).filter_by(email=email).first()
        # if user is not None:
        #    user.hashed_password = hashed_password
        #    self._session.commit()
        #    return user

        user = User(email=email, hashed_password=hashed_password)
        self._session.add(user)
        self._session.commit()

        return user

    def find_user_by(self, **kwargs) -> User:
        """
        Finds a user in the database by the specified attributes.

        Args:
            **kwargs: The attributes to filter by.

        Returns:
            User: The found user.

        Raises:
            NoResultFound: If no user is found.
            InvalidRequestError: If no keyword arguments
            are provided or if any key does not correspond
            to a column name
        """
        if not kwargs:
            raise InvalidRequestError

        column_names = User.__table__.columns.keys()
        for key in kwargs.keys():
            if key not in column_names:
                raise InvalidRequestError

        user = self._session.query(User).filter_by(**kwargs).first()

        if user is None:
            raise NoResultFound

        return user

    def update_user(self, user_id: int, **kwargs) -> None:
        """
        Updates a user in the database.

        Args:
            user_id (int): The ID of the user to update.
            **kwargs: The attributes to update.

        Raises:
            ValueError: If any key does not correspond to a column name.
        """
        user = self.find_user_by(id=user_id)

        column_names = User.__table__.columns.keys()
        for key in kwargs.keys():
            if key not in column_names:
                raise ValueError

        for key, value in kwargs.items():
            setattr(user, key, value)

        self._session.commit()
