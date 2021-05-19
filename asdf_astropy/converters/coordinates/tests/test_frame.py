

import pytest

import asdf
from astropy import units as u
from astropy.coordinates import (
    Angle,
    CartesianRepresentation,
    CIRS,
    FK4,
    FK4NoETerms,
    FK5,
    Galactic,
    Galactocentric,
    GCRS,
    ICRS,
    ITRS,
    Latitude,
    Longitude,
    PrecessedGeocentric,
    SphericalRepresentation,
)
from astropy.time import Time
import numpy as np

from asdf_astropy.testing.helpers import assert_frame_equal


TEST_DATA = {
    "ra": 1 * u.deg,
    "dec": 2 * u.deg,
}

TEST_FRAMES = [
    CIRS(**TEST_DATA),
    CIRS(**TEST_DATA, obstime=Time("J2005")),
    FK4(**TEST_DATA),
    FK4(**TEST_DATA, obstime=Time("B1950")),
    FK4NoETerms(**TEST_DATA),
    FK4NoETerms(**TEST_DATA, obstime= Time("J1975")),
    FK5(**TEST_DATA),
    FK5(**TEST_DATA, equinox="J2005"),
    FK5(**TEST_DATA, equinox="2011-01-01T00:00:00"),
    Galactic(l=47.37 * u.degree, b=+6.32 * u.degree),
    Galactocentric(
        x=np.linspace(-10., 10., 100) * u.kpc,
        y=np.linspace(-10., 10., 100) * u.kpc,
        z=np.zeros(100) * u.kpc,
        z_sun=15 * u.pc
    ),
    GCRS(**TEST_DATA),
    GCRS(**TEST_DATA, obsgeoloc=CartesianRepresentation([1, 2, 3], unit=u.m)),
    ICRS(**TEST_DATA),
    ICRS(ra=Longitude(25, unit=u.deg), dec=Latitude(45, unit=u.deg)),
    ICRS(ra=Longitude(25, unit=u.deg, wrap_angle=Angle(1.5, unit=u.rad)), dec=Latitude(45, unit=u.deg)),
    ICRS(ra=[0, 1, 2] * u.deg, dec=[3, 4, 5] * u.deg),
    ITRS(SphericalRepresentation(lon=12.3 * u.deg, lat=45.6 * u.deg, distance=1 * u.km)),
    PrecessedGeocentric(**TEST_DATA),
    PrecessedGeocentric(**TEST_DATA, equinox="B1975"),
]


@pytest.mark.parametrize("frame", TEST_FRAMES)
def test_serialization(frame, tmp_path):
    file_path = tmp_path / "test.asdf"
    with asdf.AsdfFile() as af:
        af["frame"] = frame
        af.write_to(file_path)

    with asdf.open(file_path) as af:
        assert_frame_equal(af["frame"], frame)
