import requests as rq
import re
import os


def process_pic_ref(content: str, id: str, save_path: str):
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    
    reg = re.compile(r'!\[.*?\]\(.*?\)')
    pic_tokens = reg.findall(content)
    
    pic_index = {}

    for pic_token in pic_tokens:
        url_start = pic_token.rindex('(') + 1
        pic_url = pic_token[url_start:-1]
        pic_name = pic_url.split('/')[-1]
        res = rq.get(pic_url)
        if res.status_code != 200:
            continue
        with open(os.path.join(save_path, pic_name), 'wb') as fd:
            fd.write(res.content)
        pic_index[pic_token] = os.path.join(id, pic_name)
    
    for pic_url, pic_local_path in pic_index.items():
        replace_str = pic_url[:pic_url.rindex('(')] + f'({pic_local_path})'
        content = content.replace(pic_url, replace_str)
    return content



if __name__ == '__main__':
    with open('./articles/markdown/139172010.md', 'r', encoding='utf-8') as fd:
        arti = fd.read()
    with open('./articles/markdown/1344.md', 'w', encoding='utf-8') as fd:
        fd.write(process_pic_ref(arti, '34', "./articles/markdown/34")   )
    