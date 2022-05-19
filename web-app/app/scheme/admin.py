from django.contrib import admin
from .models import Therm, Connection, XmlFile, RelationshipsTherm

admin.site.register(Therm)
admin.site.register(Connection)
admin.site.register(XmlFile)
admin.site.register(RelationshipsTherm)
