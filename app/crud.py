from fastapi import Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app.db import get_db_session
from app.models import Nested, User, Weather
from app.schemas import NestedIn, UserIn, UserOut, WeatherIn, WeatherOut

DB: Session = Depends(get_db_session)


def crud_add_user(user: UserIn, db: Session = DB):

    db_user = User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def crud_get_user(user_id: int, db: Session = DB):

    user = db.query(User).filter(User.id == user_id).first()
    if user:
        return UserOut(**user.__dict__)
    return None


def crud_add_weather(weather: WeatherIn, db: Session = DB):

    db_weather = Weather(**weather.dict())
    exist = (
        db.query(Weather)
        .filter(Weather.city == weather.city, Weather.date == weather.date)
        .first()
    )
    if exist:
        return None
    db.add(db_weather)
    db.commit()
    db.refresh(db_weather)
    return db_weather


def crud_get_weather(city: str, db: Session = DB):

    weather = (
        db.query(Weather)
        .filter(Weather.city == city)
        .order_by(Weather.date.desc())
        .limit(7)
        .all()
    )
    if weather:
        result = []
        for item in weather:
            result.append(WeatherOut(**item.__dict__))
        return {city: result[::-1]}

    return None


def crud_add_nested(nested: NestedIn, db: Session = DB):

    db_nested = Nested(**nested.dict())
    db.add(db_nested)
    db.commit()
    db.refresh(db_nested)
    return db_nested


def crud_update_nested(nested: NestedIn, db: Session = DB):

    db_nested = (
        db.query(Nested).filter(Nested.input_token == nested.input_token).first()
    )
    if db_nested:
        db_nested.output = nested.output
        db.commit()
        db.refresh(db_nested)
        return db_nested
    return None


def crud_error_message(message):
    return {"error": message}
