# -*- encoding: utf-8 -*-
import colander


class ProfileSchema(colander.MappingSchema):
    role = colander.SchemaNode(colander.String(),
                               validator=colander.OneOf(['Healer', 'DPS']),
                               missing=None)
    listed_3s = colander.SchemaNode(colander.Boolean(), missing=None)
    listed_2s = colander.SchemaNode(colander.Boolean(), missing=None)
