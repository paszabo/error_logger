from dal_select2.fields import Select2ListChoiceField
from dal_select2.widgets import ListSelect2
from django.core.urlresolvers import reverse
from django.forms import Form, ModelForm

from .models import CsvFile


class CsvFileForm(ModelForm):
    class Meta:
        model = CsvFile
        fields = ['name', 'file']


def securities_autocomplete_factory(file_name):
    class SecuritiesAutocompleteForm(Form):
        security_name = Select2ListChoiceField(
            widget=ListSelect2(
                url=reverse(
                    'securities-autocomplete',
                    kwargs={'file_name': file_name},
                ),
            ),
        )

    return SecuritiesAutocompleteForm()


def errors_autocomplete_factory(file_name):
    class ErrorsForm(Form):
        error_code = Select2ListChoiceField(
            widget=ListSelect2(
                url=reverse(
                    'errors-autocomplete',
                    kwargs={'file_name': file_name},
                ),
            ),
        )

    return ErrorsForm()
