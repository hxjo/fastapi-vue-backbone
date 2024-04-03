from sqladmin import ModelView

from app.auth.models import AdminToken


class TokenAdminView(ModelView, model=AdminToken):
    column_list = "__all__"
