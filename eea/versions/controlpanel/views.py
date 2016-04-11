""" Views
"""
from Products.Five import BrowserView

from eea.versions.controlpanel.interfaces import IEEAVersionsPortalType
from eea.versions.controlpanel.schema import PortalType
from z3c.form import form, field
from z3c.form import button
from z3c.form.interfaces import DISPLAY_MODE
from eea.versions.config import  EEAMessageFactory as _


class EEAVersionsToolView(BrowserView):
    """ Browser view for eea versions tool
    """
    def add(self):
        """ Add new portal type
        """
        if not self.request:
            return None
        self.request.response.redirect('@@add')

    def delete(self, **kwargs):
        """ Delete portal types
        """
        ids = kwargs.get('ids', [])
        msg = self.context.manage_delObjects(ids)
        if not self.request:
            return msg
        self.request.response.redirect('@@view')

    def __call__(self, **kwargs):
        if self.request:
            kwargs.update(self.request)

        if kwargs.get('form.button.Add', None):
            return self.add()
        if kwargs.get('form.button.Delete', None):
            return self.delete(**kwargs)
        return self.index()

class AddPage(form.AddForm):
    """ Add page
    """
    fields = field.Fields(IEEAVersionsPortalType)
    fields['last_assigned_version_number'].mode = DISPLAY_MODE

    def create(self, data):
        """ Create
        """
        ob = PortalType(id=data.get('title', 'ADDTitle'))
        form.applyChanges(self, ob,  data)
        return ob

    def add(self, obj):
        """ Add
        """
        name = obj.getId()
        self.context[name] = obj
        self._finished_add = True
        return obj

    def nextURL(self):
        """ Next
        """
        return "./@@view"


class EditPage(form.EditForm):
    """ Edit page
    """
    fields = field.Fields(IEEAVersionsPortalType)
    fields['last_assigned_version_number'].mode = DISPLAY_MODE

    def nextURL(self):
        """ Next
        """
        return "../@@view"

    @button.buttonAndHandler(_(u"label_apply", default=u"Apply"),
                             name='apply')
    def handleApply(self, action):
        super(EditPage, self).handleApply(self, action)
        self.request.response.redirect(self.nextURL())

    @button.buttonAndHandler(_(u"label_cancel", default=u"Cancel"),
                             name='cancel_add')
    def handleCancel(self, action):
        self.request.response.redirect(self.nextURL())
        return ''

