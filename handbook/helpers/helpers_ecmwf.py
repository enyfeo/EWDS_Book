# (C) Copyright 1996- ECMWF.
#
# This software is licensed under the terms of the Apache Licence Version 2.0
# which can be obtained at http://www.apache.org/licenses/LICENSE-2.0.
# In applying this licence, ECMWF does not waive the privileges and immunities
# granted to it by virtue of its status as an intergovernmental organisation
# nor does it submit to any jurisdiction.

import eccodes as ec
import numpy as np
import pandas as pd
import netCDF4 as nc4
import os
import datetime as datetime

def load_grb_file(FNAME,retKeys=None,verbose=False):
  """
  Loads full grib file
  xdata,xKeys=load_for_file(FNAME,retKeys=None,verbose=False)
  input:
   FNAME: file name (including full path) to read from
   retKeys: list with extra keys to return (default: None)
   verbose: if true print some details
  returns
   xdata : np.array: (nflds,npoints)
   xKeys : if retKeys is not None: dictionary with a list for each key requested
  """

  if verbose:
    print('Reading:',FNAME)
  # open file
  fgrb = open(FNAME)
  # find # of fields in file
  nflds = ec.codes_count_in_file(fgrb)
  if verbose:
    print('Found ', nflds,' fields in,',FNAME)

  # create dictionary with empty lists for each requested key
  xKeys={}
  if retKeys is not None:
    for key in retKeys:
      xKeys[key]=[]

  # load fields
  for ikfld in range(nflds):
    gid = ec.codes_grib_new_from_file(fgrb)
    xtmp = ec.codes_get_values(gid)
    if ec.codes_get(gid,'bitmapPresent') == 1:
      zmiss=ec.codes_get(gid,'missingValue')
      xtmp[xtmp==zmiss]=np.nan
    if ikfld == 0  :
      xdata = np.zeros((nflds,xtmp.shape[0]),dtype=np.float32)
    xdata[ikfld,:] = xtmp
    if retKeys is not None:
      for key in retKeys:
        xKeys[key].append(ec.codes_get(gid,key))

    ec.codes_release(gid)

  fgrb.close()
  if retKeys is not None:
    for kk in xKeys.keys():
      xKeys[kk] = np.array(xKeys[kk])
    return xdata,xKeys
  else:
    return xdata


