from tastypie.resources import ModelResource
from myBlog.models import Post, Tag, Comment
from tastypie import fields
from django.contrib.auth.models import User
from tastypie.authentication import Authentication
from tastypie.authorization import  Authorization
from tastypie.resources import ALL, ALL_WITH_RELATIONS
from django.conf.urls.defaults import *
from tastypie.utils import trailing_slash
from tastypie.serializers import Serializer


class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        resource_name = 'user'
        fields = ['username']
        # detail_uri_name = 'username'
        filtering = {
            'username':ALL,
        }
        authentication = Authentication()
        authorization = Authorization()


class TagResource(ModelResource):
    post = fields.ToManyField('myBlog.api.PostResource', 'post_set', null=True )

    class Meta:
        queryset = Tag.objects.all()
        resources_name = 'tag'
        authorization = Authorization()
        authentication =  Authentication()
        list_allowed_methods = ['get', 'post']    
        detail_allowed_methods = ['get', 'post', 'put', 'delete']

        filtering = {
            'name': ALL_WITH_RELATIONS,
        }


class CommentResource(ModelResource):
    user = fields.ForeignKey(UserResource, 'user')
    post = fields.ForeignKey('myBlog.api.PostResource', 'post')

    class Meta:
        queryset = Comment.objects.all()
        # detail_uri_name = 'text'
        authorization = Authorization()
        authentication =  Authentication()

        filtering = {
            'text': ALL_WITH_RELATIONS,
        }


class PostResource(ModelResource):
    user = fields.ForeignKey(UserResource, 'user')
    tag = fields.ToManyField(TagResource, 'tag', related_name='post', null=True, full=True)
    comment = fields.ToManyField(CommentResource, 'comment_set', related_name='post', null=True, full=True)
    always_return_data = True

    class Meta:
    	queryset = Post.objects.all()
    	resources_name = 'post'
        serializer = Serializer(formats=['json'])
        authorization = Authorization()
        authentication =  Authentication()
        filtering = {
            'title': ALL_WITH_RELATIONS,
            'content' : ALL_WITH_RELATIONS,
            'tag': ALL_WITH_RELATIONS,
            'comment':ALL_WITH_RELATIONS,
        }

    def save_m2m(self, bundle):
        for field_name, field_object in self.fields.items():
            if not getattr(field_object, 'is_m2m', False):
                continue

            if not field_object.attribute:
                continue

            if field_object.readonly:
                continue

            related_mngr = getattr(bundle.obj, field_object.attribute)

            related_objs = []

            for related_bundle in bundle.data[field_name]:
                # See if this person already exists in the database
                try:
                    tag = Tag.objects.get(name=related_bundle.obj.name)
                # If it doesn't exist, then save and use the object TastyPie
                # has already prepared for creation
                except Tag.DoesNotExist:
                    tag = related_bundle.obj
                    tag.save()

                related_objs.append(tag)

            related_mngr.add(*related_objs)


class SearchResource(ModelResource):
    class Meta:
        resources_name = 'search'

    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>%s)%s$" % (self._meta.resource_name, trailing_slash()), self.wrap_view('get_search'), name="api_get_search"),
        ]

    def get_search(self, request, **kwargs):

        toSearch = request.GET.get('q', '')

        objects = []

        postTitle = Post.objects.filter(title__contains=toSearch)
        postContent = Post.objects.filter(content__contains=toSearch)
        tagName = Tag.objects.filter(name__contains=toSearch)
        comment = Comment.objects.filter(text__contains=toSearch)
        tagPost = Post.objects.filter(tag=tagName)

        objects.append({'PostTitle: ':postTitle})
        objects.append({'PostContent':postContent})
        objects.append({'Tag: ':tagName})
        objects.append({'TagPost':tagPost})
        objects.append({'Comment':comment})

        return self.create_response(request, objects)
