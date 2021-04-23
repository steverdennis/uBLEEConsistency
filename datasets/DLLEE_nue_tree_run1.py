from uBLEEConsistency.input_readers import Read_DLLEE_Trees

import pandas as pd

def get_datasets(force_trees = False, write_csv=True):

  csv_name = "/uboone/data/sdennis/consistency/dllee/input_to_sbnfit_v48_Sep24_withExtraGENIE_1e1p_Feb08_run1.csv"
  if not force_trees:
    try:
      print("Attempting to read",csv_name)
      return pd.read_csv(csv_name)
    except: print("Falling back on trees")
    
  files = [
   "/uboone/data/sdennis/consistency/dllee/tree/input_to_sbnfit_v48_Sep24_withExtraGENIE_1e1p_run1_Feb09.root",
  ]

  frames = [Read_DLLEE_Trees.get_frame([f],treename="sel_nue_tree") for f in files]

  df_all = pd.concat(frames)
  
  # Sort them
  df_all.sort_values(["run","subrun","event","enu_true"],inplace=True)
  
  if write_csv:
    df_all.to_csv(csv_name)
    
  return df_all

