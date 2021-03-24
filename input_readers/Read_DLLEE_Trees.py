import ROOT as R
import pandas as pd
import numpy as np

from uBLEEConsistency import NuEvent

#################
##Reading files##
#################

to2dp = '{0:.2f}'

def get_frame(files,treename):
  
  tree = R.TChain(treename)
  for f in files: tree.AddFile(f)
  
  event_list = []
  
  i = 0
  for eventi in tree:
    i+=1
    myevent = NuEvent()
    
    myevent.run                  = eventi.run
    myevent.subrun               = eventi.subrun
    myevent.event                = eventi.event
    myevent.selection            = 1
    myevent.nu_pdg_init          = eventi.nu_pdg
    myevent.nu_pdg_final         = eventi.nu_pdg
    myevent.IsNC                 = eventi.nu_interaction_ccnc
    myevent.nu_interaction_mode  = eventi.nu_interaction_mode
    myevent.enu_true             = float(to2dp.format(eventi.nu_energy_true))
    myevent.enu_reco             = float(to2dp.format(eventi.nu_energy_reco))
    myevent.event_weight         = eventi.xsec_corr_weight#We acutally need one more term of correction from DLLEE group
    myevent.lepton_theta_reco    = eventi.lepton_theta_reco
    myevent.lepton_momentum_reco = -999.
    
    #data_frame.append(myevent)
    event_list.append(myevent)
    
  df = pd.DataFrame(event_list)
  df.sort_values(["run","subrun","event","enu_true"],inplace=True)
  return df
