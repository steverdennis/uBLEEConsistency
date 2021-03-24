from uBLEEConsistency.input_readers import Read_DLLEE_Trees

import pandas as pd

def get_datasets():

  files = [
   "/uboone/data/sdennis/consistency/dllee/tree/input_to_sbnfit_v48_Sep24_withExtraGENIE_1e1p_run1_Feb09.root",
   "/uboone/data/sdennis/consistency/dllee/tree/input_to_sbnfit_v48_Sep24_withExtraGENIE_1e1p_run2_Feb09.root",
   "/uboone/data/sdennis/consistency/dllee/tree/input_to_sbnfit_v48_Sep24_withExtraGENIE_1e1p_run3_Feb09.root"
  ]

  frames = [Read_DLLEE_Trees.get_frame([f],treename="sel_nue_tree") for f in files]

  df_all = pd.concat(frames)
  
  return df_all

