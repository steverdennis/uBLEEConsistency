
from uBLEEConsistency.input_readers import Read_PeLEE_Trees as readers
import numpy as np
import pandas as pd


def get_datasets(force_trees =False , write_csv = True):
  
  csv_name = "/uboone/data/sdennis/consistency/pelee/nue_1eNp_v08_00_00_48_0928.csv"
  if not force_trees:
    try: return pd.read_csv(csv_name)
    except: print("Falling back on trees")
    
  def get_frame(filename,weight):
    return readers.get_frame([(filename,weight)],weight_branches=["weightSplineTimesTune"])

  df_1e1p_nue_BNB = get_frame("/uboone/data/users/davidc/searchingfornues/v08_00_00_48/0928/SBNFit/1eNp/nue.root", 3.55E-3)
  df_1e1p_MC_BNB  = get_frame("/uboone/data/users/davidc/searchingfornues/v08_00_00_48/0928/SBNFit/1eNp/mc.root" , 1.87E-1)

  df_1e1p = [df_1e1p_nue_BNB,df_1e1p_MC_BNB]

  POT = 6.86E20
  
  for df_i in df_1e1p:
    df_i.event_weight *= 1/POT

  df_1e1p_nue_BNB['IsDirt'] = 0
  df_1e1p_MC_BNB['IsDirt'] = 0

  df_all = pd.concat(df_1e1p)
  
  df_all.sort_values(["run","subrun","event","enu_true"],inplace=True)
  
  if write_csv:
    df_all.to_csv(csv_name)
  
  return df_all

