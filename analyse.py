import os
from Bio import PDB
import pandas as pd
import warnings
warnings.filterwarnings("ignore")

# output dir

out_dir = '/share/home/cheny/Projects/stable_final/6m0j/output/run4/'
# out_dir = '/share/home/cheny/Projects/stable_final/6m0j/result/Super42'
# out_dir = '/share/home/cheny/Projects/stable_final/6m0j/result/PM'
# relax result dir 
relax_dir = '/share/home/cheny/Projects/stable_final/6m0j/output/run4/data/Relaxed_WT/'
# com result dir
mc_dir = '/share/home/cheny/Projects/stable_final/6m0j/output/run4/data/Com_PM_41/'
# mut number for DMS
mut_nums = 0
# mut site for DMS
# mut_site = ['166E']
mut_site = []

def get_seq(pdb):
    name = pdb.split('/')[-1][:4]
    parser = PDB.PDBParser()
    structure = parser.get_structure(name, pdb)
    ppb = PDB.PPBuilder()
    return str(ppb.build_peptides(structure)[0].get_sequence())

def comp_fa(raw_fa, target_fa):
    mut = ''
    num = 0
    for i in range(len(raw_fa)):
        if raw_fa[i] == target_fa[i]:
            pass
        else:
            num += 1
            mut = mut + raw_fa[i] + str(i+1) + target_fa[i] + ','
    return mut, num

def get_score(path, raw_fa):
    score_lst = []
    name_lst = []
    seq_lst = []
    mut_lst = []
    num_lst = []
    path_lst = []
    with open(os.path.join(path, 'score.sc'), 'r') as file:
        lines = file.readlines()
        for line in range(len(lines)):
            if line < 2:
                pass
            else:
                score = float(lines[line][9:18])
                name = lines[line].split(' ')[-1].replace('\n', '')
                seq = get_seq(os.path.join(path, name+'.pdb'))
                mut, num = comp_fa(raw_fa, seq)
                score_lst.append(score)
                name_lst.append(name)
                seq_lst.append(seq)
                mut_lst.append(mut)
                num_lst.append(num)
                path_lst.append(os.path.join(path, name+'.pdb'))
    return score_lst, name_lst, seq_lst, mut_lst, num_lst, path_lst

def get_raw_score(path):
    with open(os.path.join(path, 'score_Relaxed.sc'), 'r') as file:
        lines = file.readlines()
        line = lines[2]
        score = float(line[9:18])
    return score
# generate csv result


# relax result dir 
raw_path = relax_dir
# com result dir
path = mc_dir

ene = get_raw_score(raw_path)
# raw_fa = get_seq(os.path.join(raw_path, '6m0j_final_Relaxed.pdb'))
raw_fa = get_seq(os.path.join(raw_path, '6m0j_Relaxed.pdb'))
score_lst, name_lst, seq_lst, mut_lst, num_lst, path_lst = get_score(path, raw_fa)
print('read relax down')
d_score_lst = []
for score in score_lst:
    d_score_lst.append(score-ene)
df = pd.DataFrame({'name': name_lst, 'score': score_lst, 'mut': mut_lst, 'mut_num': num_lst, 'dds': d_score_lst, 'seq': seq_lst, 'path_lst': path_lst})
df.to_csv(os.path.join(out_dir, 'result.csv'), index=False)


import pandas as pd
import matplotlib.pylab as plt
import seaborn as sns

sns.distplot
# mut_nums = 1
# mut_site = ['166E']
df = pd.read_csv(os.path.join(out_dir, 'result.csv'))
df = df.sort_values('score', ascending=True)

def get_dmut(muts, mut_lst):
    for mut in mut_lst:
        muts = muts.replace((mut+','), '')
    return muts[:-1]
def get_dmun(nums, mut_num):
    return int(nums-mut_num)


