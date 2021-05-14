##################################################
##This code tries to read files from PeLEE group##
##################################################
import ROOT as R
import pandas as pd
import numpy as np
from uBLEEConsistency import NuEvent

mytreename = "nuselection/NeutrinoSelectionFilter"

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
      
      myevent.nu_pdg_init          = eventi.nu_pdg
      myevent.nu_pdg_final         = eventi.nu_pdg
      myevent.IsNC                 = eventi.ccnc
      myevent.nu_interaction_mode  = eventi.interaction
      myevent.enu_true             = float(to2dp.format(1000.*eventi.nu_e))

      myevent.event_weight = 1.

      event_list.append(myevent)
    #end event loop
  #end file loop
      
  df = pd.DataFrame(event_list)
  df.sort_values(["run","subrun","event","enu_true"],inplace=True)
  return df
