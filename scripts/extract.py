# This script extract features from folder of PE files

import sys
import os
import argparse
import json
from ember.features import PEFeatureExtractor

def _main():
    prog = "extract.py"
    descr = "Extracts features from PE files"
    parser = argparse.ArgumentParser(prog=prog, description=descr)
    parser.add_argument("-v", "--featureversion", type=int, default=2, help="EMBER feature version", required=False)
    parser.add_argument("--pe", type=str, help="folder of pe files", required=True)
    parser.add_argument("--output", type=str, help="json output file", required=True)
    args = parser.parse_args()

    root = args.pe
    outfn = args.output

    with open(outfn,'w') as fw:
        for fn in os.listdir(root):
            extractor = PEFeatureExtractor(args.featureversion)

            with open(os.path.join(root,fn),'rb') as fr:
                file_data = fr.read()

            features = extractor.raw_features(file_data)
            features['label'] = 1

            fw.write(json.dumps(features))
            fw.write('\n')

if __name__ == '__main__':
    _main()