df['dmut']=df.apply(lambda x: get_dmut(x['mut'], mut_site), axis=1)
df['dnum']=df.apply(lambda x: get_dmun(x['mut_num'], mut_nums), axis=1)
dnum = list(df['dnum'])
dmut = list(df['dmut'])
score = list(df['score'])
df.to_csv(os.path.join(out_dir, 'umut_reslt.csv'), index=False)


sns.distplot(df['score'], rug=False, hist=True)
plt.savefig(os.path.join(out_dir, 'score.png'))

def draw_mut(dnum):
    nums_lst = []
    num_lst = dnum
    for num in num_lst:
        nums_lst.append(num)
    num_flag = list(set(nums_lst))
    num_count = [nums_lst.count(i) for i in num_flag]
    num_dict = dict(zip(num_flag, num_count))
    return num_dict

def draw_count_site(dmut):
    site_lst = []
    mut_lst = dmut
    for mut in mut_lst:
        if mut == '':
            pass
        else:
            site_lst.append(mut)
    site_flag = list(set(site_lst))
    site_count = [site_lst.count(i) for i in site_flag]
    site_dict = dict(zip(site_flag, site_count))

    sites = []
    counts = []
    for each in range(len(site_flag)):
        try:
            each_lst = site_flag[each].split(',')
            new_each_lst = [i[1:-1] for i in each_lst]
            sites += new_each_lst
            counts += [site_count[each] for i in range(len(new_each_lst))]
        except:
            sites.append(each[1:-1])
            counts.append(site_count[each])                                          
    new_sites = list(set(sites))
    for aa in range(len(sites)):
        aa_lst = [i for i in sites if i==sites[aa]]
    new_count = [0 for _ in range(len(new_sites))]
    for i in range(len(new_sites)):
        for j in  range(len(sites)):
            if new_sites[i] == sites[j]:
                new_count[i] += counts[j]
    new_dict = dict(zip(new_sites, new_count))          
    return site_dict, new_dict


site_dict, new_dict = draw_count_site(dmut)

num_dict = draw_mut(dnum)
print("mut site num and num", num_dict)

# draw num pic
key = num_dict.keys()
value = num_dict.values()

df = pd.DataFrame()
df['mutated_site'] = key
df['count'] =  value
# plt.figure(1)
plt.figure(figsize=(10, 5))
# plt.subplot(211)
sns.set_theme(style = 'whitegrid')
sns.set_color_codes("muted")
p1 = sns.barplot( data=df, x='mutated_site', y='count')
# plt.bar_label(p1.containers[0])
plt.savefig(os.path.join(out_dir, 'num_count.png'))

# draw score pic
df = pd.DataFrame()
df['mutated_site'] = dnum
df['score'] = score
# plt.figure(2)
plt.figure(figsize=(10, 6))
# plt.subplot(212)
sns.set_theme(style = 'whitegrid')
sns.set_color_codes("muted")
p1 = sns.boxplot(data=df, x='mutated_site', y='score')
plt.savefig(os.path.join(out_dir, 'score_count.png'))

#draw site pic
key = site_dict.keys()
value = site_dict.values()

df = pd.DataFrame()
df['mutate'] = key
df['count'] =  value

plt.figure(figsize=(30, 18))
sns.set_theme(style = 'whitegrid')
sns.set_color_codes("muted")
p1 = sns.barplot(data=df, x='mutate', y='count')
plt.xticks(rotation=90)
plt.bar_label(p1.containers[0])
plt.savefig(os.path.join(out_dir, 'mut_type.png'))

#draw site pic
key = new_dict.keys()
value = new_dict.values()

df = pd.DataFrame()
df['mutate'] = key
df['count'] =  value

plt.figure(figsize=(10, 5))
sns.set_theme(style = 'whitegrid')
sns.set_color_codes("muted")
p1 = sns.barplot(data=df, x='mutate', y='count')
# plt.xticks(rotation=30)
plt.bar_label(p1.containers[0])
plt.savefig(os.path.join(out_dir, 'mut_site.png'))
