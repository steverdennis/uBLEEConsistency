from uBLEEConsistency.input_readers import Read_DLLEE_CSV

import pandas as pd

def get_datasets():

  files = [
   "/uboone/app/users/ritay/forCons/numu/numu_run1_Jan13_forConsGroup.csv",
   "/uboone/app/users/ritay/forCons/numu/numu_run2_Jan13_forConsGroup.csv",
   "/uboone/app/users/ritay/forCons/numu/numu_run3_Jan13_forConsGroup.csv",
   # ~ "/uboone/app/users/ritay/forCons/numu/ext_run1_Jan13_forConsGroup.csv",
   # ~ "/uboone/app/users/ritay/forCons/numu/ext_run3_Jan13_forConsGroup.csv"
  ]
  
  ereco_varname = "Enu_1m1p"

  frames = [Read_DLLEE_CSV.read_csv(f,ereco_varname) for f in files]

  df_all = pd.concat(frames)
  
  return df_all

