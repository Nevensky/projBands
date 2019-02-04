#/usr/bin/env python3
import os
import numpy as np
import matplotlib.pyplot as plt
plt.style.use("seaborn-muted")

def main():
	""" Initalize BandPlot() objects. """
	#graphene
	BandPlot("/Users/Nevensky/Desktop/vito/graphene/bandsplot.dat.gnu",-2.3190)
	#CsC8
	BandPlot("/Users/Nevensky/Desktop/vito/CsC8/bandsplot.dat.gnu",-0.6767)
	#CsC8_Ir111
	BandPlot("/Users/Nevensky/Desktop/vito/CsC8_Ir111/bandsplot.dat.gnu",5.6936)

class BandPlot():
	def __init__(self,fname,fermi_en,e_min=-5,e_max=5):
		self.fname = fname
		self.fermi_en = fermi_en
		self.e_min = e_min
		self.e_max = e_max
		self.writeBands()
		self.readBands()
		self.printDim()
		self.reshapeBands()
		self.plotBands(save=True)

	def writeBands(self):
		"""Create dirrectory for storing separated bands."""
		self.bands_out = os.path.dirname(self.fname)+"/bands"
		if not os.path.exists(self.bands_out):
			os.mkdir(self.bands_out)

	def readBands(self):
		"""Imports all bands bands from GNU file
		(output: plotband.x) into a single array.
		Extracts the number of kpoints and bands."""
		self.bands = np.loadtxt(self.fname)
		self.nkpoints = np.unique(self.bands[:,0]).shape[0]
		self.nbands = int(self.bands.shape[0]/self.nkpoints)
		return self.bands

	def printDim(self):
		print(40*"_")
		print("File: {}".format(self.fname))
		print("Number of k-points: {}".format(self.nkpoints))
		print("Number of bands: {}".format(self.nbands))

	def reshapeBands(self):
		""" Reshapes bands into a more readable format for plotting."""
		start_idx = 0
		end_idx = self.nkpoints
		self.bandsClean = np.zeros([self.nbands,self.nkpoints,2])
		for band_i in range(0,self.nbands):
			data = self.bands[start_idx:end_idx,:]
			data[:,1] -= self.fermi_en
			self.bandsClean[band_i,:,:] = data
			start_idx = end_idx
			end_idx += self.nkpoints
		return self.bandsClean

	def plotBands(self,save=True):
		"""Saves separated bands into a "bands" subdir.
		Plots all bands and creates a bandstructure pdf file."""
		for band_i in range(self.nbands):
			data = self.bandsClean[band_i,:,:]
			plt.plot(data[:,0],data[:,1])
			if save:
				np.savetxt(self.bands_out+"/band_{}.dat".format(band_i),data)
		plt.hlines(0,np.min(data[:,0]),np.max(data[:,0]),'k','-.')
		plt.ylim(self.e_min,self.e_max)
		plt.ylabel(r"$E-E_\mathrm{F} \ \mathrm{\left[eV\right]}$")
		plt.xlabel(r"$\mathrm{k-path}$")
		plt.title(self.fname)
		if save:
			plt.savefig(self.fname+".pdf")
		else:
			plt.show()

if __name__ == '__main__':
 	main()




