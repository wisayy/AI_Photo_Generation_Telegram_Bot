from tortoise import fields, Model


class User(Model):
    id = fields.BigIntField(pk=True)
    username = fields.CharField(max_length=32, null=True)
    language = fields.CharField(max_length=32, default="en")
    credits = fields.IntField(null=True, default=0)
    created_at = fields.DatetimeField(auto_now_add=True)
    orders = fields.ReverseRelation["Order"]  # Relationship to user's orders
    transactions = fields.ReverseRelation["Transaction"]  # Relationship to user's transactions

class Image(Model):  # Renamed for clarity
    id = fields.IntField(pk=True)
    url = fields.CharField(max_length=232, null=True)  # Renamed for clarity
    prompt = fields.CharField(max_length=232, null=True)
    credits = fields.IntField(null=True)
    created_at = fields.DatetimeField(auto_now_add=True)

class Order(Model):  # Renamed for consistency
    id = fields.IntField(pk=True)
    user = fields.ForeignKeyField("models.User", related_name="orders")
    image = fields.ForeignKeyField("models.Image", related_name="orders", null=True)  # Relationship to associated image
    status = fields.CharField(max_length=32)
    created_at = fields.DatetimeField(auto_now_add=True)
    processed_at = fields.DatetimeField(null=True)

class Transaction(Model):
    id = fields.IntField(pk=True)
    user = fields.ForeignKeyField("models.User", related_name="transactions")
    amount = fields.IntField()
    currency = fields.CharField(max_length=8)
    status = fields.CharField(max_length=32)
    price = fields.FloatField()
    created_at = fields.DatetimeField(auto_now_add=True)


