from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from tastypie.api import Api
from myBlog.api import PostResource, UserResource, TagResource, CommentResource, SearchResource
from django.contrib import admin

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

blog_api = Api(api_name='blog')
blog_api.register(PostResource())
blog_api.register(UserResource())
blog_api.register(TagResource())
blog_api.register(CommentResource())
blog_api.register(SearchResource())

urlpatterns = patterns('',
    url(r'^$', TemplateView.as_view(template_name='base.html')),

    # Examples:
    # url(r'^$', 'blog.views.home', name='home'),
    # url(r'^blog/', include('blog.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    (r'^api/', include(blog_api.urls)),
)
