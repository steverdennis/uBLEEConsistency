#!/usr/bin/env python
import ROOT as R
import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

import uBLEEConsistency.datasets.DLLEE_numu_tree as dllee_set
import uBLEEConsistency.datasets.PeLEE_numu_v08_00_00_48_0928 as pelee_set

colors = ['tab:blue', 'tab:orange', 'tab:green', 'tab:red', 'tab:purple', 'tab:brown', 'tab:pink', 'tab:gray']

plt.rc('xtick',labelsize=22)
plt.rc('ytick',labelsize=22)
params = {'axes.labelsize': 22,'axes.titlesize':22, 'legend.fontsize': 20, 'xtick.labelsize': 22, 'ytick.labelsize': 22}#text.fontsize
matplotlib.rcParams.update(params)
  
to2dp = '{0:.2f}'

def main():

  pelee_numu_data = pelee_set.get_datasets()
  dllee_numu_data = dllee_set.get_datasets()
  
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
  
  # ~ print("PeLEE")
  # ~ plot_breakdown_numu(pelee_numu_data,e_range=[150,1550])
  # ~ plt.savefig('pelee_numu.png')
  # ~ print("DLLEE")
  # ~ plot_breakdown_numu(dllee_numu_data,e_range=[150,1550])
  # ~ plt.savefig('dllee_numu.png')
  # ~ print("Both, PeLEE Reco")
  # ~ plot_breakdown_numu(both_pelee_reco,e_range=[150,1550])
  # ~ plt.savefig('both_numu_pelee_reco.png')
  # ~ print("Both, DLLEE Reco")
  # ~ plot_breakdown_numu(both_dllee_reco,e_range=[150,1550])
  # ~ plt.savefig('both_numu_dlee_reco.png')
  
  plot_breakdown_numu(both_pelee_reco,e_range=[-1000,1000])
  plt.savefig('both_numu_subtracted_reco.png')
  print("Both, Diff Reco")
  
  # ~ in_pelee_but_not_dllee = pelee_numu_data.merge(pd.concat([pelee_numu_data[match_events_by],same_pelee_dllee_numu]).drop_duplicates(keep=False))
  # ~ print("In PLLEE but not DLEE")
  # ~ plot_breakdown_numu(in_pllee_but_not_pelee,e_range=[150,1550])
  # ~ plt.savefig('pelee_numu_not_in_dllee.png')
  # ~ in_dllee_but_not_pelee = dllee_numu_data.merge(pd.concat([dllee_numu_data[match_events_by],same_pelee_dllee_numu]).drop_duplicates(keep=False))
  # ~ print("In DLLEE but not PeLEE")
  # ~ plot_breakdown_numu(in_dllee_but_not_pelee,e_range=[150,1550])
  # ~ plt.savefig('dllee_numu_not_in_pelee.png')

def plot_breakdown_numu(df,e_range,normalise=False):
  hknumuCCQE     = df[(df['IsNC']==0) & ((df['nu_pdg_final']== 14) | (df['nu_pdg_final']== -14))  & (df['nu_interaction_mode'] == 0)]#pdg == +-14 means muon and +-12 is electron
  hknumuRes      = df[(df['IsNC']==0) & ((df['nu_pdg_final']== 14) | (df['nu_pdg_final']== -14))  & (df['nu_interaction_mode'] == 1)]#IsNC=0 means CC and 1 is NC
  hknumuMEC      = df[(df['IsNC']==0) & ((df['nu_pdg_final']== 14) | (df['nu_pdg_final']== -14))  & (df['nu_interaction_mode'] == 10)]#interaction mode==0 is CCQE, 1 is Res, 10 is MEC
  hknumuCCOther  = df[(df['IsNC']==0) & ((df['nu_pdg_final']== 14) | (df['nu_pdg_final']== -14))  & (df['nu_interaction_mode'] != 0) & (df['nu_interaction_mode'] != 1) & (df['nu_interaction_mode'] != 10)]
  hknuEInclusive = df[(df['IsNC']==0) & ((df['nu_pdg_final']== 12) | (df['nu_pdg_final']== -12))]
  hkNCInclusive  = df[(df['IsNC']==1)]
  
  all_stacks = [hknumuCCQE,hknumuMEC,hknumuRes,hknumuCCOther,hknuEInclusive,hkNCInclusive]
  stack_labels = [r"BNB $\nu_{\mu}$ CCQE",r"BNB $\nu_{\mu}$ CCMEC",r"BNB $\nu_{\mu}$ CCRes",r"BNB $\nu_{\mu}$ CCOther",r"$\nu_{e}$ Inclusive","NC Inclusive"]
  total = sum([s.event_weight.sum() for s in all_stacks])
  
  print("CCQE:" ,hknumuCCQE    .event_weight.sum(),"\t",to2dp.format(100*hknumuCCQE    .event_weight.sum()/total))
  print("CCMEC:",hknumuMEC     .event_weight.sum(),"\t",to2dp.format(100*hknumuMEC     .event_weight.sum()/total))
  print("CCRES:",hknumuRes     .event_weight.sum(),"\t",to2dp.format(100*hknumuRes     .event_weight.sum()/total))
  print("CCoth:",hknumuCCOther .event_weight.sum(),"\t",to2dp.format(100*hknumuCCOther .event_weight.sum()/total))
  print("nuECC:",hknuEInclusive.event_weight.sum(),"\t",to2dp.format(100*hknuEInclusive.event_weight.sum()/total))
  print("NC:"   ,hkNCInclusive .event_weight.sum(),"\t",to2dp.format(100*hkNCInclusive .event_weight.sum()/total))
  
  norm_weight = 1.
  if normalise: norm_weight = 1/total
  
  x = [s.enu_reco-s.enu_reco_dllee for s in all_stacks]
  y = [s.event_weight * norm_weight for s in all_stacks]
  
  plt.figure(figsize=(15,10))
  plt.xlabel('Neutrino reconstructed energy [MeV]', fontsize=22)
  
  n, bins, patches = plt.hist(x, 40,range=e_range,histtype='bar',
    stacked=True, weights=y,
    color=colors[:len(x)],
    label=stack_labels)

  hatches = [' ',' ',' ',' ',' ',' ',' ',' ']
  for patch_set, hatch in zip(patches, hatches):
      for patch in patch_set.patches:
          patch.set_hatch(hatch)
          
  ##################
  ##Legend entries##
  ##################
  
  label_patches = [matplotlib.patches.Patch(color=colors[i],label=stack_labels[i]) for i,p in enumerate(patches)]
  
  plt.legend(label_patches,stack_labels,fontsize=20)

  plt.xlabel('Neutrino reconstructed energy [MeV]', fontsize=22)
  
  plt.rc('xtick',labelsize=22)
  plt.rc('ytick',labelsize=22)
  params = {'axes.labelsize': 22,'axes.titlesize':22, 'legend.fontsize': 20, 'xtick.labelsize': 22, 'ytick.labelsize': 22}#text.fontsize
  matplotlib.rcParams.update(params)
  #plt.savefig('ereco_numu.png')
  # ~ plt.show()

if __name__ == "__main__":
  main()
