import textwrap
from functools import cached_property

import strawberry
from django.db import models
from strawberry.printer import print_schema

from strawberry_django_plus import gql


class MyModel(models.Model):
    class Meta:
        app_label = "tests"

    id = models.BigAutoField(  # noqa: A003
        primary_key=True,
    )

    @property
    def some_property(self) -> str:
        """Some property doc."""
        return "some_value"

    @cached_property
    def some_cached_property(self) -> str:
        """Some cached property doc."""
        return "some_value"

    @gql.model_property
    def some_model_property(self) -> str:
        """Some model property doc."""
        return "some_value"


class AnotherModel(models.Model):
    class Meta:
        app_label = "tests"

    id = models.BigAutoField(  # noqa: A003
        primary_key=True,
    )

    @property
    def some_property(self) -> str:
        """Some property doc."""
        return "some_value"

    @cached_property
    def some_cached_property(self) -> str:
        """Some cached property doc."""
        return "some_value"

    @gql.model_property
    def some_model_property(self) -> str:
        """Some model property doc."""
        return "some_value"


def test_property():
    @strawberry.type
    class CommonType:
        id: strawberry.ID

    @gql.django.type(MyModel)
    class MyType:
        some_property: gql.auto

    @gql.django.type(AnotherModel)
    class AnotherType(CommonType):
        some_property: gql.auto

    @strawberry.type
    class Query:
        some_type: MyType
        another_type: AnotherType

    expected_representation = '''
    type AnotherType {
      id: ID!

      """Some property doc."""
      someProperty: String!
    }

    type MyType {
      """Some property doc."""
      someProperty: String!
    }

    type Query {
      someType: MyType!
      anotherType: AnotherType!
    }
    '''

    schema = strawberry.Schema(Query)
    assert print_schema(schema) == textwrap.dedent(expected_representation).strip()


def test_cached_property():
    @gql.django.type(MyModel)
    class MyType:
        some_cached_property: gql.auto

    @strawberry.type
    class Query:
        some_type: MyType

    expected_representation = '''
    type MyType {
      """Some cached property doc."""
      someCachedProperty: String!
    }

    type Query {
      someType: MyType!
    }
    '''

    schema = strawberry.Schema(Query)
    assert print_schema(schema) == textwrap.dedent(expected_representation).strip()


def test_model_property():
    @gql.django.type(MyModel)
    class MyType:
        some_model_property: gql.auto

    @strawberry.type
    class Query:
        some_type: MyType

    expected_representation = '''
    type MyType {
      """Some model property doc."""
      someModelProperty: String!
    }

    type Query {
      someType: MyType!
    }
    '''

    schema = strawberry.Schema(Query)
    assert print_schema(schema) == textwrap.dedent(expected_representation).strip()
