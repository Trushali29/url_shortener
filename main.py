import validators
from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.responses import RedirectResponse, HTMLResponse
from sqlalchemy.orm import Session
from . import schemas, models, crud
from .database import SessionLocal, engine
# below URL is to deal with the URL type for manipulation and other task of URL
from starlette.datastructures import URL
from .config import get_settings
from .models import URL as URLmodels

# fastapi template modules- jinja2templates, htmlresponses, request
from fastapi.templating import Jinja2Templates

# Run cleanup of Expried URL automatically 
import asyncio
from contextlib import asynccontextmanager

async def cleanup_expired_urls():

    while True:

        db = SessionLocal()

        try:

            deleted_count = \
                crud.delete_expired_urls(db)

            if deleted_count:
                print(
                    f"Deleted {deleted_count} expired URLs."
                )

        finally:

            db.close()

        # Check once every hour
        await asyncio.sleep(60 * 60)

@asynccontextmanager
async def lifespan(app: FastAPI):

    task = asyncio.create_task(
        cleanup_expired_urls()
    )

    yield

    task.cancel()


app = FastAPI(lifespan=lifespan) 

# link the templates directory to application via jinja2
templates = Jinja2Templates(directory='templates')

# create dabase table if not exists
models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally: db.close()

def raise_bad_request(message):
    raise HTTPException(status_code=400, detail=message)

def raise_not_found(request: Request):
    message = f"URL '{request.url}' doesn't exist" 
    raise HTTPException(status_code=404, detail=message)


# Template APIs
@app.get("/", response_class=HTMLResponse)
def home(request:Request, db: Session = Depends(get_db) ):
    '''Returns a Hello World string'''
    '''Display the URL with it shorten code'''
    items = db.query(URLmodels).order_by(URLmodels.created_at.desc()).all()
    
    return templates.TemplateResponse(
        request=request,
        name="home.html",
        context={"dynamic_message":"URL Shorterner",
                 "title":"Home", 
                 "items_list":items}
    )

# Backend APIs

# add the url input 
@app.post("/url", response_model=schemas.URLInfo)
def create_url(url: schemas.URLBase, db: Session = Depends(get_db)):
    '''Takes the target URL and show the url_key with other info and a secret_key'''
    if not validators.url(url.target_url):
        raise_bad_request(message="Your provided URL is not valid")

    # status of the url added in the database
    db_url = crud.create_db_url(db=db, url=url)

    return get_admin_info(db_url)

@app.get("/{url_key}")
def forward_to_target_url( url_key: str,  
                          request: Request, 
                          db: Session = Depends(get_db) 
):
    
    ''' Forwards to your target URL '''
    # If the key exists in the database than redirect to the target url original
    db_url = crud.get_db_url_by_key(db=db, url_key= url_key)

    if not db_url:

        raise HTTPException(
            status_code=404,
            detail="Short URL does not exist."
        )


    if not db_url.is_active:

        raise HTTPException(
            status_code=410,
            detail="This short URL has been deactivated."
        )


    crud.update_db_clicks(
        db=db,
        db_url=db_url
    )


    return RedirectResponse(db_url.target_url)

    

@app.get(
        "/admin/{secret_key}",
        name="administration info",
        response_model=schemas.URLInfo
)
def get_url_info(secret_key: str, request: Request, db:Session = Depends(get_db)):
    '''Shows administrative info about your shortened URL'''

    if db_url := crud.get_db_url_by_secret_key(db, secret_key=secret_key):
        return get_admin_info(db_url)
    else:
        raise_not_found(request)

def get_admin_info(db_url: models.URL) -> schemas.URLInfo:
    base_url = URL(get_settings().base_url)
    admin_endpoint =str(app.url_path_for(
        "administration info", secret_key=db_url.secret_key))
        
    db_url.url = str(base_url.replace(path= db_url.key))
    db_url.admin_url = str(base_url.replace(path= admin_endpoint))
    return db_url


''' 
It only deactivates the url is_active:False and not totally delete it 
It is the choice of the admin creator to delete permanantely
'''
@app.patch("/admin/{key}/deactivate")
def deactivate(
    key: str,
    data: schemas.SecretKeyRequest,
    request: Request,
    db: Session = Depends(get_db)
):

    db_url = crud.deactivate_db_url(
        db=db,
        key=key,
        secret_key=data.secret_key
    )

    if not db_url:

        raise HTTPException(
            status_code=403,
            detail="Invalid secret key."
        )

    return {
        "detail": "URL deactivated successfully."
    }

@app.patch("/admin/{key}/reactivate")
def reactivate(
    key: str,
    data: schemas.SecretKeyRequest,
    request: Request,
    db: Session = Depends(get_db)
):

    db_url = crud.reactivate_db_url(
        db=db,
        key=key,
        secret_key=data.secret_key
    )

    if not db_url:

        raise HTTPException(
            status_code=403,
            detail="Invalid secret key."
        )

    return {
        "detail": "URL reactivated successfully."
    }