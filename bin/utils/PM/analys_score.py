import os
import argparse
import pandas as pd
import xlwt


def get_median(data):
    data.sort()
    half = len(data) // 2
    return (data[half] + data[~half]) / 2


def get_score(dirpath, filename='score.sc'):
    with open(os.path.join(dirpath, filename), 'r') as file:
        lines = file.readlines()
        score_list = []
        for line in lines:
            if line.startswith('SEQUENCE'):
                pass
            else:
                if line[13].isdigit() == True:
                    score = float(line[8:19])
                    score_list.append(score)
    return get_median(score_list)


def score2xml(path, site):
    """
    write energy score of one site in xml
    """
    all_path = os.path.join(path, site)
    aa_list = ['A', 'C', 'D', 'E', 'F', 'G', 'H', 'K', 'I', 'L', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'V', 'Y', 'W']
    workbook = xlwt.Workbook(encoding='utf-8')
    worksheet = workbook.add_sheet('My Worksheet')
    worksheet.write(1, 0, label='score')
    for aa in range(len(aa_list)):
        worksheet.write(0, aa + 1, label=aa_list[aa])
        score_path = os.path.join(all_path, aa_list[aa])
        score = get_score(score_path)
        worksheet.write(1, aa + 1, score)
    workbook.save(f'{site}.xls')


def socre2df(in_path, out_path, site_begin=0, site_end=0, site_list=[]):
    """get score from socre.sc"""
    if site_list != []:
        pass
    else:
        site_list = [str(i) for i in range(int(site_begin), int(site_end + 1))]
    aa_list = ['ALA', 'CYS', 'ASP', 'GLU', 'PHE',
               'GLY', 'HIS', 'ILE', 'LYS', 'LEU',
               'MET', 'ASN', 'PRO', 'GLN', 'ARG',
               'SER', 'THR', 'VAL', 'TRP', 'TYR']
    score_list = []
    for site in site_list:
        site_path = os.path.join(in_path, site)
        score_dic = {}
        for aa in aa_list:
            aa_path = os.path.join(site_path, aa)
            score = get_score(aa_path)
            score_dic[aa] = score
        score_list.append(score_dic)
    df = pd.DataFrame(score_list, index=site_list, columns=aa_list)
    df.to_csv(os.path.join(out_path, 'score.csv'))
    return df, score_list


def write_fatxt(inpath, outpath, end_pos):
    letterDict = {}
    letterDict["A"] = 'ALA'
    letterDict["C"] = 'CYS'
    letterDict["D"] = 'ASP'
    letterDict["E"] = 'GLU'
    letterDict["F"] = 'PHE'
    letterDict["G"] = 'GLY'
    letterDict["H"] = 'HIS'
    letterDict["I"] = 'ILE'
    letterDict["K"] = 'LYS'
    letterDict["L"] = 'LEU'
    letterDict["M"] = 'MET'
    letterDict["N"] = 'ASN'
    letterDict["P"] = 'PRO'
    letterDict["Q"] = 'GLN'
    letterDict["R"] = 'ARG'
    letterDict["S"] = 'SER'
    letterDict["T"] = 'THR'
    letterDict["V"] = 'VAL'
    letterDict["W"] = 'TRP'
    letterDict["Y"] = 'TYR'

    fileout = open(os.path.join(outpath, 'all.txt'), 'w')
    with open(inpath, 'r') as file:
        lines = file.readlines()
        for line in lines:
            if line.startswith('>'):
                pass
            else:
                for i in range(end_pos):
                    fileout.write(f'{i + 1} {letterDict[line[i]]}')
                    fileout.write('\n')
                    # fileout.write(f'{i + 1} {letterDict[line[i]]}\n')
    fileout.close()


