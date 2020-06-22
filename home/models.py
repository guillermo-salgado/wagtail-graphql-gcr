from django.db import models

from wagtail.core import blocks
from wagtail.core.models import Page
from wagtail.snippets.blocks import SnippetChooserBlock
from wagtail.snippets.models import register_snippet
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.core.fields import RichTextField, StreamField
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel


@register_snippet
class Recipe(models.Model):
    title = models.CharField(max_length=255)
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    ingredients = StreamField([
        ('ingredient', blocks.StructBlock([
            ('name', blocks.CharBlock()),
            ('quantity', blocks.DecimalBlock()),
            ('unit', blocks.ChoiceBlock(choices=[
                ('none', '(no unit)'),
                ('g', 'Grams (g)'),
                ('ml', 'Millilitre (ml)'),
                ('tsp', 'Teaspoon (tsp.)'),
                ('tbsp', 'Tablespoon (tbsp.)'),
            ]))
        ]))
    ])
    instructions = StreamField([
        ('instruction', blocks.TextBlock()),
    ])

    panels = [
        FieldPanel('title'),
        ImageChooserPanel('image'),
        StreamFieldPanel('ingredients'),
        StreamFieldPanel('instructions'),
    ]

    objects = models.Manager()

    def __str__(self):
        return self.title


class HomePage(Page):
    body = RichTextField(blank=True)
    stream = StreamField([
        ('heading', blocks.CharBlock(classname="full title")),
        ('paragraph', blocks.RichTextBlock()),
        ('recipe', SnippetChooserBlock(Recipe)),
    ], blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('body', classname="full"),
        StreamFieldPanel('stream')
    ]


class TestPage(Page):
    test = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('test', classname="full"),
    ]
