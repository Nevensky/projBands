#!/usr/bin/env python3
import numpy as np
import sys

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

state_weight_cutoff = .05 # 5%

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


file = sys.argv[1]
# file = "/Users/nevensky/Desktop/vito/graphene/gr.proj.out"


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
      psi_dict[(kx,ky,kz,band_id)]["state weights"].append(state_weight)
      psi_dict[(kx,ky,kz,band_id)]["state ids"].append(state_id)
      psi_dict[(kx,ky,kz,band_id)]["state types"].append(state_orbital_type)
    else:
      psi_dict[(kx,ky,kz,band_id)]["deleted states"] += 1
      # print("*")



with open(file, "r") as f:
  lines = f.readlines()

  states_dict = {"state":[],"atom id":[],"atom type":[],"wfc id":[],"l":[],"m":[],"orbital type":[]}
  k_dict = {"kx":[],"ky":[],"kz":[],"psi":[],"band energy":[]}
  psi_dict = {}
  psi_tmp = []
  psi_save = False
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
      psi_save = False
      # print(10*".","end",10*".") # DEBUG
      print(30*".") # DEBUG
      # print("TEST:",kx,ky,kz,band_id)
      # print("BOND TYPE:",psi_dict[(kx,ky,kz,band_id)]["bond type"])
      print("deleted states (cutoff={}%):".format(state_weight_cutoff*100),psi_dict[(kx,ky,kz,band_id)]["deleted states"])

      bond_type = ""
      state_types = psi_dict[(kx,ky,kz,band_id)]["state types"]
      state_weights = psi_dict[(kx,ky,kz,band_id)]["state weights"]
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


      psi_dict[(kx,ky,kz,band_id)]["bond type"] = bond_type
      print("full bond type:",bond_type)

      # # odredi najmanju popunjenost
      # min_sw = 10E999
      # for st,sw in reduced_bond_type.items():
      #     if sw<min_sw and sw:
      #       min_sw = sw

      # normalizacija popunjenosti
      reduced_bond_type = {st: sw/min_sw if sw!=0 else sw for st, sw in reduced_bond_type.items()}
      print("reduced bond type:","".join(["{}({:.2f})".format(st,round(sw,2)) if sw is not 0 else "" for st,sw in reduced_bond_type.items()]))

    elif psi_save:
      # print(10*".","continue",10*".") # DEBUG
      saveState()


    if "==== e(" in ln:
      ln2 = ln.split()
      band_id = int(ln2[2].replace(")","")) # -1 dodati eventualno
      band_en = float(ln2[4])
      # print("band id:",band_id,"band energy:",band_en)
      print(10*"=","BAND #{} E= {}".format(band_id,band_en),10*"=")

      # intialize wafefunction save
      psi_save = True

      # intialize psi dictionary
      psi_dict[(kx,ky,kz,band_id)] = {"state weights":[],"state ids":[],"state types":[],"deleted states":0,"bond type":""}

    if "k =" in ln:
      kx,ky,kz = ln.split()[2:5]
      kx, ky, kz = float(kx),float(ky), float(kz)
      k_dict["kx"].append(kx)
      k_dict["ky"].append(ky)
      k_dict["kz"].append(kz)
      print(40*"-")
      print("kx:",kx,"ky:",ky,"kz:",kz)
      print(40*"-")
# print(psi_dict.keys())



# print(psi_dict[(0,0,0,1)])
# print("WARNING: Ispisivanje samo prvih 500 linija!")