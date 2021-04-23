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
  plot_breakdown_numu_1d(both_pelee_reco,x_range=my_e_range,nbins=40,quantity_func=get_ereco,x_title=pelee_reco_title)
  plt.savefig('both_numu_pelee_reco.png')
  print("Both, DLLEE Reco")
  plot_breakdown_numu_1d(both_dllee_reco,x_range=my_e_range,nbins=40,quantity_func=get_ereco,x_title=dllee_reco_title)
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
  
  both_pelee_reco["enu_reco_diff"] = both_pelee_reco["enu_reco_pelee"]-both_pelee_reco["enu_reco_dllee"]
  both_pelee_reco["enu_reco_minus_true_pelee"] = both_pelee_reco["enu_reco_pelee"]-both_pelee_reco["enu_true"]
  
  print("Both, Diff Reco")
  plot_breakdown_numu_1d(both_pelee_reco,x_range=[-400,400],
    quantity_func=lambda s: s.enu_reco_diff,
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
  
  # Ereco-Etrue 2d
  plot_2d(both_pelee_reco,normalise=True,
    x_quantity_func=get_etrue, x_title=true_title,
    y_quantity_func=lambda s: s.enu_reco_diff, y_title="PeLEE-DLLEE Reco Neutrino Energy [MeV]", y_range=[-100,100])
  plt.savefig('both_numu_reco_diff_vs_true.png')
  
  # investigate the two spikes in the bimodal distribution
  # Lower spike, diff of -60 to -20 MeV
  df_diff_lower = both_pelee_reco.loc[(both_pelee_reco["enu_reco_diff"]>-60.) & (both_pelee_reco["enu_reco_diff"]<-20.)]
  plot_breakdown_numu_1d(df_diff_lower,x_range=my_e_range,nbins=my_nbins,quantity_func=lambda s: s.enu_reco_pelee,x_title=pelee_reco_title)
  plt.savefig('both_numu_diff_lower_pelee_reco.png')
  plot_breakdown_numu_1d(df_diff_lower,x_range=my_e_range,nbins=my_nbins,quantity_func=lambda s: s.enu_reco_dllee,x_title=dllee_reco_title)
  plt.savefig('both_numu_diff_lower_dllee_reco.png')
  
  # Upper spike, diff of 20-80MeV
  df_diff_upper = both_pelee_reco.loc[(both_pelee_reco["enu_reco_diff"]>20.) & (both_pelee_reco["enu_reco_diff"]<80.)]
  plot_breakdown_numu_1d(df_diff_upper,x_range=my_e_range,nbins=my_nbins,quantity_func=lambda s: s.enu_reco_pelee,x_title=pelee_reco_title)
  plt.savefig('both_numu_diff_upper_pelee_reco.png')
  plot_breakdown_numu_1d(df_diff_upper,x_range=my_e_range,nbins=my_nbins,quantity_func=lambda s: s.enu_reco_dllee,x_title=dllee_reco_title)
  plt.savefig('both_numu_diff_upper_dllee_reco.png')
  
  df_diff_lower.to_csv("numu_diff_peak_lower.csv")
  df_diff_upper.to_csv("numu_diff_peak_upper.csv")
  
  plot_breakdown_numu_1d(df_diff_lower,x_range=[-200,200],nbins=40,quantity_func=lambda s: s.enu_reco_pelee-s.enu_true,x_title="PeLEE Ereco - Etrue [MeV]")
  plt.savefig('both_numu_diff_lower_pelee_reco_minus_true.png')
  plot_breakdown_numu_1d(df_diff_lower,x_range=[-200,200],nbins=40,quantity_func=lambda s: s.enu_reco_dllee-s.enu_true,x_title="DLLEE Ereco - Etrue [MeV]")
  plt.savefig('both_numu_diff_lower_dllee_reco_minus_true.png')
  
  plot_breakdown_numu_1d(df_diff_upper,x_range=[-200,200],nbins=40,quantity_func=lambda s: s.enu_reco_pelee-s.enu_true,x_title="PeLEE Ereco - Etrue [MeV]")
  plt.savefig('both_numu_diff_upper_pelee_reco_minus_true.png')
  plot_breakdown_numu_1d(df_diff_upper,x_range=[-200,200],nbins=40,quantity_func=lambda s: s.enu_reco_dllee-s.enu_true,x_title="DLLEE Ereco - Etrue [MeV]")
  plt.savefig('both_numu_diff_upper_dllee_reco_minus_true.png')
  
  
  plot_breakdown_numu_1d(pelee_numu_data,x_range=[-400,400],nbins=80,quantity_func=lambda s: s.enu_reco-s.enu_true,x_title="PeLEE Ereco - Etrue [MeV]")
  plt.savefig('pelee_reco_minus_true.png')
  plot_breakdown_numu_1d(dllee_numu_data,x_range=[-400,400],nbins=80,quantity_func=lambda s: s.enu_reco-s.enu_true,x_title="DLLEE Ereco - Etrue [MeV]")
  plt.savefig('dllee_reco_minus_true.png')
  
  
  
  df_compare = both_pelee_reco.loc[(both_pelee_reco["enu_reco_diff"]>20.) & (both_pelee_reco["enu_reco_diff"]<80.)&(both_pelee_reco["enu_reco_minus_true_pelee"]>40)]
  df_compare.to_csv("numu_in_both_pelee_overestimated.csv")
  
  # Debug
  db = pd.concat([df_diff_lower,df_diff_upper])
  plot_breakdown_numu_1d(db,x_range=[-400,400],
    quantity_func=lambda s: s.enu_reco_diff,
    x_title="PeLEE-DLLEE Reco Neutrino Energy [MeV]",
    nbins=40)
  plt.savefig('debug.png')

if __name__ == "__main__":
  main()
