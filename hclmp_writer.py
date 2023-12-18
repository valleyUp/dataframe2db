import pandas as pd
from pymatgen.core.composition import Composition
import json
from monty.json import MontyEncoder
import numpy as np
import torch
from glob import glob

def convert_39element_to_composition(df: pd.DataFrame):
    ELEMS_SET = ['Ag', 'Ba', 'Bi', 'Ca', 'Ce', 'Co', 'Cr',  
                 'Cu', 'Er', 'Eu', 'Fe', 'Ga', 'Gd', 'Hf', 
                 'In', 'K', 'La', 'Mg', 'Mn', 'Mo', 'Nb', 
                 'Nd', 'Ni', 'P', 'Pb', 'Pd', 'Pr', 'Rb', 
                 'Sc', 'Sm', 'Sn', 'Sr', 'Tb', 'Ti', 'V', 
                 'W', 'Yb', 'Zn', 'Zr']
    
    def convert_to_composition(row):
        composition = {}
        for stoich, elem in zip(row[:39], ELEMS_SET):
            # if stoich != 0:
            composition[elem] = stoich
        return Composition(composition)

    compositions = []
    for row in df.itertuples():
        compositions.append(convert_to_composition(row))
    
    df_dos = [np.array(row[39:]) for row in df.itertuples(index=False)]
    new_df = pd.DataFrame({"composition": compositions, "dos": df_dos})
    new_df["composition"] = new_df["composition"].apply(lambda x: json.dumps(x, cls=MontyEncoder))
    return new_df

def process_HCLMP_GAN_data():
    dat = np.load("../refRepos/HCLMP/data/20200828_MP_dos/MP_comp39_dos161.npy")
    trainIdx = np.load("../refRepos/HCLMP/data/20200828_MP_dos/train_idx.npy")
    testIdx = np.load("../refRepos/HCLMP/data/20200828_MP_dos/test_idx.npy")

    df = pd.DataFrame(dat)
    df = convert_39element_to_composition(df)
    trainCol = [True if i in trainIdx else False for i in range(len(trainIdx) + len(testIdx))]
    testCol = [True if i in testIdx else False for i in range(len(trainIdx) + len(testIdx))]
    df["train"] = trainCol
    df["test"] = testCol
    df.to_json("./hclmp_gan.json.gz")


def process_HCLMP_data():
    with open("../refRepos/HCLMP/data/uvis_dataset_no_redundancy/uvis_dict.chkpt", "rb") as f:
        dat = torch.load(f)
    df = pd.DataFrame([dat[i] for i in range(len(dat)-1)], columns=dat[0].keys())
    renameCols = {
        "composition_nonzero": "nonZeroComp",
        "gen_dos_fea": "genDosFea",
        "nonzero_element_name": "nonZeroElemName",
        "composition_nonzero_idx": "nonZeroCompIdx",
    }
    df.rename(columns=renameCols, inplace=True)
    # df.to_json("./hclmp.json.gz")

def process_ternary_indices():
    ternaryIndices = {}
    indices_paths = {
        "train": "../refRepos/HCLMP/data/uvis_dataset_no_redundancy/idx/train/*.npy",
        "val": "../refRepos/HCLMP/data/uvis_dataset_no_redundancy/idx/val_from_train/*.npy",
        "test": "../refRepos/HCLMP/data/uvis_dataset_no_redundancy/idx/test/*.npy"
    }
    for key, path in indices_paths.items():
        indices_dict = {}
        for file in glob(path):
            ternaryIdx = np.load(file)
            indices_dict[file.split("/")[-1].split(".")[0]] = ternaryIdx
        ternaryIndices[key] = indices_dict

    randomIdx = {}
    randomIdx["train"] = np.load("../refRepos/HCLMP/data/uvis_dataset_no_redundancy/idx/rd_idx/train/rd_idx.npy")
    randomIdx["val"] = np.load("../refRepos/HCLMP/data/uvis_dataset_no_redundancy/idx/rd_idx/val/rd_idx.npy")
    randomIdx["test"] = np.load("../refRepos/HCLMP/data/uvis_dataset_no_redundancy/idx/rd_idx/test/rd_idx.npy")
    ternaryIndices['random'] = randomIdx

    multiCols = [('ternary', key) for key in ternaryIndices.keys()] + [('random', 'random')]
    columns = pd.MultiIndex.from_tuples(multiCols)
    allIndices = pd.DataFrame(ternaryIndices)
    allIndices.columns = columns
    # allIndices.to_json("./hclmp_all_indices.json.gz")

# Example usage:
process_HCLMP_GAN_data()
# process_HCLMP_data()
# process_ternary_indices()

