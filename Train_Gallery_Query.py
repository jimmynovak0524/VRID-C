'''
generate list for subsets
genrate three files

train_list.yaml
gallery_list.yaml
query_list.yaml
'''
import yaml
def parse_yaml(filename):
    f = open(filename, "r")
    data = yaml.load(f, Loader=yaml.FullLoader)
    f.close()
    return data

TGQ=parse_yaml('T_G_Q.yaml')
files_id_revised=parse_yaml('files_of_all.yaml')
data ={}
data['Gallery_vehs']={}
data['Train_vehs']={}
data['query_imgs']={}
query={}
for subsets in ['Train_vehs','Gallery_vehs']:
    for ids in TGQ[subsets]:
       for imgs in files_id_revised[ids].keys():
           data[subsets][ids]=files_id_revised[ids]
           path = data[subsets][ids][imgs]['path']
           name= path.split('/')[-1]
           device=path.split('/')[-2]
           map=path.split('/')[-3]
           new=f'{map}/{device}/{name}'
           data[subsets][ids][imgs]['path']=new
for ids in TGQ['query_imgs'].keys():
    query[ids]={}
    for imgs in TGQ['query_imgs'][ids]:
        query[ids][imgs]=files_id_revised[ids][imgs]

train = dict(data['Train_vehs'])
gallery=dict(data['Gallery_vehs'])
with open('train_list.yaml', 'a', encoding='utf-8') as f:
    datsa = train
    f.write(yaml.dump(datsa))
with open('gallery_list.yaml', 'a', encoding='utf-8') as f:
    datsa = gallery
    f.write(yaml.dump(datsa))
with open('query_list.yaml', 'a', encoding='utf-8') as f:
    datsa = query
    f.write(yaml.dump(datsa))