import argparse
import os
import shutil
import warnings

warnings.filterwarnings('ignore')

def move_pdb(input_path, wt_name, output_pdb, output_ref):
    file_lst = os.listdir(input_path)
    for each_file in file_lst:
        if each_file.startswith(wt_name):
            shutil.move(os.path.join(input_path, each_file), output_pdb)
        elif each_file.startswith('resfile'):
            shutil.move(os.path.join(input_path, each_file), output_ref)


if __name__ == '__main__':
    parser = argparse.ArgumentParser('Generate xml file for mutation')
    parser.add_argument('--input_path', type=str, default='./', help='suapercharge result dir')
    parser.add_argument('--wt_name', type=str, help='wild type name')
    parser.add_argument('--output_pdb', type=str, help='output file name')
    parser.add_argument('--output_ref', type=str, help='output ref name')
    args = parser.parse_args()

    move_pdb(args.input_path, args.wt_name, args.output_pdb, args.output_ref)
