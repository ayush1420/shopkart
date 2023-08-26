from flask_restful import Resource
from application.models import db
from application.validation import ValidationError
from application.models import Admin,Product,User,Category
from application.parser import admin_parser,update_admin_parser,user_parser,update_user_parser,cat_parser,update_cat_parser,product_parser,update_product_parser

class AdminApi(Resource):

	
    def get(self, username):
        admin = Admin.query.filter_by(username=username).first()
        if admin is None:
            raise ValidationError(404, "UVE1006", "Such admin does not exist")
        else:
            return {
                "admin_id": admin.admin_id,
                "username": admin.username,
                "password": admin.password
            }


             

	
class CategoryApi(Resource):
    def get(self, name):
        pro = Category.query.filter_by(cat_name=name).first()
        if pro:
            return {
                "name": pro.cat_name,
                "id":pro.cat_id
            }
        else:
            raise ValidationError(404, "UVE1006", "Such Category does not exist")

    def put(self,name):
        # Editing name and password
        pro = Category.query.filter_by(cat_name=name).first()
        if pro is None:
            raise ValidationError(404, "UVE1006", "Such admin does not exist")
        else:
            args = update_cat_parser.parse_args()
            name = (
                args.get("name", None)
            )
            if name is None:
                raise ValidationError(404, "UVE1001", "name is required")

            else:
                pro.cat_name = name
                db.session.commit()
                return {"new_name": name}, 200

    def post(self):
        args = cat_parser.parse_args()
        name = (
            args.get("name", None)
            
        )
        if name is None:
            raise ValidationError(404, "UVE1001", "Category ID is required")
        
        else:
            query = Category(cat_name=name)
            db.session.add(query)
            db.session.commit()
            return {
                "name": query.cat_name,
                "id":query.cat_id
                
            }, 200


    def delete(self, name):
        pro = Category.query.filter_by(cat_name=name).first()
        if pro is None:
            raise ValidationError(404, "UVE1006", "Product does not exist")
        else:
            db.session.delete(pro)
            db.session.commit()
            return {
                "deleted_product": pro.cat_name
        }


	
class ProductApi(Resource):
    def get(self, name):
        pro = Product.query.filter_by(name=name).first()
        if pro:
            return {
                "name": pro.name,
                "unit": pro.unit,
                "rate": pro.rate,
                "quantity": pro.quantity,
                "cat_id": pro.cat_id
            }
        else:
            raise ValidationError(404, "UVE1006", "Such product does not exist")

    def put(self, name):
        # Editing name and password
        pro = Product.query.filter_by(name=name).first()
        if pro is None:
            raise ValidationError(404, "UVE1006", "Such admin does not exist")
        else:
            args = update_product_parser.parse_args()
            cat_id, pname, unit, rate, quantity = (
                args.get("cat_id", None),
                args.get("pname", None),
                args.get("unit", None),
                args.get("rate", None),
                args.get("quantity", None)
            )
            if cat_id is None:
                raise ValidationError(404, "UVE1001", "name is required")
            elif pname is None:
                raise ValidationError(404, "UVE1001", "Password is required")
            elif unit is None:
                raise ValidationError(404, "UVE1001", "Password is required")
            elif rate is None:
                raise ValidationError(404, "UVE1001", "Password is required")
            elif quantity is None:
                raise ValidationError(404, "UVE1001", "Password is required")
            else:
                pro.cat_id, pro.pname, pro.unit, pro.rate, pro.quantity = cat_id, pname, unit, rate, quantity
                db.session.commit()
                return {"new_name": pname}, 200

    def post(self):
        args = product_parser.parse_args()
        cat_id, pname, unit, rate, quantity = (
            args.get("cat_id", None),
            args.get("pname", None),
            args.get("unit", None),
            args.get("rate", None),
            args.get("quantity", None)
        )
        if cat_id is None:
            raise ValidationError(404, "UVE1001", "Category ID is required")
        elif pname is None:
            raise ValidationError(404, "UVE1001", "Product name is required")
        elif unit is None:
            raise ValidationError(404, "UVE1001", "Unit is required")
        elif rate is None:
            raise ValidationError(404, "UVE1001", "Rate is required")
        elif quantity is None:
            raise ValidationError(404, "UVE1001", "Quantity is required")
        else:
            query = Product(cat_id=cat_id, name=pname, unit=unit, rate=rate, quantity=quantity)
            db.session.add(query)
            db.session.commit()
            return {
                "username": query.name,
                "unit": unit
            }, 200


    def delete(self, name):
        pro = Product.query.filter_by(name=name).first()
        if pro is None:
            raise ValidationError(404, "UVE1006", "Product does not exist")
        else:
            db.session.delete(pro)
            db.session.commit()
            return {
                "deleted_product": pro.name
        }

