from dataclasses import dataclass

@dataclass
class NuEvent:
  run: int = -1
  subrun: int = -1
  
  enu_true: float = -999.
