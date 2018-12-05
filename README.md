# projBands

## projBands
The purpose of this python script is to interpret Quantum Espresso projected band structure calculations. 

Atomic orbitals $\langle\phi_i|$ (read from the pseudopotentials) are projected onto Bloch wavefunctions $|\psi_{nk}\rangle$, giving $\langle \phi_i|\psi_{nk}\rangle$.

The projections are sorted w.r.t. to their orbital contributions (s/p/d/f) to specific bands on each k-point, allow for the identification of $\sigma$ and $\pi$ bonds. Finally, the band structure is colorplotted w.r.t. orbital and bond types.

## projDOS
As a side feature, partial contributions to the electronic density of states are also plotted.

# To-do list
- [x] read proj.out k-points/bands/states into dictionaries
- [x] implement state weight cut-off & assign orbitals to states
- [ ] identify $\sigma$ and $\pi$ bonds correctly
- [ ] construct sums of Lorentzians w.r.t. to bond type / orbital type contribution
- [ ] colorplot band structure