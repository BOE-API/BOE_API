__author__ = 'Carlos'
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.db.models import Max,Count,Q,F

class ModelPagination:
    model = None
    items_per_page = None
    count = None
    page_range = []

    def __init__(self, model, items_per_page):
        self.model = model
        self.items_per_page = items_per_page
        self.count = self.model.aggregate(Max('id'))['id__max']
        print self.count
        self.num_pages = divmod(self.count, self.items_per_page)[0]+1

        for i in range(self.num_pages):
            self.page_range.append(i+1)

    def page(self, page_number):
        if page_number > self.num_pages:
            raise EmptyPage, "That page contains no results"

        if page_number <= 0:
            raise EmptyPage, "That page number is less than 1"

        start = self.items_per_page * (page_number-1)
        end = self.items_per_page * page_number

        object_list = self.model.filter(id__gte=start, id__lt=end)
        return ModelPaginationPage(object_list, page_number, self.count, start, end, self)

class ModelPaginationPage:
    object_list = None
    number = None
    count = None
    start = None
    end = None
    paginator = None

    def __unicode__(self):
        return "<Page %s of %s>"%(self.number, self.count)

    def __init__(self, object_list, number, count, start, end, paginator):
        self.number = number
        self.count = count
        self.object_list = object_list
        self.start = start
        self.end = end
        self.paginator = paginator

    def has_next(self):
        return False if self.number >= self.count else True

    def has_previous(self):
        return False if self.number <= 1 else True

    def has_other_pages(self):
        return True if self.has_next or self.has_previous else False

    def next_number(self):
        return self.number + 1

    def previous_number(self):
        return self.number + 1

    def start_index(self):
        return self.start

    def end_index(self):
        return self.end
