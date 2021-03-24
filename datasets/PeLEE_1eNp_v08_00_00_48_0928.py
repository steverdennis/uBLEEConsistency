
from uBLEEConsistency.input_readers import Read_PeLEE_Trees as readers
import numpy as np
import pandas as pd


def get_datasets():
  
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
  
  return df_all

