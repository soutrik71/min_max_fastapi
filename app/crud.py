from fastapi import Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app.db import get_db_session
from app.models import User, Weather
from app.schemas import UserIn, UserOut, WeatherIn, WeatherOut

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


def crud_error_message(message):
    return {"error": message}
