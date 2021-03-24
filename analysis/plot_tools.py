#!/usr/bin/env python
import sys
import ROOT as R
import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
  
to2dp = '{0:.2f}'

null_stream = open("/dev/null","w")
def_stream = null_stream
# ~ def_stream = sys.stdout

default_colors = ['tab:blue', 'tab:orange', 'tab:green', 'tab:red', 'tab:purple', 'tab:brown', 'tab:pink', 'tab:gray']

def get_ereco(s):
  return s.enu_reco
  
def get_etrue(s):
  return s.enu_true

def plot_breakdown_nue_1d(df,x_range,normalise=False,
  quantity_func=get_ereco, nbins=16,
  x_title="",
  colors=default_colors,
  print_stream=def_stream):
    
  hknueCCQE     = df[(df['IsNC']==0) & ((df['nu_pdg_final']== 12) | (df['nu_pdg_final']== -12))  & (df['nu_interaction_mode'] == 0)]#pdg == +-12 means muon and +-12 is electron
  hknueRes      = df[(df['IsNC']==0) & ((df['nu_pdg_final']== 12) | (df['nu_pdg_final']== -12))  & (df['nu_interaction_mode'] == 1)]#IsNC=0 means CC and 1 is NC
  hknueMEC      = df[(df['IsNC']==0) & ((df['nu_pdg_final']== 12) | (df['nu_pdg_final']== -12))  & (df['nu_interaction_mode'] == 10)]#interaction mode==0 is CCQE, 1 is Res, 10 is MEC
  hknueCCOther  = df[(df['IsNC']==0) & ((df['nu_pdg_final']== 12) | (df['nu_pdg_final']== -12))  & (df['nu_interaction_mode'] != 0) & (df['nu_interaction_mode'] != 1) & (df['nu_interaction_mode'] != 10)]
  hknuMuInclusive = df[(df['IsNC']==0) & ((df['nu_pdg_final']== 14) | (df['nu_pdg_final']== -14))]
  hkNCInclusive  = df[(df['IsNC']==1)]
  
  all_stacks = [hknueCCQE,hknueMEC,hknueRes,hknueCCOther,hknuMuInclusive,hkNCInclusive]
  stack_labels = [r"BNB $\nu_{e}$ CCQE",r"BNB $\nu_{e}$ CCMEC",r"BNB $\nu_{e}$ CCRes",r"BNB $\nu_{e}$ CCOther",r"$\nu_{e}$ Inclusive","NC Inclusive"]
  total = sum([s.event_weight.sum() for s in all_stacks])
  
  print("CCQE:" ,hknueCCQE      .event_weight.sum(),"\t",to2dp.format(100*hknueCCQE      .event_weight.sum()/total),file=print_stream)
  print("CCMEC:",hknueMEC       .event_weight.sum(),"\t",to2dp.format(100*hknueMEC       .event_weight.sum()/total),file=print_stream)
  print("CCRES:",hknueRes       .event_weight.sum(),"\t",to2dp.format(100*hknueRes       .event_weight.sum()/total),file=print_stream)
  print("CCoth:",hknueCCOther   .event_weight.sum(),"\t",to2dp.format(100*hknueCCOther   .event_weight.sum()/total),file=print_stream)
  print("nuECC:",hknuMuInclusive.event_weight.sum(),"\t",to2dp.format(100*hknuMuInclusive.event_weight.sum()/total),file=print_stream)
  print("NC:"   ,hkNCInclusive  .event_weight.sum(),"\t",to2dp.format(100*hkNCInclusive  .event_weight.sum()/total),file=print_stream)
  print("Total:",total,"\n",file=print_stream)
  
  norm_weight = 1.
  if normalise: norm_weight = 1/total
  
  x = [quantity_func(s) for s in all_stacks]
  y = [s.event_weight * norm_weight for s in all_stacks]
  
  
  plt.figure(figsize=(15,10))
  
  n, edges, patches = plt.hist(x, nbins,range=x_range,histtype='bar',
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

  plt.xlabel(x_title, fontsize=22)
  
  plt.rc('xtick',labelsize=22)
  plt.rc('ytick',labelsize=22)
  params = {'axes.labelsize': 22,'axes.titlesize':22, 'legend.fontsize': 20, 'xtick.labelsize': 22, 'ytick.labelsize': 22}#text.fontsize
  matplotlib.rcParams.update(params)
  return
  
def plot_breakdown_numu_1d(df,x_range,normalise=False,
    quantity_func=get_ereco, nbins=16,
    x_title="",
    colors=default_colors,
    print_stream=def_stream):
      
  hknumuCCQE     = df[(df['IsNC']==0) & ((df['nu_pdg_final']== 14) | (df['nu_pdg_final']== -14))  & (df['nu_interaction_mode'] == 0)]#pdg == +-14 means muon and +-12 is electron
  hknumuRes      = df[(df['IsNC']==0) & ((df['nu_pdg_final']== 14) | (df['nu_pdg_final']== -14))  & (df['nu_interaction_mode'] == 1)]#IsNC=0 means CC and 1 is NC
  hknumuMEC      = df[(df['IsNC']==0) & ((df['nu_pdg_final']== 14) | (df['nu_pdg_final']== -14))  & (df['nu_interaction_mode'] == 10)]#interaction mode==0 is CCQE, 1 is Res, 10 is MEC
  hknumuCCOther  = df[(df['IsNC']==0) & ((df['nu_pdg_final']== 14) | (df['nu_pdg_final']== -14))  & (df['nu_interaction_mode'] != 0) & (df['nu_interaction_mode'] != 1) & (df['nu_interaction_mode'] != 10)]
  hknuEInclusive = df[(df['IsNC']==0) & ((df['nu_pdg_final']== 12) | (df['nu_pdg_final']== -12))]
  hkNCInclusive  = df[(df['IsNC']==1)]
  
  all_stacks = [hknumuCCQE,hknumuMEC,hknumuRes,hknumuCCOther,hknuEInclusive,hkNCInclusive]
  stack_labels = [r"BNB $\nu_{\mu}$ CCQE",r"BNB $\nu_{\mu}$ CCMEC",r"BNB $\nu_{\mu}$ CCRes",r"BNB $\nu_{\mu}$ CCOther",r"$\nu_{e}$ Inclusive","NC Inclusive"]
  total = sum([s.event_weight.sum() for s in all_stacks])
  
  print("CCQE:" ,hknumuCCQE    .event_weight.sum(),"\t",to2dp.format(100*hknumuCCQE    .event_weight.sum()/total),file=print_stream)
  print("CCMEC:",hknumuMEC     .event_weight.sum(),"\t",to2dp.format(100*hknumuMEC     .event_weight.sum()/total),file=print_stream)
  print("CCRES:",hknumuRes     .event_weight.sum(),"\t",to2dp.format(100*hknumuRes     .event_weight.sum()/total),file=print_stream)
  print("CCoth:",hknumuCCOther .event_weight.sum(),"\t",to2dp.format(100*hknumuCCOther .event_weight.sum()/total),file=print_stream)
  print("nuECC:",hknuEInclusive.event_weight.sum(),"\t",to2dp.format(100*hknuEInclusive.event_weight.sum()/total),file=print_stream)
  print("NC:"   ,hkNCInclusive .event_weight.sum(),"\t",to2dp.format(100*hkNCInclusive .event_weight.sum()/total),file=print_stream)
  
  norm_weight = 1.
  if normalise: norm_weight = 1/total
  
  x = [quantity_func(s) for s in all_stacks]
  y = [s.event_weight * norm_weight for s in all_stacks]
  
  plt.figure(figsize=(15,10))

  n, edges, patches = plt.hist(x, nbins,range=x_range,histtype='bar',
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
  return

def plot_2d(df,normalise=False,
    x_quantity_func=get_ereco,
    y_quantity_func=get_etrue,
    x_nbins=32,
    y_nbins=32,
    x_range=(0,1600),
    y_range=(0,1600),
    x_title="",
    y_title="",
    print_stream=def_stream):
  
  # Do we normalise
  norm_weight = 1.
  if normalise: norm_weight = 1./sum(df.event_weight)
  
  # Make the series
  x = x_quantity_func(df)
  y = y_quantity_func(df)
  z = df.event_weight * norm_weight
  
  plt.figure(figsize=(15,10))

  plt.hist2d(x, y, weights=z, bins=(x_nbins,y_nbins),range=(x_range,y_range), cmap='Blues')
  
  cb = plt.colorbar()
  
  plt.xlabel(x_title, fontsize=22)
  plt.ylabel(y_title, fontsize=22)
  
  plt.rc('xtick',labelsize=22)
  plt.rc('ytick',labelsize=22)
  
  return
    
if __name__ == "__main__":
  main()
