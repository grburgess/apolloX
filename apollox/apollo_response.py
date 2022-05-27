import h5py

from rball import ResponseDatabase

from apollox.utils.package_data import get_path_of_data_file


class ApolloResponse(ResponseDatabase):
    def __init__(self, rsp_type: str, name: str) -> None:

        file_name: str = f"rsp_{rsp_type}_database.h5"

        with h5py.File(get_path_of_data_file(file_name), "r") as f:

            # this part is a little polar specific at the moment
            # will remove and generalize

            list_of_matrices = f[f"matrix"][()]

            theta = f["theta"][()]

            phi = f["phi"][()]

            ebounds = f["ebounds"][()]

            mc_energies = f["mc_energies"][()]

        super().__init__(
            list_of_matrices=list_of_matrices,
            theta=theta,
            phi=phi,
            ebounds=ebounds,
            monte_carlo_energies=mc_energies,
        )

        self._name: str = name

    @property
    def name(self) -> str:
        return self._name

    def _transform_to_instrument_coordinates(self, ra: float, dec: float):

        return super()._transform_to_instrument_coordinates(ra, dec)


class Apollo_Al_Response(ApolloResponse):
    def __init__(self):

        """
        The response of the XRFS with the Aluminium filter

        :returns:

        """
        super().__init__(rsp_type="Al", name="XRFS_AL")


class Apollo_Mg_Response(ApolloResponse):
    def __init__(self):

        """
        The response of the XRFS with the Magnesium filter

        :returns:

        """
        super().__init__(rsp_type="Mg", name="XRFS_MG")


class Apollo_Naked_Response(ApolloResponse):
    def __init__(self):

        """
        The response of the XRFS with no filter

        :returns:

        """
        super().__init__(rsp_type="non", name="XRFS_NUDE")
