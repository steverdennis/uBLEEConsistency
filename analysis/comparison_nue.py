#!/usr/bin/env python
import sys
import ROOT as R
import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt


import uBLEEConsistency.datasets.PeLEE_1eNp_v08_00_00_48_0928 as pelee_set
import uBLEEConsistency.datasets.PeLEE_1e0p_v08_00_00_48_0928 as pelee_set2
import uBLEEConsistency.datasets.DLLEE_nue_CSV as dllee_set
import uBLEEConsistency.datasets.WC_nue as wc_set

from uBLEEConsistency.analysis.plot_tools import plot_breakdown_nue_1d,plot_1d,plot_2d

# ~ import uBLEEConsistency.utilities.truth_utils as truth_utils

def get_ereco(s):
  return s.enu_reco
  
def get_etrue(s):
  return s.enu_true
  
def get_elep(s):
  return s.lepton_energy_reco
  
def get_thetalep(s):
  return s.lepton_theta_reco

def main():
  pelee_nue_data = pd.concat([pelee_set.get_datasets(),pelee_set2.get_datasets()])
  print("Read ",len(pelee_nue_data),"PeLEE events")
  dllee_nue_data = dllee_set.get_datasets()
  print("Read ",len(dllee_nue_data),"DLLEE events")
  wc_nue_data = wc_set.get_datasets()
  print("Read ",len(wc_nue_data),"WireCell events")
  
  # ~ truth_skim = truth_skim.get_datasets()
  # ~ truth_utils.match_truth(pelee_nue_data,dllee_nue_data,wc_nue_data)
  
  pelee_nue_data.sort_values(["run","subrun","event","enu_true"],inplace=True)
  dllee_nue_data.sort_values(["run","subrun","event","enu_true"],inplace=True)
  wc_nue_data.sort_values   (["run","subrun","event","enu_true"],inplace=True)
  
  # DEBUG
  pelee_nue_data["event_weight"] = 1.
  dllee_nue_data["event_weight"] = 1.
  wc_nue_data   ["event_weight"] = 1.
  
  match_events_by = ["run","subrun","event"]

  same_pelee_dllee_nue = pd.merge(pelee_nue_data      [match_events_by], dllee_nue_data[match_events_by])
  same_pelee_wc_nue    = pd.merge(pelee_nue_data      [match_events_by], wc_nue_data   [match_events_by])
  same_dllee_wc_nue    = pd.merge(dllee_nue_data      [match_events_by], wc_nue_data   [match_events_by])
  same_all_nue         = pd.merge(same_pelee_dllee_nue[match_events_by], wc_nue_data   [match_events_by])
  
  both_pl_dl_with_pl_reco = pelee_nue_data.merge(same_pelee_dllee_nue)
  both_pl_dl_with_dl_reco = dllee_nue_data.merge(same_pelee_dllee_nue)
  
  both_pl_wc_with_pl_reco = pelee_nue_data.merge(same_pelee_wc_nue)
  both_pl_wc_with_wc_reco = wc_nue_data   .merge(same_pelee_wc_nue)
  
  both_pl_wc_with_pl_reco = pelee_nue_data.merge(same_pelee_wc_nue)
  both_pl_wc_with_wc_reco = wc_nue_data   .merge(same_pelee_wc_nue)
  
  # Copy over neutrino truth from PL to and WC, change this later.
  both_pl_dl_with_dl_reco["nu_interaction_mode"] = both_pl_dl_with_pl_reco["nu_interaction_mode"]
  both_pl_dl_with_dl_reco["nu_pdg_final"       ] = both_pl_dl_with_pl_reco["nu_pdg_final"]
  both_pl_wc_with_wc_reco["nu_interaction_mode"] = both_pl_dl_with_pl_reco["nu_interaction_mode"]
  both_pl_wc_with_wc_reco["nu_pdg_final"       ] = both_pl_dl_with_pl_reco["nu_pdg_final"]
  
  my_e_range = [0,1600]
  my_nbins = 16
  my_theta_range = [0.,180.]
  my_nbins_theta = 36
  
  ereco_title        = 'Neutrino reconstructed energy [MeV]'
  pelee_ereco_title  = 'PeLEE Neutrino reconstructed energy [MeV]'
  dllee_ereco_title  = 'DLLEE Neutrino reconstructed energy [MeV]'
  wc_ereco_title     = 'Wire-Cell Neutrino reconstructed energy [MeV]'
  etrue_title        = 'Neutrino true energy [MeV]'
  ereco_lepton_title = 'Reco Electron reconstructed energy [MeV]'
  theta_lepton_title = 'Reco Electron angle [deg]'
  ereco_proton_title = 'Reco Proton reconstructed energy [MeV]'
  theta_proton_title = 'Reco Proton angle [deg]'
  pelee_thetalep_title  = 'PeLEE Electron angle [deg]'
  dllee_thetalep_title  = 'DLLEE Electron angle [deg]'
  
  print("PeLEE")
  plot_breakdown_nue_1d(pelee_nue_data,x_range=my_e_range,nbins=my_nbins,quantity_func=get_ereco,x_title=ereco_title,print_stream=sys.stdout)
  plt.savefig('pelee_nue_reco.png')
  plot_breakdown_nue_1d(pelee_nue_data,x_range=my_e_range,nbins=my_nbins,quantity_func=get_etrue,x_title=etrue_title)
  plt.savefig('pelee_nue_true.png')
  plot_breakdown_nue_1d(pelee_nue_data,x_range=my_e_range,nbins=my_nbins,quantity_func=get_elep,x_title=ereco_lepton_title)
  plt.savefig('pelee_nue_elep.png')
  plot_breakdown_nue_1d(pelee_nue_data,x_range=my_theta_range,nbins=my_nbins_theta,quantity_func=get_thetalep,x_title=theta_lepton_title)
  plt.savefig('pelee_nue_thetalep.png')
  
  print("DLLEE")
  plot_1d(dllee_nue_data,x_range=my_e_range,nbins=my_nbins,quantity_func=get_ereco,x_title=ereco_title,print_stream=sys.stdout)
  plt.savefig('dllee_nue_reco.png')
  plot_1d(dllee_nue_data,x_range=my_e_range,nbins=my_nbins,quantity_func=get_etrue,x_title=etrue_title)
  plt.savefig('dllee_nue_true.png')
  plot_1d(dllee_nue_data,x_range=my_e_range,nbins=my_nbins,quantity_func=get_elep,x_title=ereco_lepton_title)
  plt.savefig('dllee_nue_elep.png')
  plot_1d(dllee_nue_data,x_range=my_theta_range,nbins=my_nbins_theta,quantity_func=get_thetalep,x_title=theta_lepton_title)
  plt.savefig('dllee_nue_thetalep.png')
  
  print("WireCell")
  plot_breakdown_nue_1d(wc_nue_data,x_range=my_e_range,nbins=my_nbins,quantity_func=get_ereco,x_title=ereco_title,print_stream=sys.stdout)
  plt.savefig('wc_nue_reco.png')
  # ~ plot_breakdown_nue_1d(dllee_nue_data,x_range=my_e_range,nbins=my_nbins,quantity_func=get_etrue)
  # ~ plt.savefig('dllee_nue_true.png')
  
  # Ereco-Etrue 2d
  plot_2d(pelee_nue_data,normalise=True,
    x_quantity_func=get_ereco, x_title=pelee_ereco_title,
    y_quantity_func=get_etrue, y_title=etrue_title)
  plt.savefig('pelee_nue_reco_vs_true.png')
  plot_2d(dllee_nue_data,normalise=True,
    x_quantity_func=get_ereco, x_title=dllee_ereco_title,
    y_quantity_func=get_etrue, y_title=etrue_title)
  plt.savefig('dllee_nue_reco_vs_true.png')
  
  print("Both, PeLEE Reco")
  plot_breakdown_nue_1d(both_pl_dl_with_pl_reco,x_range=my_e_range,nbins=my_nbins,quantity_func=get_ereco,x_title=pelee_ereco_title,print_stream=sys.stdout)
  plt.savefig('both_nue_pelee_reco.png')
  print("Both, DLLEE Reco")
  plot_breakdown_nue_1d(both_pl_dl_with_dl_reco,x_range=my_e_range,nbins=my_nbins,quantity_func=get_ereco,x_title=dllee_ereco_title)
  plt.savefig('both_nue_dllee_reco.png')
  
  plot_breakdown_nue_1d(both_pl_dl_with_pl_reco,x_range=my_e_range,nbins=my_nbins,quantity_func=get_elep,x_title=ereco_lepton_title)
  plt.savefig('both_nue_pelee_elep_reco.png')
  plot_breakdown_nue_1d(both_pl_dl_with_dl_reco,x_range=my_e_range,nbins=my_nbins,quantity_func=get_elep,x_title=ereco_lepton_title)
  plt.savefig('both_nue_dllee_elep_reco.png')
  
  plot_breakdown_nue_1d(both_pl_dl_with_pl_reco,x_range=my_theta_range,nbins=my_nbins_theta,quantity_func=get_thetalep,x_title=pelee_thetalep_title)
  plt.savefig('both_nue_pelee_thetalep_reco.png')
  plot_breakdown_nue_1d(both_pl_dl_with_dl_reco,x_range=my_theta_range,nbins=my_nbins_theta,quantity_func=get_thetalep,x_title=dllee_thetalep_title)
  plt.savefig('both_nue_dllee_thetalep_reco.png')
  
  in_pelee_but_not_dllee = pelee_nue_data.merge(pd.concat([pelee_nue_data[match_events_by],same_pelee_dllee_nue]).drop_duplicates(keep=False))
  print("In PELEE but not DLLEE")
  plot_breakdown_nue_1d(in_pelee_but_not_dllee,x_range=my_e_range,nbins=my_nbins,quantity_func=get_ereco,x_title=ereco_title)
  plt.savefig('pelee_nue_not_in_dllee_reco.png')
  plot_breakdown_nue_1d(in_pelee_but_not_dllee,x_range=my_e_range,nbins=my_nbins,quantity_func=get_etrue,x_title=etrue_title)
  plt.savefig('pelee_nue_not_in_dllee_true.png')
  
  in_dllee_but_not_pelee = dllee_nue_data.merge(pd.concat([dllee_nue_data[match_events_by],same_pelee_dllee_nue]).drop_duplicates(keep=False))
  print("In DLLEE but not PeLEE")
  plot_breakdown_nue_1d(in_dllee_but_not_pelee,x_range=my_e_range,nbins=my_nbins,quantity_func=get_ereco,x_title=ereco_title)
  plt.savefig('dllee_nue_not_in_pelee_reco.png')
  plot_breakdown_nue_1d(in_dllee_but_not_pelee,x_range=my_e_range,nbins=my_nbins,quantity_func=get_etrue,x_title=etrue_title)
  plt.savefig('dllee_nue_not_in_pelee_true.png')
  
  both_pl_dl_with_pl_reco["enu_reco_pelee"] = both_pl_dl_with_pl_reco["enu_reco"]
  both_pl_dl_with_pl_reco["enu_reco_dllee"] = both_pl_dl_with_dl_reco["enu_reco"]
  both_pl_dl_with_pl_reco["lepton_energy_reco_pelee"] = both_pl_dl_with_pl_reco["lepton_energy_reco"]
  both_pl_dl_with_pl_reco["lepton_energy_reco_dllee"] = both_pl_dl_with_dl_reco["lepton_energy_reco"]
  both_pl_dl_with_pl_reco["lepton_theta_reco_pelee"] = both_pl_dl_with_pl_reco["lepton_theta_reco"]
  both_pl_dl_with_pl_reco["lepton_theta_reco_dllee"] = both_pl_dl_with_dl_reco["lepton_theta_reco"]
  
  #debug
  both_pl_dl_with_dl_reco["enu_reco_pelee"] = both_pl_dl_with_pl_reco["enu_reco"]
  both_pl_dl_with_dl_reco["enu_reco_dllee"] = both_pl_dl_with_dl_reco["enu_reco"]
  
  print("Both, Diff Reco")
  plot_breakdown_nue_1d(both_pl_dl_with_dl_reco,x_range=[-400,400],
    quantity_func=lambda s: s.enu_reco_pelee-s.enu_reco_dllee,
    x_title="PeLEE-DLLEE Reco Neutrino Energy [MeV]",
    nbins=40)
  plt.savefig('both_nue_subtracted_ereco.png')
  
  plot_breakdown_nue_1d(both_pl_dl_with_pl_reco,x_range=[-400.,400],
    quantity_func=lambda s: s.lepton_energy_reco_pelee-s.lepton_energy_reco_dllee,
    x_title="PeLEE-DLLEE Reco Electron Energy [MeV]",
    nbins=40)
  plt.savefig('both_nue_subtracted_elep.png')
  
  plot_breakdown_nue_1d(both_pl_dl_with_pl_reco,x_range=[-60.,60],
    quantity_func=lambda s: s.lepton_theta_reco_pelee-s.lepton_theta_reco_dllee,
    x_title="PeLEE-DLLEE Reco Electron Theta [deg]",
    nbins=48)
  plt.savefig('both_nue_subtracted_thetalep.png')
  
  # 2D, comparing analysis Ereco
  plot_2d(both_pl_dl_with_pl_reco,normalise=True,
    x_quantity_func=lambda s: s.enu_reco_pelee, x_title=pelee_ereco_title,
    y_quantity_func=lambda s: s.enu_reco_dllee, y_title=dllee_ereco_title)
  plt.savefig('both_nue_reco_comp.png')
  
  # Ereco-Etrue 2d
  plot_2d(both_pl_dl_with_pl_reco,normalise=True,
    x_quantity_func=lambda s: s.enu_reco_pelee, x_title=pelee_ereco_title,
    y_quantity_func=get_etrue, y_title=etrue_title)
  plt.savefig('both_nue_pelee_reco_vs_true.png')
  plot_2d(both_pl_dl_with_pl_reco,normalise=True,
    x_quantity_func=lambda s: s.enu_reco_dllee, x_title=dllee_ereco_title,
    y_quantity_func=get_etrue, y_title=etrue_title)
  plt.savefig('both_nue_dllee_reco_vs_true.png')
  
  # Ereco-Etrue 2d
  plot_2d(both_pl_dl_with_pl_reco,normalise=True,
    x_quantity_func=get_etrue, x_title=etrue_title,
    y_quantity_func=lambda s: s.enu_reco_pelee-s.enu_reco_dllee, y_title="PeLEE-DLLEE Reco Neutrino Energy [MeV]", y_range=[-200,200])
  plt.savefig('both_nue_reco_diff_vs_true.png')
  
  plot_breakdown_nue_1d(pelee_nue_data,x_range=[-400,400],nbins=80,quantity_func=lambda s: s.enu_reco-s.enu_true,x_title="PeLEE Ereco - Etrue [MeV]")
  plt.savefig('pelee_reco_minus_true.png')
  plot_breakdown_nue_1d(dllee_nue_data,x_range=[-400,400],nbins=80,quantity_func=lambda s: s.enu_reco-s.enu_true,x_title="DLLEE Ereco - Etrue [MeV]")
  plt.savefig('dllee_reco_minus_true.png')
    
if __name__ == "__main__":
  main()
