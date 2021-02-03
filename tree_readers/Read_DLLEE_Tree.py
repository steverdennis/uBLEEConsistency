import ROOT as R
import pandas as pd

from uBLEEConsistency import NuEvent

default_files = []

def get_frame(files=default_files):
  
  tree = R.TChain("mytreename")
  for f in files: tree.AddFile(f)
  
  data_frame = pd.DataFrame()
  
  for event in tree:
    myevent = NuEvent()
    
    myevent.run = event.run
    
    data_frame.append(myevent)
    
  return data_frame
  
