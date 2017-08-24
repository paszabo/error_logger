from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^files/$', views.CsvFileBaseView.as_view(), name='csv-files-list'),
    url(
        r'^files/(?P<file_name>[A-Za-z0-9\.\-_]+)/$',
        views.SecuritiesTableView.as_view(),
        name='securities-table-view',
    ),
    url(
        r'^files/(?P<file_name>[A-Za-z0-9\.\-_]+)/securities/'
        r'(?P<security_name>.*)/$',
        views.errors_by_security,
        name='errors-by-security',
    ),
    url(
        r'^files/(?P<file_name>[A-Za-z0-9\._]+)/securities/$',
        views.SecuritiesAutoCompleteList.as_view(),
        name='securities-autocomplete',
    ),
    url(
        r'^files/(?P<file_name>[A-Za-z0-9\._]+)/errors/$',
        views.ErrorAutoCompleteList.as_view(),
        name='errors-autocomplete',
    ),
    url(
        r'^files/(?P<file_name>[A-Za-z0-9\._]+)/securities/'
        r'(?P<security_name>.*)/$',
        views.errors_by_security,
        name='errors-by-security'
    ),
    url(
        r'^files/(?P<file_name>[A-Za-z0-9\._]+)/errors/(?P<error_code>.*)/$',
        views.securities_by_error,
        name='securities-by-error',
    ),
]
