#!/usr/bin/env python
import sys

import ROOT as R
import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

import uBLEEConsistency.datasets.DLLEE_nue_tree_run1 as dllee_set
import uBLEEConsistency.datasets.WC_nue as wc_set

from uBLEEConsistency.analysis.plot_tools import plot_breakdown_nue_1d,plot_2d,plot_1d

def get_ereco(s):
  return s.enu_reco
  
def get_etrue(s):
  return s.enu_true

def main():

  wc_nue_data = wc_set.get_datasets()
  print("Read ",len(wc_nue_data),"WireCell events")
  dllee_nue_data = dllee_set.get_datasets()
  print("Read ",len(dllee_nue_data),"DLLEE events")
  
  wc_nue_data.sort_values(["run","subrun","event","enu_true"],inplace=True)
  dllee_nue_data.sort_values(["run","subrun","event","enu_true"],inplace=True)
  
  # DEBUG
  wc_nue_data["event_weight"] = 1.
  dllee_nue_data["event_weight"] = 1.
  
  # ~ match_events_by = ["run","subrun","event","enu_true"]
  match_events_by = ["run","subrun","event"]
  # ~ match_events_by = ["enu_true"]

  same_wc_dllee_nue = pd.merge(wc_nue_data[match_events_by],dllee_nue_data[match_events_by])
  
  both_wc_reco = wc_nue_data.merge(same_wc_dllee_nue)
  both_dllee_reco = dllee_nue_data.merge(same_wc_dllee_nue)
  
  both_wc_reco["enu_reco_wc"]         = both_wc_reco["enu_reco"]
  both_wc_reco["enu_reco_dllee"]      = both_dllee_reco["enu_reco"]
  both_wc_reco["enu_true"]            = both_dllee_reco["enu_true"]
  both_wc_reco["nu_pdg_final"]        = both_dllee_reco["nu_pdg_final"]
  both_wc_reco["IsNC"]                = both_dllee_reco["IsNC"]
  both_wc_reco["nu_interaction_mode"] = both_dllee_reco["nu_interaction_mode"]
  
  both_dllee_reco["enu_reco_wc"]    = both_wc_reco["enu_reco"]
  both_dllee_reco["enu_reco_dllee"] = both_dllee_reco["enu_reco"]
  
  my_e_range = [0,1600]
  my_nbins = 16

  reco_title = 'Neutrino reconstructed energy [MeV]'
  wc_reco_title = 'WireCell Neutrino reconstructed energy [MeV]'
  dllee_reco_title = 'DLLEE Neutrino reconstructed energy [MeV]'
  true_title = 'Neutrino true energy [MeV]'
  print("WireCell")
  plot_1d(wc_nue_data,x_range=my_e_range,nbins=my_nbins,quantity_func=get_ereco,x_title=reco_title,print_stream=sys.stdout)
  plt.savefig('wc_nue_reco.png')
  # ~ plot_breakdown_nue_1d(wc_nue_data,x_range=my_e_range,nbins=my_nbins,quantity_func=get_etrue)
  # ~ plt.savefig('wc_nue_true.png')
  
  print("DLLEE")
  plot_1d(dllee_nue_data,x_range=my_e_range,nbins=my_nbins,quantity_func=get_ereco,x_title=reco_title,print_stream=sys.stdout)
  plt.savefig('dllee_nue_reco.png')
  plot_breakdown_nue_1d(dllee_nue_data,x_range=my_e_range,nbins=my_nbins,quantity_func=get_etrue)
  plt.savefig('dllee_nue_true.png')
  
  # Ereco-Etrue 2d
  # ~ plot_2d(wc_nue_data,normalise=True,
    # ~ x_quantity_func=get_ereco, x_title=wc_reco_title,
    # ~ y_quantity_func=get_etrue, y_title=true_title)
  # ~ plt.savefig('wc_nue_reco_vs_true.png')
  plot_2d(dllee_nue_data,normalise=True,
    x_quantity_func=get_ereco, x_title=dllee_reco_title,
    y_quantity_func=get_etrue, y_title=true_title)
  plt.savefig('dllee_nue_reco_vs_true.png')
  
  print("Both, WireCell Reco")
  plot_breakdown_nue_1d(both_dllee_reco,x_range=my_e_range,nbins=40,quantity_func=lambda s: s.enu_reco_wc,x_title=wc_reco_title,print_stream=sys.stdout)
  plt.savefig('both_nue_wc_reco.png')
  print("Both, DLLEE Reco")
  plot_breakdown_nue_1d(both_dllee_reco,x_range=my_e_range,nbins=40,quantity_func=get_ereco,x_title=dllee_reco_title)
  plt.savefig('both_nue_dllee_reco.png')
  
  in_wc_but_not_dllee = wc_nue_data.merge(pd.concat([wc_nue_data[match_events_by],same_wc_dllee_nue]).drop_duplicates(keep=False))
  print("In WireCell but not DLLEE")
  plot_1d(in_wc_but_not_dllee,x_range=my_e_range,nbins=my_nbins,quantity_func=get_ereco,x_title=reco_title)
  plt.savefig('wc_nue_not_in_dllee_reco.png')
  # ~ plot_breakdown_nue_1d(in_wc_but_not_dllee,x_range=my_e_range,nbins=my_nbins,quantity_func=get_etrue,x_title=true_title)
  # ~ plt.savefig('wc_nue_not_in_dllee_true.png')
  
  in_dllee_but_not_wc = dllee_nue_data.merge(pd.concat([dllee_nue_data[match_events_by],same_wc_dllee_nue]).drop_duplicates(keep=False))
  print("In DLLEE but not WireCell")
  plot_breakdown_nue_1d(in_dllee_but_not_wc,x_range=my_e_range,nbins=my_nbins,quantity_func=get_ereco,x_title=reco_title)
  plt.savefig('dllee_nue_not_in_wc_reco.png')
  plot_breakdown_nue_1d(in_dllee_but_not_wc,x_range=my_e_range,nbins=my_nbins,quantity_func=get_etrue,x_title=true_title)
  plt.savefig('dllee_nue_not_in_wc_true.png')
  
  both_wc_reco["enu_reco_wc"] = both_wc_reco["enu_reco"]
  both_wc_reco["enu_reco_dllee"] = both_dllee_reco["enu_reco"]
  
  #debug
  both_dllee_reco["enu_reco_wc"] = both_wc_reco["enu_reco"]
  both_dllee_reco["enu_reco_dllee"] = both_dllee_reco["enu_reco"]
  
  both_wc_reco["enu_reco_diff"]          = both_wc_reco["enu_reco_wc"]-both_wc_reco["enu_reco_dllee"]
  both_wc_reco["enu_reco_minus_true_wc"] = both_wc_reco["enu_reco_wc"]-both_wc_reco["enu_true"]
  
  print("Both, Diff Reco")
  plot_breakdown_nue_1d(both_wc_reco,x_range=[-400,400],
    quantity_func=lambda s: s.enu_reco_diff,
    x_title="WireCell-DLLEE Reco Neutrino Energy [MeV]",
    nbins=40)
  plt.savefig('both_nue_subtracted_reco.png')
  
  # 2D, comparing analysis Ereco
  plot_2d(both_wc_reco,normalise=True,
    x_quantity_func=lambda s: s.enu_reco_wc, x_title=wc_reco_title,
    y_quantity_func=lambda s: s.enu_reco_dllee, y_title=dllee_reco_title)
  plt.savefig('both_nue_reco_comp.png')
  
  # Ereco-Etrue 2d
  plot_2d(both_wc_reco,normalise=True,
    x_quantity_func=lambda s: s.enu_reco_wc, x_title=wc_reco_title,
    y_quantity_func=get_etrue, y_title=true_title)
  plt.savefig('both_nue_wc_reco_vs_true.png')
  plot_2d(both_wc_reco,normalise=True,
    x_quantity_func=lambda s: s.enu_reco_dllee, x_title=dllee_reco_title,
    y_quantity_func=get_etrue, y_title=true_title)
  plt.savefig('both_nue_dllee_reco_vs_true.png')
  
  # Ereco-Etrue 2d
  plot_2d(both_wc_reco,normalise=True,
    x_quantity_func=get_etrue, x_title=true_title,
    y_quantity_func=lambda s: s.enu_reco_diff, y_title="WireCell-DLLEE Reco Neutrino Energy [MeV]", y_range=[-100,100])
  plt.savefig('both_nue_reco_diff_vs_true.png')

if __name__ == "__main__":
  main()
