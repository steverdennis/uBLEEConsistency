from uBLEEConsistency.input_readers import Read_WC_Trees as readers
import numpy as np
import pandas as pd

def get_datasets(force_trees = False, write_csv= True):
  
  csv_name = "/uboone/data/sdennis/consistency/wirecell/run2_bnb_plus_intrinsic_nueCC.csv"

  if not force_trees:
    try: return pd.read_csv(csv_name)
    except: print("Falling back on trees")
  
  files_and_weights = [
                       ("/pnfs/uboone/scratch/users/jjo/to/consistency_group/unselected/checkout_prodgenie_bnb_nu_overlay_run2.root",1),
                       ("/pnfs/uboone/scratch/users/jjo/to/consistency_group/unselected/checkout_prodgenie_bnb_intrinsic_nue_overlay_run2.root",1),
                      ]
                       
  
  df_nue_MC_all = readers.get_frame(files_and_weights, weight_branches=[])
  
  # ~ df_nue_MC_FC = df_nue_MC_FC.loc[(df_nue_MC_FC["match_isFC"]==1)]
  # ~ df_nue_MC_PC = df_nue_MC_PC.loc[(df_nue_MC_PC["match_isFC"]==0)]
  
  # ~ dfs_nue = [df_nue_MC_FC,df_nue_MC_PC]
  dfs_nue = [df_nue_MC_all]
  
  dfs_cut = [df.loc[(df["numu_cc_flag"]>=0)] for df in dfs_nue]
  dfs_cut = [df.loc[(df["nue_score"]>7.0)] for df in dfs_cut]
  # ~ dfs_cut = dfs_nue
  
  # Sort them
  for df in dfs_cut:
    df.sort_values(["run","subrun","event","enu_true"],inplace=True)
    
  # Fix this hack
  for df in dfs_cut:
    df["nu_pdg_final"]=12
    
  df_all = pd.concat(dfs_cut)
  
  df_all.sort_values(["run","subrun","event","enu_true"],inplace=True)

  if write_csv:
    df_all.to_csv(csv_name)
    
  return df_all

