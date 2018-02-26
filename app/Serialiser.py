from marshmallow import Schema, fields

class PrebirthSchema(Schema):
   id = fields.Integer()
   month_no = fields.Integer()
   title = fields.String()
   article = fields.String()
   dos = fields.String()
   donts = fields.String()
   diet = fields.String()

class PostbirthSchema(Schema):
	id = fields.Integer()
	month_no = fields.Integer()
	title = fields.String()
	article = fields.String()
	dos = fields.String()
	donts = fields.String()
	diet = fields.String()

class BlogSchema(Schema):
    id = fields.Integer()
    author_email = fields.String()
    author_name = fields.String()
    title = fields.String()
    article = fields.String()
    time_created = fields.DateTime()
    keywords = fields.String()
