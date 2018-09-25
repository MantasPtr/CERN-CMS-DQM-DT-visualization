from math import ceil

class Pagination(object):

    def __init__(self, page, per_page, total_count):
        self.page = page
        self.per_page = per_page
        self.total_count = total_count

    @property
    def last_page(self):
        return int(ceil(self.total_count / float(self.per_page)))

    @property
    def has_prev(self):
        return self.page > 1

    @property
    def has_next(self):
        return self.page < self.last_page

    def iter_pages(self, first_count=1, left_of_current_count=2,right_of_current_count=2, last_count=1):
        last = 0
        for num in range(1, self.last_page + 1):
            if num <= first_count or (self.page - left_of_current_count <= num <= self.page + right_of_current_count) or num > self.last_page - last_count:
                if last + 1 != num:
                    yield None
                yield num
                last = num