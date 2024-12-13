from models.product import Product
from sqlalchemy.orm import Session, joinedload
from infrastructures.product_exception import *
from infrastructures.weapons_exception import weaponsException404
from schemas.product_schema import ProductSchema, ProductSchemaModify
from abstracts.abc_product_repository import AbcProductRepository

class ProductRepository(AbcProductRepository):

    def __init__(self, db: Session):
        self.db = db

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


    def update_product(self, model: str, request: ProductSchema):
        product = self.db.query(Product).filter(Product.model == model).first()
        if not product:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f'product \'{model.upper()}\' is absent in db!')

        self.db.query(Product).filter(Product.model == model).update(request.model_dump(exclude_unset=True))
        self.db.commit()

    def modify_product(self, model: str, request: ProductSchemaModify):
        product = self.db.query(Product).filter(Product.model == model).first()
        if not product:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f'product \'{model.upper()}\' is absent in db!')

        request_update = request.model_dump(exclude_unset=True)
        for key, value in request_update.items():
            setattr(product, key, value)
        self.db.commit()