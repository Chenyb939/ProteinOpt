import argparse
def per_process(input, output, target_chain):
    with open(input, 'r') as file, open(output, 'w') as file2:
        lines = file.readlines()
        for line in lines:
            if line.startswith('ATOM'):
                if target_chain == line[21]:
                    file2.write(line)
            else:
                pass
if __name__ == '__main__':
    parser = argparse.ArgumentParser('Generate xml file for mutation')
    parser.add_argument('--wt_path', type=str, default='/public/cheny/stability/test_stab_v0/6m0j.pdb', help='WT pdb file')
    parser.add_argument('--chain', type=str, default='E', help='chain to design')
    parser.add_argument('--out_path', type=str, default='/public/cheny/stability/test_stab_v0/6m0j_new.pdb', help='output path')

    args = parser.parse_args()

    per_process(args.wt_path, args.out_path, args.chain)