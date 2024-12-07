from rest_framework.pagination import PageNumberPagination


class PageNumPagination(PageNumberPagination):
    """Класс, описывающий постраничный вывод"""
    page_size = 3
    page_size_query_param = 'page_size'
    max_page_size = 100
