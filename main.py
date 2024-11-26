import requests as rq
import os
import yaml
import json
from tqdm import tqdm
import constant as c
from pic_process import process_pic_ref
import signature as sg




headers = {
    "Host": "bizapi.csdn.net",
    "X-Ca-Key": c.xca_key,
    "X-Ca-Nonce": c.once_key,
    "X-Ca-Signature-Headers":"x-ca-key,x-ca-nonce",
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.6367.118 Safari/537.36",
    "Accept":"application/json, text/plain, */*"
}


if __name__ == '__main__':
    with open('config.yml', 'r', encoding='utf-8') as fd:
        config = yaml.load(fd, Loader=yaml.SafeLoader)
    headers['Cookie'] = config['cookie']

    output_path = config['output_path']
    markdown_path = os.path.join(output_path, 'markdown')
    meta_path = os.path.join(output_path, 'meta')
    if not os.path.exists(markdown_path):
        os.makedirs(markdown_path)
    if not os.path.exists(meta_path):
        os.makedirs(meta_path)

    page = 0
    article_cnt = 0
    article_list = []
    print('Start to get articles...')
    while True:
        list_router = c.list_router.format(page, 20)
        articles_list_url = 'https://bizapi.csdn.net'+list_router
        sig = sg.get_articles_list_signature(list_router, c.xca_key, c.once_key)
        headers['X-Ca-Signature'] = sg.to_base64_encode(c.e_key, sig)
        res = rq.get(url=articles_list_url, headers=headers)
        if res.status_code != 200:
            print(f'Request Error, status : {res.status_code}, check cookie please.')
            exit(1)
        res_json = json.loads(res.text)
        article_infos = res_json['data']['list']
        
        if len(article_infos) == 0:
            break
        page += 1
        article_cnt += len(article_infos)
        article_list.extend(article_infos)
    
    print(f'Get articles {article_cnt}')
    
    
    for article in tqdm(article_list):
        id = article['articleId']

        article_router = c.article_router.format(id)
        articles_url = 'https://bizapi.csdn.net'+article_router
        sig = sg.get_articles_list_signature(article_router, c.xca_key, c.once_key)
        headers['X-Ca-Signature'] = sg.to_base64_encode(c.e_key, sig)
        res = rq.get(url=articles_url, headers=headers)
        if res.status_code != 200:
            print(f'Request Error, status : {res.status_code}, check cookie please.')
            exit(1)

        res_json = json.loads(res.text)['data']
        res_json.update(article)
        
        del res_json['content']
        markdown_content = res_json['markdowncontent']
        del res_json['markdowncontent']
        markdown_header = ''
        st = {}
        
        if 'markdown_header_meta'in config and len(config['markdown_header_meta']) != 0:
            markdown_header = '\n'.join([f'{value}: {res_json[key]}' for key, value in config['markdown_header_meta'].items()])
            markdown_header='---\n'+markdown_header+'\n---\n'
        if config['save_pic_to_local']:
            markdown_content = process_pic_ref(markdown_content, id, os.path.join(markdown_path, id))

        with open(os.path.join(markdown_path, id+'.md'), 'w', encoding='utf-8') as fd:
            fd.write(markdown_header + markdown_content)
        
        with open(os.path.join(meta_path, id+'.json'), 'w', encoding='utf-8') as fd:
            wjson = json.dumps(res_json, indent=4).encode('utf-8').decode('unicode_escape')
            fd.write(wjson)
        
        # break



    
        
