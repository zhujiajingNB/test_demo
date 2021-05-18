
# 获取总页数
def get_pages(count: int, page_num: int):
    if count//page_num == 0:
        return 1
    elif count/page_num > count//page_num:
        return count//page_num + 1
    else:
        return count//page_num