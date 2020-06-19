import graphene

from graphene_django.types import DjangoObjectType

from home.models import HomePage


class HomeType(DjangoObjectType):
    class Meta:
        model = HomePage


class HomeQuery(object):
    all_home = graphene.List(HomeType)

    home = graphene.Field(
        HomeType,
        id=graphene.Int(),
        slug=graphene.String())

    child_of = graphene.Field(
        HomeType,
        id=graphene.Int(),
        slug=graphene.String())

    def resolve_all_home(self, info, **kwargs):
        return HomePage.objects.all()

    def resolve_home(self, info, **kwargs):
        id = kwargs.get('id')
        slug = kwargs.get('slug')

        if id is not None:
            return HomePage.objects.get(pk=id)

        if slug is not None:
            return HomePage.objects.get(slug=slug)

        return None

    def resolve_child_of(self, info, **kwargs):
        id = kwargs.get('id')
        slug = kwargs.get('slug')

        if id is not None:
            parent_page = HomePage.objects.get(id=id)
            return HomePage.objects.child_of(parent_page).get()

        if slug is not None:
            parent_page = HomePage.objects.get(slug=slug)
            return HomePage.objects.child_of(parent_page).get()

        return None


class Query(HomeQuery, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query)
