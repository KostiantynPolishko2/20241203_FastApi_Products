from models.product import Product
from sqlalchemy.orm import Session, joinedload
from infrastructures.product_exception import *
from infrastructures.weapons_exception import weaponsException404
from abstracts.abc_weapons_repository import AbcWeaponsRepository
from models.property import Property

class SqlDbWeaponsRepository(AbcWeaponsRepository):

    def __init__(self, db: Session):
        self.db=db

    def get_all(self):
        products = self.db.query(Product).all()
        if not products:
            raise products_empty_exc

        return products

    def get_product_card_by_name(self, model: str):
        product = self.db.query(Product).options(joinedload(Product.property)).filter(Product.model == model).first()
        if not product:
            raise weaponsException404(name_obj='product', _property=model)

        return product

    def delete_product_by_name(self, model: str):
        product = self.db.query(Product).filter(Product.model == model).first()
        if not product:
            raise weaponsException404(name_obj='product', _property=model)

        self.db.delete(product)
        self.db.commit()

    def delete_product(self, product: Product):
        self.db.delete(product)
        self.db.commit()

    def add_new_product(self, product: Product)->int:
        self.db.add(product)
        self.db.commit()
        self.db.refresh(product)

        if not product.id:
            raise products_not_added_exc

        return product.id

    def add_new_property(self, _property: Property):
        self.db.add(_property)
        # if _property.product_id:
        #     raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='failed add property')
        self.db.commit()
