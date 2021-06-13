from rest_framework import viewsets, mixins


class RetrieveUpdateDestroy(

    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet): pass


class ListCreateGenericViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet): pass
