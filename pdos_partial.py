#/usr/bin/env python3
import numpy as np
import matplotlib.pyplot as plt
import glob
plt.style.use("ggplot")


files = glob.glob("/Users/nevensky/Desktop/vito/CsC8/*pdos_atm*")
# print(files)

fig, axs = plt.subplots(1, 3)


axname={"C":0,"Cs":1,"Ir":2}
legend = {"C":[],"Cs":[],"Ir":[]}
pdos = {"C":[],"Cs":[],"Ir":[]}
maxpdos = {"C":0,"Cs":0,"Ir":0}

for fl in files:
	info = fl.split("_")
	atom = info[-2].replace(")","(").split("(")[1]
	atomNo = info[-2].replace(")","(").split("(")[0]	
	wfc = info[-1]
	orbital = wfc.split("#")[-1]
	print(atom,orbital)	

	data = np.genfromtxt(fl,skip_header=1)
	pdos = data[:,[0,1]]
	if np.max(pdos[:,1])>maxpdos[atom]:
		maxpdos[atom] = np.max(pdos[:,1])
	
	legend[atom].append(orbital)
	print(axname[atom])
	axs[axname[atom]].plot(pdos[:,1],pdos[:,0])

for atom in list(axname):
	axs[axname[atom]].set_xlabel("Projected Density of States")
	axs[axname[atom]].set_ylabel(r"$E$ [ eV ]")
	axs[axname[atom]].hlines(0,0,maxpdos[atom],linestyles="dashed",label="Fermi level")
	axs[axname[atom]].legend(legend[atom])
	axs[axname[atom]].set_title(atom)
#legend.append("Fermi level")

# fig.tight_layout()
plt.show()