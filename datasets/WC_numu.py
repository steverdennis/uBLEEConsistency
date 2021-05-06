from uBLEEConsistency.input_readers import Read_WC_Trees as readers
import numpy as np
import pandas as pd

def get_datasets(force_trees = False, write_csv=True):
  csv_name = "/uboone/data/sdennis/consistency/wirecell/checkout_prodgenie_bnb_nu_overlay_run1_numuCC.csv"
  if not force_trees:
    try: return pd.read_csv(csv_name)
    except: print("Falling back on trees")
    
  df_numu_MC_FC = readers.get_frame([("/uboone/data/sdennis/consistency/wirecell/checkout_prodgenie_bnb_nu_overlay_run1_numuCC_FC.root", 1.)], [])
  # ~ df_numu_MC_PC = readers.get_frame([("/uboone/data/sdennis/consistency/wirecell/checkout_prodgenie_bnb_nu_overlay_run1_numuCC_PC.root", 1.)], [])
  
  df_numu_MC_FC = df_numu_MC_FC.loc[(df_numu_MC_FC["match_isFC"]==1)]
  # ~ df_numu_MC_PC = df_numu_MC_PC.loc[(df_numu_MC_PC["match_isFC"]==0)]
  
  # ~ dfs_numu = [df_numu_MC_FC,df_numu_MC_PC]
  dfs_numu = [df_numu_MC_FC]
  
  dfs_cut = [df.loc[(df["numu_cc_flag"]>0)] for df in dfs_numu]
  dfs_cut = [df.loc[(df["numu_score"]>0.9)] for df in dfs_cut]
  
  # Sort them
  for df in dfs_cut:
    df.sort_values(["run","subrun","event","enu_true"],inplace=True)
  
  # Fix this hack
  for df in dfs_cut:
    df["nu_pdg_final"]=14

  df_all = pd.concat(dfs_cut)
  
  if write_csv:
    df_all.to_csv(csv_name)
  
  return df_all
