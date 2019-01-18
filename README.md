# projBands
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/0d6129d523a4468a8af35dff58cbc30a)](https://www.codacy.com/app/Nevensky/projBands?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=Nevensky/projBands&amp;utm_campaign=Badge_Grade)

## Bands
The purpose of this python script is to interpret Quantum Espresso projected band structure calculations. 

Atomic orbitals ![atomic](http://mathurl.com/y9zgkx6m.png) (read from the pseudopotentials) are projected onto Bloch wavefunctions ![bloch](http://mathurl.com/y9lfw2zq.png), giving ![proj](http://mathurl.com/y9nggo8r.png).

The projections are sorted w.r.t. to their orbital contributions (s/p/d/f) to specific bands on each k-point, allow for the identification of ![sigma](http://mathurl.com/y8pnjxgx.png) and ![pi](http://mathurl.com/62kzla.png) bonds. Finally, the band structure is colorplotted w.r.t. orbital and bond types.

## DOS
As a side feature, partial contributions to the electronic density of states are also plotted.

## To-do list
- [x]  read proj.out k-points/bands/states into dictionaries
- [x]  implement state weight cut-off & assign orbitals to states
- [ ]  identify ![sigma](http://mathurl.com/y8pnjxgx.png) and ![pi](http://mathurl.com/62kzla.png) bonds correctly
- [ ]  construct sums of Lorentzians w.r.t. to bond type / orbital type contribution
- [ ]  colorplot band structure
