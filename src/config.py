from fastapi import FastAPI, APIRouter

class HandleServer:
    title: str
    version: int

    def __init__(self, title: str, version = 1):
        self.title = title.lower()
        self.version = version

    def __call__(self):

        app = FastAPI(
            title=f'{self.title}Api',
            description=f'WebApi CRUD of {self.title.capitalize()} entities',
            version=f'v{self.version}',
            docs_url='/swagger',
            contact={
                'name': 'itstep academy',
                'url': 'https://itstep.dp.ua',
                'email': 'polxs_wp31@student.itstep.org'
            },
            root_path=f'/api/v{self.version}/{self.title}',
        )

        return app