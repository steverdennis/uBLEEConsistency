#import uBLEEConsistency
from uBLEEConsistency.input_readers import Read_PeLEE_Trees_truthonly as readers
import numpy as np
import pandas as pd

def get_datasets(force_trees =False , write_csv = True):
  csv_name = "/uboone/data/sdennis/consistency/pelee/all_preselec_truth_v08_00_00_48_0928.csv"
  # ~ csv_name = "/uboone/data/sdennis/consistency/pelee/nue_preselec_truth_v08_00_00_48_0928.csv"
  if not force_trees:
    try: return pd.read_csv(csv_name)
    except: print("Falling back on trees")
    
  basepath = "/uboone/data/users/davidc/searchingfornues/v08_00_00_48/0928/"
  subpaths = [
    "run1/numupresel/prodgenie_bnb_nu_uboone_overlay_mcc9.1_v08_00_00_26_filter_run1_reco2_reco2.root",
    "run2/numupresel/prodgenie_bnb_nu_uboone_overlay_mcc9.1_v08_00_00_26_filter_run2_reco2_D1D2_reco2.root",
    "run3/numupresel/prodgenie_bnb_nu_uboone_overlay_mcc9.1_v08_00_00_26_filter_run3_reco2_G_reco2_newtune.root",
    "run1/numupresel/prodgenie_bnb_intrinsice_nue_uboone_overlay_mcc9.1_v08_00_00_26_run1_reco2_reco2.root",
    "run2/numupresel/prodgenie_bnb_intrinsic_nue_overlay_run2_v08_00_00_35_run2a_reco2_reco2.root",
    "run3/numupresel/prodgenie_bnb_intrinsice_nue_uboone_overlay_mcc9.1_v08_00_00_26_run3_reco2_reco2.root",
    "run1/nuepresel/prodgenie_bnb_nu_uboone_overlay_mcc9.1_v08_00_00_26_filter_run1_reco2_reco2.root",
    "run2/nuepresel/prodgenie_bnb_nu_uboone_overlay_mcc9.1_v08_00_00_26_filter_run2_reco2_D1D2_reco2.root",
    "run3/nuepresel/prodgenie_bnb_nu_uboone_overlay_mcc9.1_v08_00_00_26_filter_run3_reco2_G_reco2.root",
    "run1/nuepresel/prodgenie_bnb_intrinsice_nue_uboone_overlay_mcc9.1_v08_00_00_26_run1_reco2_reco2.root",
    "run2/nuepresel/prodgenie_bnb_intrinsic_nue_overlay_run2_v08_00_00_35_run2a_reco2_reco2.root",
    "run3/nuepresel/prodgenie_bnb_intrinsice_nue_uboone_overlay_mcc9.1_v08_00_00_26_run3_reco2_reco2.root",
    ]
  
  files_and_weights = [(basepath+sp,1.) for sp in subpaths]
  weights = [""]
  
  df_list = [readers.get_frame(files_and_weights, weights)]

  df_all = pd.concat(df_list)
  
  df_all.sort_values(["run","subrun","event","enu_true"],inplace=True)
  
  df_all.drop_duplicates(inplace=True)
  
  if write_csv:
    df_all.to_csv(csv_name)
  
  return df_all

