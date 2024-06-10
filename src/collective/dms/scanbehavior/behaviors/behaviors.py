# -*- coding: utf-8 -*-

from collective.dms.scanbehavior import _
from plone.autoform.interfaces import IFormFieldProvider
from plone.base.utils import base_hasattr
from plone.indexer import indexer
from plone.supermodel import model
from Products.ZCatalog.ZCatalogIndexes import _marker
from zope import schema
from zope.interface import alsoProvides

import datetime


class IScanFields(model.Schema):

    model.fieldset(
        "scan",
        label=_("Scan"),
        fields=(
            "scan_id",
            "version",
            "pages_number",
            "scan_date",
            "scan_user",
            "scanner",
            "to_sign",
            "signed",
        ),
    )

    scan_id = schema.TextLine(
        title=_(
            "scan_id",
            default="Scan id",
        ),
        required=False,
    )

    version = schema.Int(title=_("Version"), required=False, default=0)

    pages_number = schema.Int(
        title=_(
            "pages_number",
            default="Pages numbers",
        ),
        required=False,
    )

    scan_date = schema.Datetime(
        title=_(
            "scan_date",
            default="Scan date",
        ),
        required=False,
        min=datetime.datetime(1990, 1, 1),
        max=datetime.datetime.today() + datetime.timedelta(days=7),
    )

    scan_user = schema.TextLine(
        title=_(
            "scan_user",
            default="Scan user",
        ),
        required=False,
    )

    scanner = schema.TextLine(
        title=_(
            "scanner",
            default="scanner",
        ),
        required=False,
    )

    to_sign = schema.Bool(
        title=_("To sign?"),
        default=False,
        required=False,
    )

    signed = schema.Bool(
        title=_("Signed version"),
        default=False,
        required=False,
    )


alsoProvides(IScanFields, IFormFieldProvider)


@indexer(IScanFields)
def scan_id_indexer(obj):
    """
    indexer method
    """
    if base_hasattr(obj, "scan_id") and obj.scan_id:
        return obj.scan_id
    return _marker
