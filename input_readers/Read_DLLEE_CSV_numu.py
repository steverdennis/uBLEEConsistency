import math
import pandas
import numpy as np


# enu_reco and weights are added later
columns = {
  "run"             : "run",
  "subrun"          : "subrun",
  "event"           : "event",
  "EnuTrue"         : "enu_true",
  "ccnc"            : "IsNC",
  "Lepton_ThetaReco": "lepton_theta_reco",
  "Muon_Edep"       : "lepton_energy_reco",
  "Proton_ThetaReco": "proton_theta_reco",
  "Proton_Edep"     : "proton_energy_reco",
  "Xreco"           : "reco_nuvtx_x",
  "Yreco"           : "reco_nuvtx_y",
  "Zreco"           : "reco_nuvtx_z",
}

weights = ["GENIE_weight","LEE_weight","POTweight"]

def read_csv(filename,ereco_name="Enu_1m1p"):
  delim = ","
  if ".txt" in filename: delim = " "
  input_frame = pandas.read_csv(filename,delim)
  
  # put in a dummy true neutrino energy for non-neutrino events here
  if not "EnuTrue" in input_frame:
    input_frame["EnuTrue"] = -999.
  # and dummy weights for any we're missing (eg neutrino weights for non-neutrino events)
  for w in weights:
    if not w in input_frame:
      input_frame[w] = 1.
      
  # make a pure weight column based on the product of existing weights
  input_frame["event_weight"] = input_frame.apply(lambda row: np.prod([getattr(row,w) for w in weights]),axis=1)
  
  # no additional selection here
  selected_frame = input_frame
  
  needed_columns = dict(columns)
  needed_columns[ereco_name] = "enu_reco"
  needed_columns["event_weight"] = "event_weight"
  
  output_frame = selected_frame[needed_columns.keys()]
  output_frame = output_frame.rename(needed_columns,axis="columns")
  
  output_frame.sort_values(["run","subrun","event","enu_true"],inplace=True)
  
  # add a dummy neutrino type, interaction mode
  output_frame["nu_pdg_init"        ] = 14
  output_frame["nu_pdg_final"       ] = 14
  output_frame["nu_interaction_mode"] = 0 # QE
  
  # Convert radians to degrees
  output_frame["lepton_theta_reco"]*=180./math.pi
  
  return output_frame
