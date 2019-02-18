#!/usr/bin/env python3
import numpy as np
import sys
import matplotlib.pyplot as plt
# plt.style.use("ggplot")

"""Orbital Order
 Order of m-components for each l in the output:
    1, cos(phi), sin(phi), cos(2*phi), sin(2*phi), .., cos(l*phi), sin(l*phi)
where phi is the polar angle:
x=r cos(theta)cos(phi),
y=r cos(theta)sin(phi)
This is determined in file Modules/ylmr2.f90
that calculates spherical harmonics.
for l=0:
  1 s     (m=0)
for l=1:
  1 pz     (m=0)
  2 px     (real combination of m=+/-1 with cosine)
  3 py     (real combination of m=+/-1 with sine)
for l=2:
  1 dz2    (m=0)
  2 dzx    (real combination of m=+/-1 with cosine)
  3 dzy    (real combination of m=+/-1 with sine)
  4 dx2-y2 (real combination of m=+/-2 with cosine)
  5 dxy    (real combination of m=+/-2 with sine)
"""

"""
Bond type
= sigma bonds =
for l=0 & l=0:
  1 s-s
for l=0 & l=1:
  1 s-pz
for l=1 & l=1:
  1 pz-pz
for l=1 & l=2:
  1 pz-dz^2
for l=2 & l=2:
  1 dz^2-dz^2
  2 d(x^2-y^2) - d(x^2-y^2)

for hybrids:
  1 s-sp
  2 s-sp2
  3 s-sp3
  4 sp-sp
  5 sp-sp2
  6 sp-sp3
  7 sp2-sp2
  8 sp2-sp3
  9 sp3-sp3"""

state_weight_cutoff = .02 # 2%

orbital_type = {
  (0,1):"s",
  (1,1):"pz",
  (1,2):"px",
  (1,3):"py",
  (2,1):"dz2",
  (2,2):"dzx",
  (2,3):"dzy",
  (2,4):"dx2-y2",
  (2,5):"dxy"
  }


# file = sys.argv[1]
# file = "/Users/nevensky/Desktop/vito/graphene/gr.proj.out"
# file = "/Users/nevensky/Desktop/vito/CsC8/CsC8.proj.out"
# file = "/Users/nevensky/Desktop/vito/CsC8_Ir111/IrCsC8.proj.out"
file = "/Users/nevensky/Desktop/vito/LiC6/LiC6.proj.out"

e_min = -4
e_max = 4

nkpoints = 150
ncontribs = 4 # sigma, pi, d, other

# graphene
# highsymm = [0.0000, 0.6778, 1.0167, 1.6038]
# fermi_en = -2.3190
# nbands = 15
# nwfcs = 8

#CsC8
# highsymm = [0.0000, 0.6667, 1.0000, 1.5773]
# fermi_en = -0.6767
# nbands = 100
# nwfcs = 45

#CsC8 / Ir(111)
# highsymm = [0.0000, 0.5774, 0.9107, 1.5773]
# fermi_en = 5.6936
# nbands = 300
# nwfcs = 180

#LiC6
highsymm = [0.0000, 0.6389, 0.9583, 1.5116]
fermi_en = -1.3981
nbands = 100
nwfcs = 29

def saveState():
  a = ln.replace("psi =","+").split("+")
  for i in range(1,len(a)-1):
    b = a[i].split("*")
    state_weight = float(b[0])
    state_id = int(b[1].split()[1].replace("]",""))-1
    state_orbital_type = states_dict["orbital type"][state_id]
    state_atom_type = states_dict["atom type"][state_id]
    state_atom_id = states_dict["atom id"][state_id]
    if state_weight>state_weight_cutoff:
      print("atom id:",state_atom_id,"atom type:",state_atom_type,"state weight:",state_weight,"state id:",state_id,"orbital type:",state_orbital_type)
      psi_dict[(k_dist,band_id)]["state weights"].append(state_weight)
      psi_dict[(k_dist,band_id)]["state ids"].append(state_id)
      psi_dict[(k_dist,band_id)]["state types"].append(state_orbital_type)

      psi_dict[(k_dist,band_id)]["atoms"].append([state_atom_id,state_atom_type])
    else:
      psi_dict[(k_dist,band_id)]["deleted states"] += 1
      # print("*")




# band_id , k_i, x(k distance)_k_i, y(energy)_k_i, contrib_k_i
# data = np.zeros([nbands,nkpoints,2])
# data = np.zeros([nbands,nkpoints,2,ncontribs])
data = np.zeros([nbands,nkpoints,3,ncontribs])


