from dataclasses import dataclass

int_default   = -1
float_default = -999.

@dataclass
class NuEvent:
  run:    int = int_default
  subrun: int = int_default
  event:  int = int_default

  selection:int = int_default
    
  nu_pdg_init:int = int_default#same with nu_pdg_final
  nu_pdg_final:int = int_default
  #nu_interaction_ccnc:int = int_default#IsNC?
  IsNC: int = int_default
  nu_interaction_mode:int = int_default

  enu_true:float = float_default # both in MeV
  enu_reco:float = float_default # both in MeV
  
  event_weight:float = float_default     
  lepton_theta_reco:float = float_default
  lepton_energy_reco:float = float_default
  proton_theta_reco:float = float_default
  proton_energy_reco:float = float_default
  
  reco_nuvtx_x:float = float_default
  reco_nuvtx_y:float = float_default
  reco_nuvtx_z:float = float_default
  
  # WC
  numu_cc_flag:int = int_default
  nue_cc_flag:int = int_default
  match_isFC:int = int_default
  
  numu_score:float = float_default
  nue_score:float = float_default
