from dal_select2.views import Select2ListView
from django.core.urlresolvers import reverse
from django.shortcuts import redirect, render
from django.utils.html import format_html
from django.views import View
from django.views.generic import CreateView
from django_tables2 import RequestConfig

from .csv_data import get_headers_and_data
from .dynamic_tables import DynamicTableBuilder
from .forms import (
    CsvFileForm,
    errors_autocomplete_factory,
    securities_autocomplete_factory,
)
from .models import CsvFile


class SecuritiesTableView(View):
    def urlify(self, file_name, security_name):
        url = reverse(
            'errors-by-security',
            kwargs={
                'file_name': file_name,
                'security_name': security_name,
            },
        )
        return format_html('<a href="{}">{}</a>', url, security_name)

    def get(self, request, file_name):
        """
        Render the CSV in table view
        """

        headers, data = get_headers_and_data(file_name)

        for d in data:
            d[0] = self.urlify(file_name, d[0])

        table_class = DynamicTableBuilder(
            name=file_name,
            headers=headers,
            meta_attrs={'class': 'paleblue'},
        )
        table = table_class([dict(zip(headers, d)) for d in data])
        RequestConfig(request).configure(table)

        return render(
            request,
            'table_view.html',
            {
                'table': table,
                'securities_form': securities_autocomplete_factory(file_name),
                'errors_form': errors_autocomplete_factory(file_name),
            },
        )

    def post(self, request, file_name):
        """
        Redirect to the correct page from autocomplete thing
        """
        if 'security_name' in request.POST:
            return redirect(
                reverse(
                    'errors-by-security',
                    kwargs={
                        'file_name': file_name,
                        'security_name': request.POST['security_name'],
                    }
                )
            )
        elif 'error_code' in request.POST:
            return redirect(
                reverse(
                    'securities-by-error',
                    kwargs={
                        'file_name': file_name,
                        'error_code': request.POST['error_code']
                    }
                )
            )
        else:
            raise ValueError('I dont know what to do')


def errors_by_security(request, file_name, security_name):
    """
    List of errors by security
    """

    error_codes, data = get_headers_and_data(file_name)

    this_security = [d for d in data if d[0] == security_name]

    errors = [
        error_codes[i] for i, is_present in enumerate(this_security[0])
        if is_present == '1'
    ]

    return render(
        request,
        'errors_by_security.html',
        {
            'security_name': security_name,
            'errors': errors,
        }
    )


def securities_by_error(request, file_name, error_code):
    """
    List of securities by error code
    """
    headers, data = get_headers_and_data(file_name)

    error_code_index = headers.index(error_code)
    securities = [
        i[0] for i in data
        if i[error_code_index] == '1'
    ]

    return render(
        request,
        'securities_by_error.html',
        {
            'error_code': error_code,
            'securities': securities,
        }
    )


class CsvFileBaseView(CreateView):
    """
    View and upload available CSV files
    """

    template_name = 'csv_files.html'
    form_class = CsvFileForm
    model = CsvFile
    success_url = '/securities/files/'

    def post(self, request, *args, **kwargs):
        print(request.FILES)

        return super().post(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['files'] = [
            {
                'name': file.name,
                'url': reverse(
                    'securities-table-view',
                    kwargs={'file_name': file.name},
                ),
            }
            for file in CsvFile.objects.all()
        ]

        return context


class SecuritiesAutoCompleteList(Select2ListView):
    """
    API used by the securities auto complete search widget
    """

    def get_list(self):
        _, data = get_headers_and_data(self.kwargs['file_name'])

        return [d[0] for d in data]


class ErrorAutoCompleteList(Select2ListView):
    """
    API used by the error codes auto complete search widget
    """

    def get_list(self):
        headers, _ = get_headers_and_data(self.kwargs['file_name'])

        return headers[1:]