k_id = -1 # if k_id stays -1, no k-points were found in projwfc output
with open(file, "r") as f:
  lines = f.readlines()

  states_dict = {"state":[],"atom id":[],"atom type":[],"wfc id":[],"l":[],"m":[],"orbital type":[]}
  k_dict = {"kx":[],"ky":[],"kz":[],"psi":[],"band energy":[],"k-dist":[]}
  psi_dict = {}
  bands = []
  psi_tmp = []
  line_contains_psi_states = False

  print("=== ATOMIC WAVEFUNCTIONS===")
  for ln_idx,ln in enumerate(lines):
    if "state #" in ln:
      ln2 = ln.split()
      state = int(ln2[2].replace(":",""))
      atom_no = int(ln2[4])
      atom_type = ln2[5].replace("(","")
      wfc_no = int(ln2[8])
      l = int(ln2[9].replace("(","").split("=")[-1])
      m =int(ln2[11].replace(")",""))
      states_dict["state"].append(state)
      states_dict["atom id"].append(atom_no)
      states_dict["atom type"].append(atom_type)
      states_dict["wfc id"].append(wfc_no)
      states_dict["l"].append(l)
      states_dict["m"].append(m)
      states_dict["orbital type"].append(orbital_type[(l,m)])

      print("state:",state,"atom id:",atom_no,"atom type:",atom_type,"wfc id:",wfc_no,"l:",l,"m:",m,"orbital type:",orbital_type[(l,m)])


    if "|psi|^2 =" in ln:
      line_contains_psi_states = False
      # print(10*".","end",10*".") # DEBUG
      print(30*".") # DEBUG
      # print("TEST:",k_dist,band_id)
      # print("BOND TYPE:",psi_dict[(k_dist,band_id)]["bond type"])
      print("deleted states (cutoff={}%):".format(state_weight_cutoff*100),psi_dict[(k_dist,band_id)]["deleted states"])

      bond_type = ""
      state_types = psi_dict[(k_dist,band_id)]["state types"]
      state_weights = psi_dict[(k_dist,band_id)]["state weights"]
      state_atom_types = psi_dict[(k_dist,band_id)]["atoms"]

      # percentage of the density covered by the projected states after applying the cutoff
      psiSq_old = float(ln.strip().split()[-1])
      psiSq_new = np.sum(state_weights)
      psi_dict[(k_dist,band_id)]["|psi^2|"] = np.sum(state_weights)
      print("old |psi^2| {}\t new |psi^2| {}".format(psiSq_old,psiSq_new))


      # calculate orbital projected bond type
      contribs = np.zeros(4) # sigma pi d unknown

      if state_atom_types != []:
        state_atom_types = np.asarray(state_atom_types)[:,1].tolist()

      # condition = True
      # Cs-Cs, C-Cs
      # condition = "Cs" in state_atom_types
      # C-C
      # condition = ("C" in state_atom_types and "Ir" not in state_atom_types and "Cs" not in state_atom_types and "Li" not in state_atom_types)
      # Cs-Ir, Cs-Cs
      #condition = ((("Cs" in state_atom_types and "Ir" not in state_atom_types) or ("Ir" in state_atom_types and "Cs" in state_atom_types)) and "C" not in state_atom_types)
      # Cs-C, Cs-Cs
      #condition = ((("Cs" in state_atom_types and "C" not in state_atom_types) or ("C" in state_atom_types and "Cs" in state_atom_types)) and "Ir" not in state_atom_types)
      condition = (("Li" in state_atom_types and "C" not in state_atom_types) or ("Li" in state_atom_types and "C" in state_atom_types))
      if condition:
        for st,sw,sa in zip(state_types,state_weights,state_atom_types):
          if st=="s":
            contribs[0] += sw
          elif (st=="px" or st=="py"):
            contribs[0] += sw
          elif st=="pz":
            contribs[1] += sw
          # elif st=="dz2":
            # contribs[0] += sw
          # elif (st=="dzx" or st=="dzy"):
            # contribs[1] += sw
          # elif (st=="dx2-y2" or st=="dxy"):
            # contribs[2] += sw
          elif "d" in st:
            contribs[2] += sw
        contribs[3] = 1 - np.sum(contribs)
        print(contribs)
      # fill data array


      for idx, contrib_i in enumerate(contribs):
        try:
          data[band_id,k_id,0,idx] = k_dist
          data[band_id,k_id,1,idx] = band_en
          if psiSq_new>.10:
            data[band_id,k_id,2,idx] = contrib_i
        except IndexError:
          pass
  

      # turn state weights into occupancy 2.0
      state_weights = [item/min(state_weights) for item in state_weights]


      reduced_bond_type = {
      "s":0,
      "px":0,
      "py":0,
      "pz":0,
      "dz2":0,
      "dzx":0,
      "dzy":0,
      "dx2-y2":0,
      "dxy":0
      }

      # def vrstu veze, sumira dorpinose po tipu orbitale, odredi najmanju popunjenost
      min_sw = 10E999
      for st,sw in zip(state_types,state_weights):
        bond_type += "{}({:.2f})".format(st,round(sw,2))
        reduced_bond_type[st] += sw
        if sw<min_sw and sw:
          min_sw = sw


      psi_dict[(k_dist,band_id)]["bond type"] = bond_type
      print("full bond type:",bond_type)

      # # odredi najmanju popunjenost
      # min_sw = 10E999
      # for st,sw in reduced_bond_type.items():
      #     if sw<min_sw and sw:
      #       min_sw = sw

      # normalizacija popunjenosti
      reduced_bond_type = {st: sw/min_sw if sw!=0 else sw for st, sw in reduced_bond_type.items()}
      print("reduced bond type:","".join(["{}({:.2f})".format(st,round(sw,2)) if sw is not 0 else "" for st,sw in reduced_bond_type.items()]))


    elif line_contains_psi_states:
      # print(10*".","continue",10*".") # DEBUG
      saveState()


    if "==== e(" in ln:
      ln2 = ln.split()
      band_id = int(ln2[2].replace(")","")) -1 # start from idx 0 instead of 1
      band_en = float(ln2[4]) - fermi_en
      # print("band id:",band_id,"band energy:",band_en)
      print(10*"=","BAND #{} E= {}".format(band_id,band_en),10*"=")

      # intialize wafefunction save
      line_contains_psi_states = True

      # intialize psi dictionary
      psi_dict[(k_dist,band_id)] = {"state weights":[],"state ids":[],"state types":[],"deleted states":0,"bond type":"","band_en":None, "atoms":[],"|psi^2|":None}

      # save band id and energy
      psi_dict[(k_dist,band_id)]["band_en"] = band_en

    if "k =" in ln:
      k_id += 1 # counter
      kx,ky,kz = ln.split()[2:5]
      kx, ky, kz = float(kx),float(ky), float(kz)
      if k_id == 0:
        k_dist = 0.0
      else:
        k_dist = k_dict["k-dist"][k_id-1] + np.linalg.norm([k_dict["kx"][k_id-1]-kx,k_dict["ky"][k_id-1]-ky,k_dict["kz"][k_id-1]-kz])
      # k_dict je nepotreban u ovom obliku
      k_dict["kx"].append(kx)
      k_dict["ky"].append(ky)
      k_dict["kz"].append(kz)
      k_dict["k-dist"].append(k_dist)
      print(40*"-")
      print("kx:",kx,"ky:",ky,"kz:",kz,"k-dist:",k_dist)
      print(40*"-")


