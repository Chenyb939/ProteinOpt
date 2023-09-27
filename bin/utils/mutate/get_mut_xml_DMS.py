import argparse

def write_mutant_xml(in_site, out_path, chain, start_pos):
    site_lst = in_site.replace(' ', '').split(',')
    # pos_lst = [i[:-1] for i in site_lst]
    pos_lst = [int(i[:-1]) - (int(start_pos) - 1)  for i in site_lst]
    tag_lst = [i[-1:].upper() for i in site_lst]

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

    mut_lst = [letterDict[i] for i in tag_lst]
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
    parser.add_argument('--in_site', type=str, help='design site')
    parser.add_argument('--output_file', type=str, default='./mutate.xml', help='mutate.xml path')
    parser.add_argument('--chain', type=str, default='E', help='chain to design')
    parser.add_argument('--start_pos', type=int, default=334, help='The first residue position of the chain to be designed in the pdb file')
    args = parser.parse_args()
    
    write_mutant_xml(args.in_site, args.output_file, args.chain, args.start_pos)