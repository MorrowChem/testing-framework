# Model for Stillinger-Weber with original parameters for Si (Z=14)

from quippy.potential import Potential

# A module defining a module needs to define only one variable,
# named `calculator`, which should be an instance of the ase.calculator.Calculator,
# a subclass of this, or a compatible class implementing the calculator interface.

calculator = Potential('IP TS', param_str="""

<!-- Long-range fit to same LDA database -->
<TS_params label="ewald_LDA" betapol="0.75" cutoff_coulomb="20.0" cutoff_ms="22.0" smoothlength_ms="18.0" \
                  tolpol="1e-10" iesr="-1 -1 -1" a_ew="1e-06" n_types="2" gcut="0.0" \
                  pred_order="2" maxipol="60" raggio="0.0" tewald="T">

  <per_type_data atomic_num="8" pol="6.0204711" z="-1.4828267" type="1" />
  <per_type_data atomic_num="14" pol="0.0" z="2.9656534" type="2" />

  <per_pair_data C_pol="0.46554812" atnum_j="8" atnum_i="8" D_ms="0.0002032023" gamma_ms="10.89313" B_pol="1.0768296" R_ms="8.3955036" />
  <per_pair_data C_pol="-1.4947753" atnum_j="8" atnum_i="14" D_ms="0.0021072801" gamma_ms="11.016375" B_pol="2.0996956" R_ms="4.7425089" />
  <per_pair_data C_pol="0.0" atnum_j="14" atnum_i="14" D_ms="0.031452519" gamma_ms="10.839689" B_pol="0.0" R_ms="4.9469448" />

</TS_params>
""")

no_checkpoint = True
calculator.name = 'TS'
name = 'TS'

