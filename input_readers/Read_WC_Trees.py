##################################################
##This code tries to read files from WireCELL group##
##################################################
import ROOT as R
import pandas as pd
import numpy as np
from uBLEEConsistency import NuEvent

dirname = "wcpselection"
# ~ treenames = ["T_eval","T_KINEvars","T_PFeval","T_BDTvars"]
treenames = ["T_eval","T_PFeval","T_BDTvars"]

to2dp = '{0:.2f}'

# list of files and their associated weight [(filename,wght),(filename,wght)]
# weight branches is list of branch names containing weights
def get_frame(files_with_weights,weight_branches):

  event_list = []
  for i,(filename,input_weight) in enumerate(files_with_weights):
    myfile = R.TFile(filename)
    assert(myfile.IsOpen())
    trees = [myfile.Get(dirname+"/"+tn) for tn in treenames]
    main_tree = trees[0]
    for t in trees[1:]: main_tree.AddFriend(t)
    
  i = 0
  #data_frame = pd.DataFrame()
  for eventi in main_tree:
    # ~ if i > 100: break
    i+=1
    myevent = NuEvent()

    # DEBUG, before Pandas

    myevent.run                  = eventi.run
    myevent.subrun               = eventi.subrun
    myevent.event                = eventi.event
    myevent.selection            = 1
    myevent.nu_pdg_init          = -1 # get this properly
    myevent.nu_pdg_final         = -1 # get this properly
    myevent.IsNC                 = 0  # get this properly
    myevent.nu_interaction_mode  = eventi.neutrino_type
    myevent.enu_true             = float(to2dp.format(1.)) # get this properly
    myevent.enu_reco             = float(to2dp.format(eventi.kine_reco_Enu))
    myevent.lepton_theta_reco    = -999#Not sure
    myevent.lepton_momentum_reco = -999.

    myevent.event_weight = input_weight * np.prod([getattr(eventi,b) for b in weight_branches])
    #getattr(eventi,b) is eventi.b, while for ext files, b should be weightTune.

    myevent.reco_nuvtx_x = eventi.reco_nuvtxX
    myevent.reco_nuvtx_y = eventi.reco_nuvtxY
    myevent.reco_nuvtx_z = eventi.reco_nuvtxZ

    myevent.numu_score   = eventi.numu_score
    myevent.nue_score    = eventi.nue_score
    myevent.numu_cc_flag = eventi.numu_cc_flag
    # ~ myevent.nue_cc_flag  = eventi.nue_cc_flag

    myevent.match_isFC = eventi.match_isFC

    #data_frame.append(myevent)
    event_list.append(myevent)
      
  df = pd.DataFrame(event_list)
  df.sort_values(["run","subrun","event","enu_true"],inplace=True)
  return df
