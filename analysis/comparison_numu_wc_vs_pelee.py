#!/usr/bin/env python
import sys

import ROOT as R
import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

import uBLEEConsistency.datasets.PeLEE_numu_v08_00_00_48_0928 as pelee_set
import uBLEEConsistency.datasets.WC_numu as wc_set

from uBLEEConsistency.analysis.plot_tools import plot_breakdown_numu_1d,plot_2d,plot_1d

def get_ereco(s):
  return s.enu_reco
  
def get_etrue(s):
  return s.enu_true

def main():

  wc_numu_data = wc_set.get_datasets()
  print("Read ",len(wc_numu_data),"WireCell events")
  pelee_numu_data = pelee_set.get_datasets()
  print("Read ",len(pelee_numu_data),"PeLEE events")
  
  wc_numu_data.sort_values(["run","subrun","event","enu_true"],inplace=True)
  pelee_numu_data.sort_values(["run","subrun","event","enu_true"],inplace=True)
  
  # DEBUG
  wc_numu_data["event_weight"] = 1.
  pelee_numu_data["event_weight"] = 1.
  
  # ~ match_events_by = ["run","subrun","event","enu_true"]
  match_events_by = ["run","subrun","event"]
  # ~ match_events_by = ["enu_true"]

  same_wc_pelee_numu = pd.merge(wc_numu_data[match_events_by],pelee_numu_data[match_events_by])
  
  print("Same WC, PeLEE\n ", same_wc_pelee_numu)
  
  both_wc_reco = wc_numu_data.merge(same_wc_pelee_numu)
  both_pelee_reco = pelee_numu_data.merge(same_wc_pelee_numu)
  
  both_wc_reco["enu_reco_wc"]         = both_wc_reco["enu_reco"]
  both_wc_reco["enu_reco_pelee"]      = both_pelee_reco["enu_reco"]
  both_wc_reco["enu_true"]            = both_pelee_reco["enu_true"]
  both_wc_reco["nu_pdg_final"]        = both_pelee_reco["nu_pdg_final"]
  both_wc_reco["IsNC"]                = both_pelee_reco["IsNC"]
  both_wc_reco["nu_interaction_mode"] = both_pelee_reco["nu_interaction_mode"]
  
  both_pelee_reco["enu_reco_wc"]    = both_wc_reco["enu_reco"]
  both_pelee_reco["enu_reco_pelee"] = both_pelee_reco["enu_reco"]
  
  my_e_range = [150,1550]
  my_nbins = 15

  reco_title = 'Neutrino reconstructed energy [MeV]'
  wc_reco_title = 'WireCell Neutrino reconstructed energy [MeV]'
  pelee_reco_title = 'PeLEE Neutrino reconstructed energy [MeV]'
  true_title = 'Neutrino true energy [MeV]'
  print("WireCell")
  plot_1d(wc_numu_data,x_range=my_e_range,nbins=my_nbins,quantity_func=get_ereco,x_title=reco_title,print_stream=sys.stdout)
  plt.savefig('wc_numu_reco.png')
  # ~ plot_breakdown_numu_1d(wc_numu_data,x_range=my_e_range,nbins=my_nbins,quantity_func=get_etrue)
  # ~ plt.savefig('wc_numu_true.png')
  
  print("PeLEE")
  plot_breakdown_numu_1d(pelee_numu_data,x_range=my_e_range,nbins=my_nbins,quantity_func=get_ereco,x_title=reco_title,print_stream=sys.stdout)
  plt.savefig('pelee_numu_reco.png')
  plot_breakdown_numu_1d(pelee_numu_data,x_range=my_e_range,nbins=my_nbins,quantity_func=get_etrue)
  plt.savefig('pelee_numu_true.png')
  
  # Ereco-Etrue 2d
  # ~ plot_2d(wc_numu_data,normalise=True,
    # ~ x_quantity_func=get_ereco, x_title=wc_reco_title,
    # ~ y_quantity_func=get_etrue, y_title=true_title)
  # ~ plt.savefig('wc_numu_reco_vs_true.png')
  plot_2d(pelee_numu_data,normalise=True,
    x_quantity_func=get_ereco, x_title=pelee_reco_title,
    y_quantity_func=get_etrue, y_title=true_title)
  plt.savefig('pelee_numu_reco_vs_true.png')
  
  print("Both, WireCell Reco")
  plot_breakdown_numu_1d(both_pelee_reco,x_range=my_e_range,nbins=40,quantity_func=lambda s: s.enu_reco_wc,x_title=wc_reco_title,print_stream=sys.stdout)
  plt.savefig('both_numu_wc_reco.png')
  print("Both, PeLEE Reco")
  plot_breakdown_numu_1d(both_pelee_reco,x_range=my_e_range,nbins=40,quantity_func=get_ereco,x_title=pelee_reco_title)
  plt.savefig('both_numu_pelee_reco.png')
  
  in_wc_but_not_pelee = wc_numu_data.merge(pd.concat([wc_numu_data[match_events_by],same_wc_pelee_numu]).drop_duplicates(keep=False))
  print("In WireCell but not PeLEE")
  plot_1d(in_wc_but_not_pelee,x_range=my_e_range,nbins=my_nbins,quantity_func=get_ereco,x_title=reco_title)
  plt.savefig('wc_numu_not_in_pelee_reco.png')
  # ~ plot_breakdown_numu_1d(in_wc_but_not_pelee,x_range=my_e_range,nbins=my_nbins,quantity_func=get_etrue,x_title=true_title)
  # ~ plt.savefig('wc_numu_not_in_pelee_true.png')
  
  in_pelee_but_not_wc = pelee_numu_data.merge(pd.concat([pelee_numu_data[match_events_by],same_wc_pelee_numu]).drop_duplicates(keep=False))
  print("In PeLEE but not WireCell")
  plot_breakdown_numu_1d(in_pelee_but_not_wc,x_range=my_e_range,nbins=my_nbins,quantity_func=get_ereco,x_title=reco_title)
  plt.savefig('pelee_numu_not_in_wc_reco.png')
  plot_breakdown_numu_1d(in_pelee_but_not_wc,x_range=my_e_range,nbins=my_nbins,quantity_func=get_etrue,x_title=true_title)
  plt.savefig('pelee_numu_not_in_wc_true.png')
  
  both_wc_reco["enu_reco_wc"] = both_wc_reco["enu_reco"]
  both_wc_reco["enu_reco_pelee"] = both_pelee_reco["enu_reco"]
  
  #debug
  both_pelee_reco["enu_reco_wc"] = both_wc_reco["enu_reco"]
  both_pelee_reco["enu_reco_pelee"] = both_pelee_reco["enu_reco"]
  
  both_wc_reco["enu_reco_diff"]          = both_wc_reco["enu_reco_wc"]-both_wc_reco["enu_reco_pelee"]
  both_wc_reco["enu_reco_minus_true_wc"] = both_wc_reco["enu_reco_wc"]-both_wc_reco["enu_true"]
  
  print("Both, Diff Reco")
  plot_breakdown_numu_1d(both_wc_reco,x_range=[-400,400],
    quantity_func=lambda s: s.enu_reco_diff,
    x_title="WireCell-PeLEE Reco Neutrino Energy [MeV]",
    nbins=40)
  plt.savefig('both_numu_subtracted_reco.png')
  
  # 2D, comparing analysis Ereco
  plot_2d(both_wc_reco,normalise=True,
    x_quantity_func=lambda s: s.enu_reco_wc, x_title=wc_reco_title,
    y_quantity_func=lambda s: s.enu_reco_pelee, y_title=pelee_reco_title)
  plt.savefig('both_numu_reco_comp.png')
  
  # Ereco-Etrue 2d
  plot_2d(both_wc_reco,normalise=True,
    x_quantity_func=lambda s: s.enu_reco_wc, x_title=wc_reco_title,
    y_quantity_func=get_etrue, y_title=true_title)
  plt.savefig('both_numu_wc_reco_vs_true.png')
  plot_2d(both_wc_reco,normalise=True,
    x_quantity_func=lambda s: s.enu_reco_pelee, x_title=pelee_reco_title,
    y_quantity_func=get_etrue, y_title=true_title)
  plt.savefig('both_numu_pelee_reco_vs_true.png')
  
  # Ereco-Etrue 2d
  plot_2d(both_wc_reco,normalise=True,
    x_quantity_func=get_etrue, x_title=true_title,
    y_quantity_func=lambda s: s.enu_reco_diff, y_title="WireCell-PeLEE Reco Neutrino Energy [MeV]", y_range=[-100,100])
  plt.savefig('both_numu_reco_diff_vs_true.png')

if __name__ == "__main__":
  main()
