from django.shortcuts import render_to_response
from student.models import Student
from teacher.models import Teacher
from edu.models import EduAdmin

def my_render(request, template, context={}):
    context['user'] = request.user

    return render_to_response(template, context)

def username(request):

    return {'s_username':Student.objects.filter(no__username=request.user).first(),
            't_username':Teacher.objects.filter(no__username=request.user).first(),
            'e_username':EduAdmin.objects.filter(no__username=request.user).first(),
            }





class MyPagination(object):
    def __init__(self, totalCount, currentPage, perPageItemNum=30, maxPageNum=10,url=None):
        #总条目数
        self.total_count = totalCount
        #当前页
        try:
            v = int(currentPage)
            if v <= 0:
                self.current_page = 1
            else:
                self.current_page = v
        except Exception as e:
            self.current_page = 1
        #每页显示多少
        self.per_page_item_num = perPageItemNum
        #显示多少页码
        self.per_page_numb = maxPageNum
        # 加入跳转url
        self.url = url

    def start(self):
        return (self.current_page-1)*self.per_page_item_num
    def end(self):
        return self.current_page*self.per_page_item_num

    @property
    def num_pages(self):
        a,b = divmod(self.total_count,self.per_page_item_num)
        if b == 0:
            return a
        return a+1

    def page_range(self):
        if self.num_pages < self.per_page_numb:
            return range(1, self.num_pages + 1)
        part = self.per_page_numb // 2
        if self.current_page <= part:
            return range(1, self.per_page_numb + 1)
        if (self.current_page + part) > self.num_pages:
            return range(self.num_pages - self.per_page_numb + 1, self.num_pages + 1)
        return range(self.current_page - part, self.current_page + part + 1)

    def page_range_str(self):
        page_str = []
        if self.current_page == 1:
            prev = "<li class='disabled'><a href='#'>上一页</a></li>"
        else:
            prev = "<li><a href='"+self.url+"?p=%s'>上一页</a></li>" % str(self.current_page-1)
        page_str.append(prev)
        for i in self.page_range():
            if i == self.current_page:
                a = "<li class='active'><a href='"+self.url+"?p=%s' >%s</a></li>" % (i,i)
            else:
                a = "<li><a href='"+self.url+"?p=%s'>%s</a></li>" % (i, i)
            page_str.append(a)
        if self.current_page == self.num_pages:
            next_ = "<li class='disabled'><a href='#'>下一页</a></li>"
        else:
            next_ = "<li><a href='"+self.url+"?p=%s'>下一页</a></li>" % str(self.current_page+1)
        page_str.append(next_)
        return ''.join(page_str)
