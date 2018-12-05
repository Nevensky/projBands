#!/usr/bin/env python3
import xmltodict
import numpy as np
import io

xmlfile = "atomic_proj.xml"
with open(xmlfile) as fl:
    atomic_proj = xmltodict.parse(fl.read())["ATOMIC_PROJECTIONS"]


nbands = int(atomic_proj["HEADER"]["NUMBER_OF_BANDS"]["#text"])
nkpoints = int(atomic_proj["HEADER"]["NUMBER_OF_K-POINTS"]["#text"])
nwfcs = int(atomic_proj["HEADER"]["NUMBER_OF_ATOMIC_WFC"]["#text"])
nelectrons = float(atomic_proj["HEADER"]["NUMBER_OF_ELECTRONS"]["#text"])

units_kpoints = atomic_proj["HEADER"]["UNITS_FOR_K-POINTS"]["@UNITS"]
units_energy = atomic_proj["HEADER"]["UNITS_FOR_ENERGY"]["@UNITS"]

fermi_en = float(atomic_proj["HEADER"]["FERMI_ENERGY"]["#text"])


print("Number of bands:",nbands)
print("Number of k-points:",nkpoints)
print("Number of atomic wavefunctions:",nwfcs)

kpoints = np.asarray(atomic_proj["K-POINTS"]["#text"])
# print(kpoints)

kweights = np.asarray(atomic_proj["WEIGHT_OF_K-POINTS"]["#text"])
# print(kweights)


eigenvals = np.zeros((nkpoints,nbands))
for kp, eigval in atomic_proj["EIGENVALUES"].items():
	kp_i = int(kp.split(".")[-1])
	eigval_np = np.asarray(eigval["EIG"]["#text"].split("\n"),dtype="float64")
	eigenvals[kp_i-1,:] = eigval_np
# print(eigenvals)
# print(eigenvals.shape)
# np.savetxt("eigenvalues.dat",eigenvals)

wavefcs = np.zeros((nkpoints,nwfcs,nbands,2),dtype="float64")	
for kp, wfcs in atomic_proj["PROJECTIONS"].items():
	kp_i = int(kp.split(".")[-1])
	print("k-point: ",kp_i)
	for wfci, wfc in wfcs.items():
		wfc_i = int(wfci.split(".")[-1])
		# print(wfc_i)
		wfc_np = np.genfromtxt(io.StringIO(wfc["#text"]),delimiter=",",dtype="float64")
		wavefcs[kp_i-1,wfc_i-1,:] = wfc_np
# print(wavefcs)
# np.savetxt("projected_wavefunctions.dat",wavefcs)		 NE RADI

print(eigenvals[0,0],wavefcs[0,0,:])

