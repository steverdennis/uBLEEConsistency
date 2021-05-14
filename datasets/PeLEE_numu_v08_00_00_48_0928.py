#import uBLEEConsistency
from uBLEEConsistency.input_readers import Read_PeLEE_Trees_numu as readers
import numpy as np
import pandas as pd

def get_datasets(force_trees = False , write_csv = True):
  csv_name = "/uboone/data/sdennis/consistency/pelee/numu_v08_00_00_48_0928.csv"
  if not force_trees:
    try: return pd.read_csv(csv_name)
    except: print("Falling back on trees")

  df_numu_MC_BNB = readers.get_frame([("/uboone/data/users/davidc/searchingfornues/v08_00_00_48/0928/SBNFit/numu/mc.root", 0.159)], ["weightSplineTimesTune"])
  # ~ df_numu_DIRT   = readers.get_frame([("/uboone/data/users/davidc/searchingfornues/v08_00_00_48/0928/SBNFit/numu/dirt.root", 0.649)], ["weightSplineTimesTune"])
  # ~ df_numu_EXT    = readers.get_frame([("/uboone/data/users/wospakrk/sbnfit_0928/numu/ext.root", 0.257)], ["weightTune"])
  
  df_numu = [df_numu_MC_BNB]
  # ~ df_numu = [df_numu_MC_BNB, df_numu_DIRT, df_numu_EXT]

  POT = 2.13#2.13E+20,now all dataframes are scaled to 1E+20, we only need to multiply the needed POT at the analysis level
  
  for df_i in df_numu:
      df_i.event_weight *= 1/POT

  df_numu_MC_BNB['IsDirt'] = 0
  # ~ df_numu_DIRT['IsDirt']   = 1
  # ~ df_numu_EXT['IsDirt']    = 2

  df_all = pd.concat(df_numu)
  
  df_all.sort_values(["run","subrun","event","enu_true"],inplace=True)
  
  if write_csv:
    df_all.to_csv(csv_name)
  
  return df_all

