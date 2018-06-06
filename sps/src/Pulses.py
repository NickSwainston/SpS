import numpy as np
import pandas as pd

import RFIexcision
from Parameters import *


def Loader(events,args):
  """
  Create a table with the pulses
  """
    
  gb = events.groupby('Pulse',sort=False)
  pulses = events.loc[gb.Sigma.idxmax()]  
  pulses.index = pulses.Pulse
  pulses.index.name = None
  pulses = pulses.loc[:,['SAP','BEAM','DM','Sigma','Time','Duration','Sample','Time_org','Downfact']]
  pulses.index.name = 'idx'
  pulses['Rank'] = 0
  pulses.Rank = pulses.Rank.astype(np.int8)
  pulses['Candidate'] = -1
  pulses.Candidate = pulses.Candidate.astype(np.int32)
  pulses['N_events'] = gb.DM.count()
  pulses.N_events = pulses.N_events.astype(np.int16)

  pulses = pulses[pulses.N_events >= args.N_min]

  # Apply filters to discriminate interesting pulses
  if not args.RFI_filter: classic_filters(events[events.Pulse.isin(pulses.index)], pulses, args)

  #Store the pulses
  pulses.sort(['DM','Time'], inplace=True)
  if not args.no_store: pulses.to_hdf(args.store_name, 'pulses')

  return pulses



def classic_filters(events, pulses, params):
  """
  Apply RFI filters to the pulses
  """

  RFI_code = 9
  events = events[events.Pulse.isin(pulses.index)]
  events.sort_values(by='DM',inplace=True)
  gb = events.groupby('Pulse')
  pulses.sort_index(inplace=True)

  #Remove flat SNR pulses
  pulses.Pulse[pulses.Sigma / gb.Sigma.min() <= args.SNR_peak_min / args.SNR_min] = RFI_code

  #Remove flat duration pulses (from Eq.6.21 of Pulsar Handbook)
  pulses.Pulse[gb.Downfact.max() / pulses.Downfact < (args.SNR_peak_min / args.SNR_min)**2] = RFI_code

  #Remove pulses peaking near the DM edges
  if args.DM_min is not None and args.DM_max is not None:
    DM_frac = (args.DM_high - args.DM_low) * 0.05  #Remove 5% of DM range from each edge
    pulses.Pulse[(pulses.DM < args.DM_low + DM_frac) | (pulses.DM > args.DM_high - DM_frac)] = RFI_code

  #Remove pulses intersecting half the maximum SNR other than 2,4,6,8 times
  def crosses(sig):
    diff = sig - (sig.max() + sig.min()) / 2.
    count = np.count_nonzero(np.diff(np.sign(diff)))
    return (count != 2) & (count != 4) & (count != 6) & (count != 8)
  pulses.Pulse[gb.apply(lambda x: crosses(x.Sigma))] = RFI_code

  #Remove weaker pulses within 20 ms of brighter ones
  def simultaneous(p):
    puls = pulses.Pulse[np.abs(pulses.Time-p.Time) < 0.02]
    if puls.shape[0] == 1: return False
    if p.name == puls.index[0]: return False
    else: return True
  pulses.Pulse[pulses.apply(lambda x: simultaneous(x), axis=1)] = RFI_code

  return



