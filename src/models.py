from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()

user_favorite_people = db.Table('user_favorite_people',
                                db.Column('user_id', db.Integer,
                                          db.ForeignKey('user.id'), primary_key=True),
                                db.Column('people_id', db.Integer, db.ForeignKey(
                                    'people.id'), primary_key=True)
                                )
user_favorite_planet = db.Table('user_favorite_planet',
                                db.Column('user_id', db.Integer,
                                          db.ForeignKey('user.id'), primary_key=True),
                                db.Column('planet_id', db.Integer, db.ForeignKey(
                                    'planet.id'), primary_key=True)
                                )
user_favorite_vehicle = db.Table('user_favorite_vehicle',
                                 db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
                                 db.Column('vehicle_id', db.Integer, db.ForeignKey('vehicle.id', primary_key=True))
                                 )

class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(
        String(120), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    # is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)
    # user_favorite_planet = db.relationship(
    #     'Planet', secondary=user_favorite_planet, backref='favorite_by_user_for_planet')
    favorite_planet: Mapped[list["Planet"]] = relationship(
        secondary=user_favorite_planet,
        back_populates="favorite_by_user_for_planet")
    # user_favorite_people = db.relationship(
    #     'People', secondary=user_favorite_people, backref='favorite_by_user_for_people')
    favorite_people: Mapped[list["People"]] = relationship(
        secondary=user_favorite_people,
        back_populates="favorite_by_user_for_people")

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
            "name": self.name
        }


class Planet(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)

    favorite_by_user_for_planet: Mapped[list["User"]] = relationship(
        secondary=user_favorite_planet, back_populates="favorite_planet"
    )

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name
        }


class People(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)

    favorite_by_user_for_people: Mapped[list["User"]] = relationship(
        secondary=user_favorite_people, back_populates="favorite_people"
    )

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name
        }
