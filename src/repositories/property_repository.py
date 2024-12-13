from sqlalchemy.orm import Session
from models.property import Property
from abstracts.abc_property_repository import AbcPropertyRepository

class PropertyRepository(AbcPropertyRepository):

    def __init__(self, db: Session):
        self.db = db

    def add_new_property(self, _property: Property):
        self.db.add(_property)
        # if _property.product_id:
        #     raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='failed add property')
        self.db.commit()