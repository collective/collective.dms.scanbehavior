# from AccessControl.SecurityManagement import getSecurityManager
# from DateTime import DateTime
# from datetime import datetime
# from z3c.form.interfaces import IEditForm, IAddForm
# from z3c.form.widget import ComputedWidgetAttribute
# from zope.interface import provider
from zope.interface import alsoProvides
# from zope.component import adapts
# from zope.component.hooks import getSite
from zope import schema
# from zope.schema.interfaces import IText, ISequence
# from zope.schema.interfaces import IContextAwareDefaultFactory
# from Products.CMFCore.utils import getToolByName
# from Products.CMFPlone.interfaces.siteroot import IPloneSiteRoot
from plone.autoform import directives as form
from plone.supermodel import model
from plone.dexterity.interfaces import IDexterityContent
from plone.autoform.interfaces import IFormFieldProvider
from imio.dms.scanbehavior import _


class IScan(model.Schema):

    model.fieldset(
            'scan',
            label=_(u'Scan'),
            fields=('scan_id',
                'pages_number',
                'scan_date',
                'scan_user',
                'scanner',
                ),
        )

    scan_id = schema.TextLine(
        title=_(u'scan_id',
            default=u'Scan id',
            ),
        required=False,
    )

    pages_number = schema.Int(
        title=_(u'pages_number',
            default=u'Pages numbers',
            ),
        required=False,
    )

    scan_date = schema.Datetime(
        title=_(u'scan_date',
            default=u'Scan date',
            ),
        required=False,
    )

    scan_user = schema.TextLine(
        title=_(u'scan_user',
            default=u'Scan user',
            ),
        required=False,
    )

    scanner = schema.TextLine(
        title=_(u'scanner',
            default=u'scanner',
            ),
        required=False,
    )

alsoProvides(IScan, IFormFieldProvider)

    # form.order_before(description='*')
    # form.order_before(title='*')
    # form.omitted('scanner')


# class MetadataBase(object):
    # """ This adapter uses DCFieldProperty to store metadata directly on an
        # object using the standard CMF DefaultDublinCoreImpl getters and
        # setters.
    # """
    # adapts(IDexterityContent)

    # def __init__(self, context):
        # self.context = context


# _marker = object()


# class Basic(MetadataBase):

    # def _get_title(self):
        # return self.context.title

    # def _set_title(self, value):
        # if isinstance(value, str):
            # raise ValueError('Title must be unicode.')
        # self.context.title = value
    # title = property(_get_title, _set_title)

    # def _get_description(self):
        # return self.context.description

    # def _set_description(self, value):
        # if isinstance(value, str):
            # raise ValueError('Description must be unicode.')
        # self.context.description = value
    # description = property(_get_description, _set_description)


