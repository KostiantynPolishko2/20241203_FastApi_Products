from sqlalchemy.orm import Session
from models.property import Property
from abstracts.abc_property_repository import AbcPropertyRepository
from schemas.property_schema import PropertySchema
from infrastructures.weapons_exception import weaponsException404
from infrastructures.property_exceptions import property_exc_404

class PropertyRepository(AbcPropertyRepository):

    def __init__(self, db: Session):
        self.db = db

    def r_add_new_property(self, _property: Property):
        self.db.add(_property)
        # if _property.product_id:
        #     raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='failed add property')
        self.db.commit()

    def r_modify_property(self, id: int, request: PropertySchema):
        _property = self.db.query(Property).filter(Property.id == id).first()
        if not _property:
            raise weaponsException404('property id', str(id))

        request_update = request.model_dump(exclude_unset=True)
        for key, value in request_update.items():
            setattr(_property, key, value)
        self.db.commit()

    def r_get_all(self):
        properties = self.db.query(Property).all()
        if not properties:
            raise property_exc_404

        return properties