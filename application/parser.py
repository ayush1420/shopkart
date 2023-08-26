from flask_restful import reqparse

admin_parser=reqparse.RequestParser()

admin_parser.add_argument("username")
admin_parser.add_argument("password")

update_admin_parser=reqparse.RequestParser()
update_admin_parser.add_argument("name")
update_admin_parser.add_argument("password")



user_parser=reqparse.RequestParser()

user_parser.add_argument("name")
user_parser.add_argument("username")
user_parser.add_argument("password")

update_user_parser=reqparse.RequestParser()
update_user_parser.add_argument("name")
update_user_parser.add_argument("password")

cat_parser=reqparse.RequestParser()
cat_parser.add_argument("name")

update_cat_parser=reqparse.RequestParser()
update_cat_parser.add_argument("name")

product_parser=reqparse.RequestParser()
product_parser.add_argument("cat_id")
product_parser.add_argument("pname")
product_parser.add_argument("unit")
product_parser.add_argument("rate")
product_parser.add_argument("quantity")


update_product_parser=reqparse.RequestParser()
update_product_parser.add_argument("cat_id")
update_product_parser.add_argument("pname")
update_product_parser.add_argument("unit")
update_product_parser.add_argument("rate")
update_product_parser.add_argument("quantity")