# print(psi_dict.keys())



# print(psi_dict[(0,0,0,1)])
# print("WARNING: Ispisivanje samo prvih 500 linija!")

psi_dict_keys = [*psi_dict]
for key in psi_dict_keys:
  psiSq = np.sum( psi_dict[key]["state weights"])
  psi_dict[key]["|psi^2|"] = psiSq
  # if psi_dict[key]["|psi^2|"] >0 :
    # print(psi_dict[key]["band_en"],psi_dict[key]["|psi^2|"],psi_dict[key]["state weights"],psi_dict[key]["state ids"], psi_dict[key]["state types"], psi_dict[key]["atoms"])

  # print("atom id:",state_atom_id,"atom type:",state_atom_type,"state weight:",state_weight,"state id:",state_id,"orbital type:",state_orbital_type)


# print(data)

for band_idx in range(band_id): 
  # black bands
  plt.plot(data[band_idx,:,0,0],data[band_idx,:,1,0],"k-")
  #SIGMA
  plt.scatter(data[band_idx,:,0,0],data[band_idx,:,1,0],s=data[band_idx,:,2,0]*100,c="magenta",label=r"$\sigma$",alpha=.7)
   #PI
  plt.scatter(data[band_idx,:,0,1],data[band_idx,:,1,1],s=data[band_idx,:,2,1]*100,c="salmon",label=r"$\pi$",alpha=.7)
  # d
  plt.scatter(data[band_idx,:,0,2],data[band_idx,:,1,2],s=data[band_idx,:,2,2]*100,c="lightblue",label=r"$d$",alpha=.7)
  # unknown
  # plt.scatter(data[band_idx,:,0,3],data[band_idx,:,1,3],s=data[band_idx,:,2,3]*100,c="wheat")

# plt.legend(["bands",r"$\sigma$",r"$\pi$",r"$d$"])
# plt.legend()

for h_i in highsymm:
  plt.vlines(h_i,e_min,e_max,linestyle="dashed",lw=0.75,color='k',alpha=.9)

plt.ylim(e_min,e_max)
plt.xlim(np.min(data[0,:,0,0]),np.max(data[0,:,0,0]))
plt.ylabel(r"$E - E_\mathrm{F} \ \left[ \mathrm{eV} \right]$")
plt.xticks(highsymm, (r"$\Gamma$",r"$\mathrm{K}$",r"$\mathrm{M}$",r"$\Gamma$"))
plt.show()
# plt.savefig(file.strip(".out")+".pdf")