def dg_df(input_file, score_df, score_list, out_path):
    aa_list = ['ALA', 'CYS', 'ASP', 'GLU', 'PHE',
               'GLY', 'HIS', 'ILE', 'LYS', 'LEU',
               'MET', 'ASN', 'PRO', 'GLN', 'ARG',
               'SER', 'THR', 'VAL', 'TRP', 'TYR']
    # aa_list = ['A', 'C', 'D', 'E', 'F', 'G', 'H', 'K', 'I', 'L', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'V', 'Y', 'W']

    with open(input_file, 'r') as file:
        lines = file.readlines()
        site_list = []
        d_score_list = []
        for line in lines:
            site = line.replace('\n', '').split(' ')[0]
            aa = line.replace('\n', '').split(' ')[-1]
            site_list.append(site)
            score = score_df.at[site, aa]
            p = site_list.index(site)
            score_dict = score_list[p]
            new_socrea_dict = {}
            [new_socrea_dict.update({i: format(score_dict[i] - score, '.3f')}) for i in aa_list]
            d_score_list.append(new_socrea_dict)
        df = pd.DataFrame(d_score_list, index=site_list, columns=aa_list)
        df.to_csv(os.path.join(out_path, 'd_score.csv'))
    return df


def writeref(df, input_file, out_path, chain):
    aa_list = ['ALA', 'CYS', 'ASP', 'GLU', 'PHE',
               'GLY', 'HIS', 'ILE', 'LYS', 'LEU',
               'MET', 'ASN', 'PRO', 'GLN', 'ARG',
               'SER', 'THR', 'VAL', 'TRP', 'TYR']

    letterDict = {}
    letterDict["ALA"] = 'A'
    letterDict["CYS"] = 'C'
    letterDict["ASP"] = 'D'
    letterDict["GLU"] = 'E'
    letterDict["PHE"] = 'F'

    letterDict["GLY"] = 'G'
    letterDict["HIS"] = 'H'
    letterDict["ILE"] = 'I'
    letterDict["LYS"] = 'K'
    letterDict["LEU"] = 'L'

    letterDict["MET"] = 'M'
    letterDict["ASN"] = 'N'
    letterDict["PRO"] = 'P'
    letterDict["GLN"] = 'Q'
    letterDict["ARG"] = 'R'

    letterDict["SER"] = 'S'
    letterDict["THR"] = 'T'
    letterDict["VAL"] = 'V'
    letterDict["TRP"] = 'W'
    letterDict["TYR"] = 'Y'
    # aa_list = ['A', 'C', 'D', 'E', 'F', 'G', 'H', 'K', 'I', 'L', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'V', 'Y', 'W']

    file = open(os.path.join(out_path, 'ref.txt'), 'w')
    file.write('NATAA\nUSE_INPUT_SC\n\nStart\n\n')
    indexs = list(df.index.values)
    for index in indexs:
        aas = ''
        for aa in aa_list:
            score = df.at[index, aa]
            if (float(score)+0.5) < 0:
                aas += letterDict[aa]
        try:
            aas.replace('C', '')
        except:
            pass
        if aas == '':
            pass
        else:
            with open(input_file, 'r') as filei:
                lines = filei.readlines()
                for line in lines:
                    site = line.replace('\n', '').split(' ')[0]
                    if index == site:
                        aa = line.replace('\n', '').split(' ')[-1]
                        aas += letterDict[aa]

            file.write(f'{index} {chain} PIKAA {aas}\n')
    file.close()


if __name__ == '__main__':

    parser = argparse.ArgumentParser('Generate xml file for mutation')
    parser.add_argument('--input_path', type=str, default='./', help='PM result folder')
    parser.add_argument('--output_path', type=str, default='./', help='output path result folder')
    parser.add_argument('--start_pos', type=int, default=1, help='The first residue position of the chain to be designed in the pdb file')
    parser.add_argument('--end_pos', type=int, default=195, help='The last residue position of the chain to be designed in the pdb file')
    parser.add_argument('--target_fasta', type=str, default='6yz5_EF_mut_relax_E.fasta', help='Target chain fasta file')
    parser.add_argument('--chain', type=str, default='A', help='Target chain')
    
    args = parser.parse_args()

    df, score_list = socre2df(args.input_path, args.output_path, site_begin=args.start_pos, site_end=args.end_pos)
    write_fatxt(args.target_fasta, args.output_path, args.end_pos)

    new_df = dg_df(os.path.join(args.output_path, './all.txt'), df, score_list, args.output_path)
    writeref(new_df, os.path.join(args.output_path, './all.txt'), args.output_path, args.chain)
