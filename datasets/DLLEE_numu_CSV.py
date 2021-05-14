from uBLEEConsistency.input_readers import Read_DLLEE_CSV_numu

import pandas as pd

def get_datasets(force_original = True, write_csv=True):

  csv_name = "/uboone/data/sdennis/consistency/dllee/eventlist_overlay_numu_newsample_2021_05_06.csv"
  if not force_original:
    try:
      print("Attempting to read",csv_name)
      return pd.read_csv(csv_name)
    except: print("Falling back on trees")
    
  files = [
   "/uboone/data/sdennis/consistency/dllee/forCons_copied_2021_05_06/numu/new_samples/FinalSelection0_overlay_run1.txt",
   "/uboone/data/sdennis/consistency/dllee/forCons_copied_2021_05_06/numu/new_samples/FinalSelection0_overlay_run2.txt",
   "/uboone/data/sdennis/consistency/dllee/forCons_copied_2021_05_06/numu/new_samples/FinalSelection0_overlay_run3.txt",
   "/uboone/data/sdennis/consistency/dllee/forCons_copied_2021_05_06/numu/new_samples/FinalSelection0_intrinsics_run1.txt",
   "/uboone/data/sdennis/consistency/dllee/forCons_copied_2021_05_06/numu/new_samples/FinalSelection0_intrinsics_run2.txt",
   "/uboone/data/sdennis/consistency/dllee/forCons_copied_2021_05_06/numu/new_samples/FinalSelection0_intrinsics_run3.txt"
  ]

  frames = [Read_DLLEE_CSV_numu.read_csv(f) for f in files]

  df_all = pd.concat(frames)
  
  # Sort them
  df_all.sort_values(["run","subrun","event","enu_true"],inplace=True)
  
  if write_csv:
    df_all.to_csv(csv_name)
    
  return df_all
