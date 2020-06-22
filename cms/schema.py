import string
import graphene

from wagtail.core.models import Page
from wagtail.core.fields import StreamField

from graphene.types import Scalar
from graphene.types.generic import GenericScalar
from graphene_django.types import DjangoObjectType
from graphene_django.converter import convert_django_field

from home.models import HomePage, Recipe


class GenericStreamFieldType(Scalar):
    @staticmethod
    def serialize(stream_value):
        return stream_value.stream_data


@convert_django_field.register(StreamField)
def convert_stream_field(field, registry=None):
    return GenericStreamFieldType(
        description=field.help_text, required=not field.null
    )


class DefaultStreamBlock(graphene.ObjectType):
    block_type = graphene.String()
    value = GenericScalar()


def create_stream_field_type(field_name, **kwargs):
    block_type_handlers = kwargs.copy()

    class Meta:
        types = (DefaultStreamBlock, ) + tuple(
            block_type_handlers.values())

    StreamFieldType = type(
        f"{string.capwords(field_name, sep='_').replace('_', '')}Type",
        (graphene.Union,),
        dict(Meta=Meta))

    def convert_block(block):
        block_type = block.get('type')
        value = block.get('value')
        if block_type in block_type_handlers:
            handler = block_type_handlers.get(block_type)
            if isinstance(value, dict):
                return handler(value=value, block_type=block_type, **value)
            else:
                return handler(value=value, block_type=block_type)
        else:
            return DefaultStreamBlock(value=value, block_type=block_type)

    # We also generate the resolver function for the field
    def resolve_field(self, info):
        field = getattr(self, field_name)
        return [convert_block(block) for block in field.stream_data]

    return (graphene.List(StreamFieldType), resolve_field)


class RecipeNode(DjangoObjectType):
    class Meta:
        model = Recipe


class ParagraphBlock(DefaultStreamBlock):
    value = GenericScalar()


class HeadingBlock(DefaultStreamBlock):
    value = GenericScalar()


class RecipeBlock(DefaultStreamBlock):
    recipe = graphene.Field(RecipeNode)

    def resolve_recipe(self, info):
        return Recipe.objects.get(id=self.value)


class HomeType(DjangoObjectType):
    (stream, resolve_stream) = create_stream_field_type(
        'stream',
        paragraph=ParagraphBlock,
        heading=HeadingBlock,
        recipe=RecipeBlock)

    class Meta:
        model = HomePage


class HomeQuery():
    all_home = graphene.List(HomeType)

    home = graphene.Field(
        HomeType,
        id=graphene.Int(),
        slug=graphene.String())

    child_of = graphene.List(
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
            return HomePage.objects.child_of(parent_page)

        if slug is not None:
            parent_page = HomePage.objects.get(slug=slug)
            return HomePage.objects.child_of(parent_page)

        return None


class Query(HomeQuery, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query)
