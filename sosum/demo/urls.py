from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('demo',
    url(r'^$', 'views.index'),
    url(r'^summarize', 'views.summarize'),
)
