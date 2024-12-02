import argparse
import warnings

warnings.filterwarnings('ignore')

def get_mutant_pos(path):
    with open(path, 'r') as file:
        position_lst = []
        native_lst = []
        mutant_lst = []
        lines = file.readlines()
        for line in lines:
            if line.startswith('Position'):
                pos_line = line.split(' ')
                nat_line = line.split('Native AA: ')
                mut_line = line.split('Mutant AA: ')
                position_lst.append(pos_line[1])
                native_lst.append(nat_line[1][:3])
                mutant_lst.append(mut_line[1][:3])

    pos_lst = list(set(position_lst))
    pos_lst.sort(reverse = True)
    index_list = [position_lst.index(i) for i in pos_lst]
    nat_lst = [native_lst[i] for i in index_list]
    mut_lst = [mutant_lst[i] for i in index_list]
    return pos_lst, nat_lst, mut_lst

def write_mutant_xml(in_path, out_path, chain):
    pos_lst, nat_lst, mut_lst = get_mutant_pos(in_path)
    with open(out_path, 'w') as file:
        file.write('<ROSETTASCRIPTS>\n\t<MOVERS>\n')
        for i in range(len(pos_lst)):
            file.write(f'\t\t<MutateResidue name="mutate_{i}" target="{pos_lst[i]}{chain}" new_res="{mut_lst[i]}"/>\n')
        file.write('\t</MOVERS>\n\t<PROTOCOLS>\n')
        for i in range(len(pos_lst)):
            file.write(f'\t\t<Add mover="mutate_{i}"/>\n')
        file.write('\t</PROTOCOLS>\n</ROSETTASCRIPTS>\n')
        
if __name__ == '__main__':
    parser = argparse.ArgumentParser('Generate xml file for mutation')
    parser.add_argument('--input_file', type=str, default='./reports.txt', help='VIP report')
    parser.add_argument('--output_file', type=str, default='./mutate.xml', help='mutate.xml path')
    parser.add_argument('--chain', type=str, default='E', help='chain to design')
    args = parser.parse_args()
    
    write_mutant_xml(args.input_file, args.output_file, args.chain)