from marshmallow import Schema, fields

class PrebirthSchema(Schema):
   id = fields.Integer()
   month_no = fields.Integer()
   article = fields.String()
   dos = fields.String()
   donts = fields.String()
   diet = fields.String()

class PostbirthSchema(Schema):
	id = fields.Integer()
	month_no = fields.Integer()
	article = fields.String()
	dos = fields.String()
	donts = fields.String()
	diet = fields.String()