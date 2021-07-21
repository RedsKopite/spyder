def handle_starttag_001(attrs, like_data_list):
    for (variable, value) in attrs:
        if variable == "title" and "点赞数" in value:
            like_data_list.append(value)
