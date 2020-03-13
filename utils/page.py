

"""
传入：
    - 所有数据
    - 当前页
    - 每页显示30条数据
    - 最多显示几个页码  7个

自定义分页器
    - 所有数据的个数
    - 当前页
    - 每页显示30条数据
    - 最多显示几个页码  7个
"""


class Pagination(object):
    def __init__(self, total_count, current_page, per_page_item_num=10, max_pag_num=11):
        self.total_count = total_count  # 总数据个数
        try:
            first = int(current_page)
            if first <= 0:
                first = 1
            self.current_page = first  # 当前页
        except Exception as e:
            self.current_page = 1
        self.per_page_item_num = per_page_item_num  # 每页显示数据
        self.max_pag_num = max_pag_num  # 显示几个页码

    @property
    def start(self):
        return (self.current_page-1) * self.per_page_item_num

    @property
    def end(self):
        return self.current_page * self.per_page_item_num

    @property
    def num_pages(self):
        """
        计算总页数
        数据总个数/每页显示数据个数==总页数
        :return: 有多少页数
        """
        a, b = divmod(self.total_count, self.per_page_item_num)
        if b == 0:
            return a
        return a+1


    def pager_num_range(self):
        if self.num_pages <= self.max_pag_num:
            return range(1, self.num_pages+1)
        part = int(self.max_pag_num/2)
        if self.current_page <= part:
            return range(1, self.max_pag_num+1)
        if (self.current_page+part) > self.num_pages:
            return range(self.num_pages-self.max_pag_num+1, self.num_pages+1)
            # return range(self.current_page-part, self.num_pages+1)
        return range(self.current_page-part, self.current_page+part+1)

    def page_str(self):
        page_list = []
        first = '<li><a href="/page/?p=1">首页</a></li>'
        page_list.append(first)
        if self.current_page == 1:
            prev = '<li class="disabled"><a href="javascript:;">上一页</a></li>'
        else:
            prev = '<li><a href="/page/?p=%s">上一页</a></li>' % (self.current_page-1)
        page_list.append(prev)
        for i in self.pager_num_range():
            if self.current_page == i:
                temp = '<li class="active"><a href="/page/?p=%s">%s</a></li>' % (i, i)
            else:
                temp = '<li><a href="/page/?p=%s">%s</a></li>' % (i, i)
            page_list.append(temp)
        if self.current_page == self.num_pages:
            next = '<li class="disabled"><a href="javascript:;">下一页</a></li>'
        else:
            next = '<li><a href="/page/?p=%s">下一页</a></li>' % (self.current_page+1)
        page_list.append(next)
        last = '<li><a href="/page/?p=%s">尾页</a></li>' % (self.num_pages)
        page_list.append(last)

        page_list_str = ''.join(page_list)
        return page_list_str