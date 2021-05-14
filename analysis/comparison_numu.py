#!/usr/bin/env python
import sys

import ROOT as R
import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

import uBLEEConsistency.datasets.DLLEE_numu_CSV_run3 as dllee_set
# ~ import uBLEEConsistency.datasets.DLLEE_numu_tree_run3 as dllee_set
import uBLEEConsistency.datasets.PeLEE_numu_v08_00_00_48_0928 as pelee_set

from uBLEEConsistency.analysis.plot_tools import plot_breakdown_numu_1d,plot_1d,plot_2d

def get_ereco(s):
  return s.enu_reco
  
def get_etrue(s):
  return s.enu_true
  
def get_elep(s):
  return s.lepton_energy_reco
  
def get_thetalep(s):
  return s.lepton_theta_reco

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
  
  both_pl_dl_with_pl_reco = pelee_numu_data.merge(same_pelee_dllee_numu)
  both_pl_dl_with_dl_reco = dllee_numu_data.merge(same_pelee_dllee_numu)
  
  both_pl_dl_with_pl_reco["enu_reco_pelee"] = pelee_numu_data["enu_reco"]
  both_pl_dl_with_pl_reco["enu_reco_dllee"] = both_pl_dl_with_dl_reco["enu_reco"]

  # Copy over neutrino truth from PL to and WC, change this later.
  both_pl_dl_with_dl_reco["nu_interaction_mode"] = both_pl_dl_with_pl_reco["nu_interaction_mode"]
  both_pl_dl_with_dl_reco["nu_pdg_final"       ] = both_pl_dl_with_pl_reco["nu_pdg_final"]
  # ~ both_pl_wc_with_wc_reco["nu_interaction_mode"] = both_pl_dl_with_pl_reco["nu_interaction_mode"]
  # ~ both_pl_wc_with_wc_reco["nu_pdg_final"       ] = both_pl_dl_with_pl_reco["nu_pdg_final"]
  
  my_e_range = [-50,1550]
  my_nbins = 17
  my_theta_range = [0.,180.]
  my_nbins_theta = 36
  
  ereco_title        = 'Neutrino reconstructed energy [MeV]'
  pelee_ereco_title  = 'PeLEE Neutrino reconstructed energy [MeV]'
  dllee_ereco_title  = 'DLLEE Neutrino reconstructed energy [MeV]'
  wc_ereco_title     = 'Wire-Cell Neutrino reconstructed energy [MeV]'
  etrue_title        = 'Neutrino true energy [MeV]'
  ereco_lepton_title = 'Reco Muon energy [MeV]'
  theta_lepton_title = 'Reco Muon angle [deg]'
  ereco_proton_title = 'Reco Proton energy [MeV]'
  theta_proton_title = 'Reco Proton angle [deg]'
  pelee_thetalep_title  = 'PeLEE Muon angle [deg]'
  dllee_thetalep_title  = 'DLLEE Muon angle [deg]'

  print("PeLEE")
  plot_breakdown_numu_1d(pelee_numu_data,x_range=my_e_range,nbins=my_nbins,quantity_func=get_ereco,x_title=ereco_title,print_stream=sys.stdout)
  plt.savefig('pelee_numu_reco.png')
  plot_breakdown_numu_1d(pelee_numu_data,x_range=my_e_range,nbins=my_nbins,quantity_func=get_etrue,x_title=etrue_title)
  plt.savefig('pelee_numu_true.png')
  plot_breakdown_numu_1d(pelee_numu_data,x_range=my_e_range,nbins=my_nbins,quantity_func=get_elep,x_title=ereco_lepton_title)
  plt.savefig('pelee_numu_elep.png')
  plot_breakdown_numu_1d(pelee_numu_data,x_range=my_theta_range,nbins=my_nbins_theta,quantity_func=get_thetalep,x_title=theta_lepton_title)
  plt.savefig('pelee_numu_thetalep.png')
  
  print("DLLEE")
  plot_1d(dllee_numu_data,x_range=my_e_range,nbins=my_nbins,quantity_func=get_ereco,x_title=ereco_title,print_stream=sys.stdout)
  plt.savefig('dllee_numu_reco.png')
  plot_1d(dllee_numu_data,x_range=my_e_range,nbins=my_nbins,quantity_func=get_etrue,x_title=etrue_title)
  plt.savefig('dllee_numu_true.png')
  plot_1d(dllee_numu_data,x_range=my_e_range,nbins=my_nbins,quantity_func=get_elep,x_title=ereco_lepton_title)
  plt.savefig('dllee_numu_elep.png')
  plot_1d(dllee_numu_data,x_range=my_theta_range,nbins=my_nbins_theta,quantity_func=get_thetalep,x_title=theta_lepton_title)
  plt.savefig('dllee_numu_thetalep.png')
  
  # Ereco-Etrue 2d
  plot_2d(pelee_numu_data,normalise=True,
    x_quantity_func=get_ereco, x_title=pelee_ereco_title,
    y_quantity_func=get_etrue, y_title=etrue_title)
  plt.savefig('pelee_numu_reco_vs_true.png')
  plot_2d(dllee_numu_data,normalise=True,
    x_quantity_func=get_ereco, x_title=dllee_ereco_title,
    y_quantity_func=get_etrue, y_title=etrue_title)
  plt.savefig('dllee_numu_reco_vs_true.png')
  
  print("Both, PeLEE Reco")
  plot_breakdown_numu_1d(both_pl_dl_with_pl_reco,x_range=my_e_range,nbins=40,quantity_func=get_ereco,x_title=pelee_ereco_title,print_stream=sys.stdout)
  plt.savefig('both_numu_pelee_reco.png')
  print("Both, DLLEE Reco")
  plot_breakdown_numu_1d(both_pl_dl_with_dl_reco,x_range=my_e_range,nbins=40,quantity_func=get_ereco,x_title=dllee_ereco_title)
  plt.savefig('both_numu_dllee_reco.png')
  
  in_pelee_but_not_dllee = pelee_numu_data.merge(pd.concat([pelee_numu_data[match_events_by],same_pelee_dllee_numu]).drop_duplicates(keep=False))
  print("In PELEE but not DLLEE")
  plot_breakdown_numu_1d(in_pelee_but_not_dllee,x_range=my_e_range,nbins=my_nbins,quantity_func=get_ereco,x_title=ereco_title)
  plt.savefig('pelee_numu_not_in_dllee_reco.png')
  plot_breakdown_numu_1d(in_pelee_but_not_dllee,x_range=my_e_range,nbins=my_nbins,quantity_func=get_etrue,x_title=etrue_title)
  plt.savefig('pelee_numu_not_in_dllee_true.png')
  
  in_dllee_but_not_pelee = dllee_numu_data.merge(pd.concat([dllee_numu_data[match_events_by],same_pelee_dllee_numu]).drop_duplicates(keep=False))
  print("In DLLEE but not PeLEE")
  plot_breakdown_numu_1d(in_dllee_but_not_pelee,x_range=my_e_range,nbins=my_nbins,quantity_func=get_ereco,x_title=ereco_title)
  plt.savefig('dllee_numu_not_in_pelee_reco.png')
  plot_breakdown_numu_1d(in_dllee_but_not_pelee,x_range=my_e_range,nbins=my_nbins,quantity_func=get_etrue,x_title=etrue_title)
  plt.savefig('dllee_numu_not_in_pelee_true.png')
  
  both_pl_dl_with_pl_reco["enu_reco_pelee"] = both_pl_dl_with_pl_reco["enu_reco"]
  both_pl_dl_with_pl_reco["enu_reco_dllee"] = both_pl_dl_with_dl_reco["enu_reco"]
  both_pl_dl_with_pl_reco["lepton_energy_reco_pelee"] = both_pl_dl_with_pl_reco["lepton_energy_reco"]
  both_pl_dl_with_pl_reco["lepton_energy_reco_dllee"] = both_pl_dl_with_dl_reco["lepton_energy_reco"]
  both_pl_dl_with_pl_reco["lepton_theta_reco_pelee"] = both_pl_dl_with_pl_reco["lepton_theta_reco"]
  both_pl_dl_with_pl_reco["lepton_theta_reco_dllee"] = both_pl_dl_with_dl_reco["lepton_theta_reco"]
  
  print("Both, Diff Reco")
  plot_breakdown_numu_1d(both_pl_dl_with_pl_reco,x_range=[-400.,400.],
    quantity_func=lambda s: s.enu_reco_pelee-s.enu_reco_dllee,
    x_title="PeLEE-DLLEE Reco Neutrino Energy [MeV]",
    nbins=40)
  plt.savefig('both_numu_subtracted_ereco.png')

  plot_breakdown_numu_1d(both_pl_dl_with_pl_reco,x_range=[-400.,400.],
    quantity_func=lambda s: s.lepton_energy_reco_pelee-s.lepton_energy_reco_dllee,
    x_title="PeLEE-DLLEE Reco Muon Energy [MeV]",
    nbins=50)
  plt.savefig('both_numu_subtracted_elep.png')
  
  plot_breakdown_numu_1d(both_pl_dl_with_pl_reco,x_range=[-60.,60],
    quantity_func=lambda s: s.lepton_theta_reco_pelee-s.lepton_theta_reco_dllee,
    x_title="PeLEE-DLLEE Reco Muon Theta [deg]",
    nbins=48)
  plt.savefig('both_numu_subtracted_thetalep.png')
  
  # Don't care about 2D right now.
  return
  
  # 2D, comparing analysis Ereco
  plot_2d(both_pl_dl_with_pl_reco,normalise=True,
    x_quantity_func=lambda s: s.enu_reco_pelee, x_title=pelee_ereco_title,
    y_quantity_func=lambda s: s.enu_reco_dllee, y_title=dllee_ereco_title)
  plt.savefig('both_numu_reco_comp.png')
  
  # Ereco-Etrue 2d
  plot_2d(both_pl_dl_with_pl_reco,normalise=True,
    x_quantity_func=lambda s: s.enu_reco_pelee, x_title=pelee_ereco_title,
    y_quantity_func=get_etrue, y_title=etrue_title)
  plt.savefig('both_numu_pelee_reco_vs_true.png')
  plot_2d(both_pl_dl_with_pl_reco,normalise=True,
    x_quantity_func=lambda s: s.enu_reco_dllee, x_title=dllee_ereco_title,
    y_quantity_func=get_etrue, y_title=etrue_title)
  plt.savefig('both_numu_dllee_reco_vs_true.png')
  
  # Ereco-Etrue 2d
  plot_breakdown_numu_1d(pelee_numu_data,x_range=[-400,400],nbins=80,quantity_func=lambda s: s.enu_reco-s.enu_true,x_title="PeLEE Ereco - Etrue [MeV]")
  plt.savefig('pelee_reco_minus_true.png')
  plot_breakdown_numu_1d(dllee_numu_data,x_range=[-400,400],nbins=80,quantity_func=lambda s: s.enu_reco-s.enu_true,x_title="DLLEE Ereco - Etrue [MeV]")
  plt.savefig('dllee_reco_minus_true.png')
  
  plot_breakdown_numu_1d(both_pl_dl_with_pl_reco,x_range=[-400,400],nbins=80,quantity_func=lambda s: s.enu_reco-s.enu_true,x_title="DLLEE Peeco - Etrue [MeV]")
  plt.savefig('both_pl_dl_with_pl_reco_minus_true.png')
  plot_breakdown_numu_1d(both_pl_dl_with_dl_reco,x_range=[-400,400],nbins=80,quantity_func=lambda s: s.enu_reco-s.enu_true,x_title="DLLEE Ereco - Etrue [MeV]")
  plt.savefig('both_pl_dl_with_dl_reco_minus_true.png')
  

if __name__ == "__main__":
  main()
