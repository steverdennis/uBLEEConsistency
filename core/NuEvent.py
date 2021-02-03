from dataclasses import dataclass

int_default   = -1
float_default = -999.

@dataclass
class NuEvent:
  run:    int = int_default
  subrun: int = int_default
  
  enu_true: float = float_default
