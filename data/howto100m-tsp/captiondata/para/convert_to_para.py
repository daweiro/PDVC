import json
split='val'
p='formatted_captions_{}.json'.format(split)
out_p = 'para_formatted_captions_{}.json'.format(split)

d = json.load(open(p))
out = {}
for k,v in d.items():
    para = '. '.join(v['sentences'])
    out[k] = para
json.dump(out, open(out_p, 'w'))
