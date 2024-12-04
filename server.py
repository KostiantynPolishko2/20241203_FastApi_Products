from fastapi import FastAPI, APIRouter
from exception_handlers import *

class HandleServer:
    title: str
    version: int

    def __init__(self, title: str, version = 1):
        self.title = title
        self.version = version

    def __call__(self, router: APIRouter):

        app = FastAPI(
            title=f'{self.title}Api',
            description='WebApi CRUD of Note entities',
            version=f'v{self.version}',
            docs_url='/swagger',
            contact={
                'name': 'itstep academy',
                'url': 'https://itstep.dp.ua',
                'email': 'polxs_wp31@student.itstep.org'
            },
            root_path=f'/api/v{self.version}',
            routes=router.routes)

        app.add_exception_handler(RequestValidationError, validation_exception_handler)
        app.add_exception_handler(HTTPException, http_exception_handler)
        app.add_exception_handler(Exception, base_exception_handler)

        return app