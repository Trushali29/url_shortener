from sqlalchemy.orm import Session
from . import keygen, models, schemas
from datetime import datetime, timedelta

'''
Generate a unique key and a secret key having key+random_key
Stores it in the database
'''
def create_db_url(db: Session, url: schemas.URLBase) -> models.URL:
    key = keygen.create_unique_random_key(db)
    secret_key = f"{key}_{keygen.create_random_key(length=8)}"
    db_url = models.URL(
        target_url = url.target_url,
        key = key,
        secret_key = secret_key
    )
    db.add(db_url)
    db.commit()
    db.refresh(db_url) 
    print("URL created successfylly and store in DB.")
    return db_url

# only URLs which are active
def get_db_url_by_key(db:Session, url_key:str) -> models.URL:
    return(
        db.query(models.URL)
        .filter(models.URL.key == url_key, 
                models.URL.is_active == True)
        .first()
    )

# to check the secret key entry in the database
def get_db_url_by_secret_key(db:Session, secret_key:str) -> models.URL:
    return(
        db.query(models.URL)
        .filter(models.URL.secret_key == secret_key, 
                models.URL.is_active)
        .first()
    )

# log clicks in the url site
def update_db_clicks(db:Session, db_url:schemas.URL) -> models.URL:
    db_url.clicks += 1
    db.commit()
    db.refresh(db_url)
    return db_url

# delete url
def deactivate_db_url(
    db: Session,
    key: str,
    secret_key: str
):

    db_url = (
        db.query(models.URL)
        .filter(
            models.URL.key == key,
            models.URL.secret_key == secret_key
        )
        .first()
    )

    if not db_url:
        return None

    if not db_url.is_active:
        return db_url

    db_url.is_active = False

    # Automatically delete after 7 days
    db_url.delete_at = (
        datetime.now() + timedelta(days=7)
    )

    db.commit()
    db.refresh(db_url)

    return db_url

# Reactivate function
def reactivate_db_url(
    db: Session,
    key: str,
    secret_key: str
):

    db_url = (
        db.query(models.URL)
        .filter(
            models.URL.key == key,
            models.URL.secret_key == secret_key
        )
        .first()
    )

    if not db_url:
        return None

    if db_url.is_active:
        return db_url

    db_url.is_active = True

    # Cancel automatic deletion
    db_url.delete_at = None

    db.commit()
    db.refresh(db_url)

    return db_url

# Delete the expried URLS
def delete_expired_urls(db: Session):

    expired_urls = (
        db.query(models.URL)
        .filter(
            models.URL.is_active == False,
            models.URL.delete_at != None,
            models.URL.delete_at <= datetime.now()
        )
        .all()
    )

    for url in expired_urls:
        db.delete(url)

    db.commit()

    return len(expired_urls)