# lms/paginators.py

from rest_framework.pagination import PageNumberPagination


class CustomPagination(PageNumberPagination):
    # Количество элементов на одной странице по умолчанию
    page_size = 10

    # GET /courses/?page_size=20
    page_size_query_param = 'page_size'

    # Максимально допустимое количество элементов на странице, которое клиент может запросить
    max_page_size = 50
