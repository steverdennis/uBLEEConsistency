##################################################
##This code tries to read files from PeLEE group##
##################################################
import math
import ROOT as R
import pandas as pd
import numpy as np
from uBLEEConsistency import NuEvent

mytreename = "NeutrinoSelectionFilter"

to2dp = '{0:.2f}'

# list of files and their associated weight [(filename,wght),(filename,wght)]
# weight branches is list of branch names containing weights
def get_frame(files_with_weights,weight_branches):

  event_list = []
  for i,(filename,input_weight) in enumerate(files_with_weights):
    myfile = R.TFile(filename)
    assert(myfile.IsOpen())
    tree = myfile.Get(mytreename)

  #data_frame = pd.DataFrame()
    for eventi in tree:
      myevent = NuEvent()

      myevent.run                  = eventi.run
      myevent.subrun               = eventi.sub
      myevent.event                = eventi.evt
      myevent.selection            = 1
      myevent.nu_pdg_init          = eventi.nu_pdg
      myevent.nu_pdg_final         = eventi.nu_pdg
      myevent.IsNC                 = eventi.ccnc
      myevent.nu_interaction_mode  = eventi.interaction
      myevent.enu_true             = float(to2dp.format(1000.*eventi.nu_e))
      myevent.enu_reco             = float(to2dp.format(1000.*eventi.reco_e))
      myevent.lepton_theta_reco    = eventi.elecangle*180/math.pi
      myevent.lepton_energy_reco   = float(to2dp.format(1000.*eventi.elecenergy))

      myevent.event_weight = input_weight * np.prod([getattr(eventi,b) for b in weight_branches])
      #getattr(eventi,b) is eventi.b, while for ext files, b should be weightTune.

      #data_frame.append(myevent)
      event_list.append(myevent)
      
  df = pd.DataFrame(event_list)
  df.sort_values(["run","subrun","event","enu_true"],inplace=True)
  return df
