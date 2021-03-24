#!/usr/bin/env python
import ROOT as R
import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

import uBLEEConsistency.datasets.DLLEE_numu_tree as dllee_set
import uBLEEConsistency.datasets.PeLEE_numu_v08_00_00_48_0928 as pelee_set

from uBLEEConsistency.analysis.plot_tools import plot_breakdown_numu_1d,plot_2d

def get_ereco(s):
  return s.enu_reco
  
def get_etrue(s):
  return s.enu_true

def main():

  pelee_numu_data = pelee_set.get_datasets()
  print("Read ",len(pelee_numu_data),"PeLEE events")
  dllee_numu_data = dllee_set.get_datasets()
  print("Read ",len(dllee_numu_data),"DLLEE events")
  
  pelee_numu_data.sort_values(["run","subrun","event","enu_true"],inplace=True)
  dllee_numu_data.sort_values(["run","subrun","event","enu_true"],inplace=True)
  
  # DEBUG
  pelee_numu_data["event_weight"] = 1.
  dllee_numu_data["event_weight"] = 1.
  
  # ~ match_events_by = ["run","subrun","event","enu_true"]
  match_events_by = ["run","subrun","event"]
  # ~ match_events_by = ["enu_true"]

  same_pelee_dllee_numu = pd.merge(pelee_numu_data[match_events_by],dllee_numu_data[match_events_by])
  
  both_pelee_reco = pelee_numu_data.merge(same_pelee_dllee_numu)
  both_dllee_reco = dllee_numu_data.merge(same_pelee_dllee_numu)
  
  both_pelee_reco["enu_reco_pelee"] = pelee_numu_data["enu_reco"]
  both_pelee_reco["enu_reco_dllee"] = both_dllee_reco["enu_reco"]
  
  my_e_range = [150,1550]
  my_nbins = 15

  reco_title = 'Neutrino reconstructed energy [MeV]'
  pelee_reco_title = 'PeLEE Neutrino reconstructed energy [MeV]'
  dllee_reco_title = 'DLLEE Neutrino reconstructed energy [MeV]'
  true_title = 'Neutrino true energy [MeV]'
  print("PeLEE")
  plot_breakdown_numu_1d(pelee_numu_data,x_range=my_e_range,nbins=my_nbins,quantity_func=get_ereco,x_title=reco_title)
  plt.savefig('pelee_numu_reco.png')
  plot_breakdown_numu_1d(pelee_numu_data,x_range=my_e_range,nbins=my_nbins,quantity_func=get_etrue)
  plt.savefig('pelee_numu_true.png')
  print("DLLEE")
  plot_breakdown_numu_1d(dllee_numu_data,x_range=my_e_range,nbins=my_nbins,quantity_func=get_ereco,x_title=reco_title)
  plt.savefig('dllee_numu_reco.png')
  plot_breakdown_numu_1d(dllee_numu_data,x_range=my_e_range,nbins=my_nbins,quantity_func=get_etrue)
  plt.savefig('dllee_numu_true.png')
  
  # Ereco-Etrue 2d
  plot_2d(pelee_numu_data,normalise=True,
    x_quantity_func=get_ereco, x_title=pelee_reco_title,
    y_quantity_func=get_etrue, y_title=true_title)
  plt.savefig('pelee_numu_reco_vs_true.png')
  plot_2d(dllee_numu_data,normalise=True,
    x_quantity_func=get_ereco, x_title=dllee_reco_title,
    y_quantity_func=get_etrue, y_title=true_title)
  plt.savefig('dllee_numu_reco_vs_true.png')
  
  print("Both, PeLEE Reco")
  plot_breakdown_numu_1d(both_pelee_reco,x_range=my_e_range,nbins=my_nbins,quantity_func=get_ereco,x_title=pelee_reco_title)
  plt.savefig('both_numu_pelee_reco.png')
  print("Both, DLLEE Reco")
  plot_breakdown_numu_1d(both_dllee_reco,x_range=my_e_range,nbins=my_nbins,quantity_func=get_ereco,x_title=dllee_reco_title)
  plt.savefig('both_numu_dllee_reco.png')
  
  in_pelee_but_not_dllee = pelee_numu_data.merge(pd.concat([pelee_numu_data[match_events_by],same_pelee_dllee_numu]).drop_duplicates(keep=False))
  print("In PELEE but not DLLEE")
  plot_breakdown_numu_1d(in_pelee_but_not_dllee,x_range=my_e_range,nbins=my_nbins,quantity_func=get_ereco,x_title=reco_title)
  plt.savefig('pelee_numu_not_in_dllee_reco.png')
  plot_breakdown_numu_1d(in_pelee_but_not_dllee,x_range=my_e_range,nbins=my_nbins,quantity_func=get_etrue,x_title=true_title)
  plt.savefig('pelee_numu_not_in_dllee_true.png')
  
  in_dllee_but_not_pelee = dllee_numu_data.merge(pd.concat([dllee_numu_data[match_events_by],same_pelee_dllee_numu]).drop_duplicates(keep=False))
  print("In DLLEE but not PeLEE")
  plot_breakdown_numu_1d(in_dllee_but_not_pelee,x_range=my_e_range,nbins=my_nbins,quantity_func=get_ereco,x_title=reco_title)
  plt.savefig('dllee_numu_not_in_pelee_reco.png')
  plot_breakdown_numu_1d(in_dllee_but_not_pelee,x_range=my_e_range,nbins=my_nbins,quantity_func=get_etrue,x_title=true_title)
  plt.savefig('dllee_numu_not_in_pelee_true.png')
  
  both_pelee_reco["enu_reco_pelee"] = both_pelee_reco["enu_reco"]
  both_pelee_reco["enu_reco_dllee"] = both_dllee_reco["enu_reco"]
  
  #debug
  both_dllee_reco["enu_reco_pelee"] = both_pelee_reco["enu_reco"]
  both_dllee_reco["enu_reco_dllee"] = both_dllee_reco["enu_reco"]
  
  print("Both, Diff Reco")
  plot_breakdown_numu_1d(both_dllee_reco,x_range=[-400,400],
    quantity_func=lambda s: s.enu_reco_pelee-s.enu_reco_dllee,
    x_title="PeLEE-DLLEE Reco Neutrino Energy [MeV]",
    nbins=40)
  plt.savefig('both_numu_subtracted_reco.png')
  
  # 2D, comparing analysis Ereco
  plot_2d(both_pelee_reco,normalise=True,
    x_quantity_func=lambda s: s.enu_reco_pelee, x_title=pelee_reco_title,
    y_quantity_func=lambda s: s.enu_reco_dllee, y_title=dllee_reco_title)
  plt.savefig('both_numu_reco_comp.png')
  
  # Ereco-Etrue 2d
  plot_2d(both_pelee_reco,normalise=True,
    x_quantity_func=lambda s: s.enu_reco_pelee, x_title=pelee_reco_title,
    y_quantity_func=get_etrue, y_title=true_title)
  plt.savefig('both_numu_pelee_reco_vs_true.png')
  plot_2d(both_pelee_reco,normalise=True,
    x_quantity_func=lambda s: s.enu_reco_dllee, x_title=dllee_reco_title,
    y_quantity_func=get_etrue, y_title=true_title)
  plt.savefig('both_numu_dllee_reco_vs_true.png')

if __name__ == "__main__":
  main()
