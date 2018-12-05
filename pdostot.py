#/usr/bin/env python3
import numpy as np
import matplotlib.pyplot as plt
plt.style.use("ggplot")

file = "CsC8_Ir111_9x9x1.pdos_tot"

data = np.genfromtxt(file,skip_header=1)
dos=data[:,[0,1]]
pdos = data[:,[0,2]]
# print(dos)
# print(pdos)


plt.plot(dos[:,1],dos[:,0])
plt.plot(pdos[:,1],pdos[:,0])
plt.xlabel("Density of States")
plt.ylabel(r"$E$ [ eV ]")
plt.hlines(0,0,30,colors="turquoise",linestyles="dashed",label="Fermi level")
plt.legend(["DOS","PDOS","Fermi level"])
plt.show()