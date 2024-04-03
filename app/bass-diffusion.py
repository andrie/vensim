"""
Python model 'bass-diffusion.py'
Translated using PySD
"""


from pysd.py_backend.functions import Integ
from pysd import cache

__pysd_version__ = "1.8.1"

__data = {"scope": None, "time": lambda: 0}

_subscript_dict = {}

_namespace = {
    "TIME": "time",
    "Time": "time",
    "Customers": "customers",
    "Annual customer value": "annual_customer_value",
    "Revenue": "revenue",
    "Marketing effect": "marketing_effect",
    "New customers": "new_customers",
    "Potential customers": "potential_customers",
    "Word of mouth effect": "word_of_mouth_effect",
    "FINAL TIME": "final_time",
    "INITIAL TIME": "initial_time",
    "SAVEPER": "saveper",
    "TIME STEP": "time_step",
}

##########################################################################
#                            CONTROL VARIABLES                           #
##########################################################################


def _init_outer_references(data):
    for key in data:
        __data[key] = data[key]


def time():
    return __data["time"]()


@cache.run
def final_time():
    """
    Real Name: FINAL TIME
    Original Eqn: 100
    Units: Month
    Limits: (None, None)
    Type: constant
    Subs: None

    The final time for the simulation.
    """
    return 100


@cache.run
def initial_time():
    """
    Real Name: INITIAL TIME
    Original Eqn: 0
    Units: Month
    Limits: (None, None)
    Type: constant
    Subs: None

    The initial time for the simulation.
    """
    return 0


@cache.step
def saveper():
    """
    Real Name: SAVEPER
    Original Eqn: TIME STEP
    Units: Month
    Limits: (0.0, None)
    Type: component
    Subs: None

    The frequency with which output is stored.
    """
    return time_step()


@cache.run
def time_step():
    """
    Real Name: TIME STEP
    Original Eqn: 1
    Units: Month
    Limits: (0.0, None)
    Type: constant
    Subs: None

    The time step for the simulation.
    """
    return 1


##########################################################################
#                             MODEL VARIABLES                            #
##########################################################################


@cache.step
def customers():
    """
    Real Name: Customers
    Original Eqn: INTEG ( New customers, 0)
    Units: cpy
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return _integ_customers()


@cache.run
def annual_customer_value():
    """
    Real Name: Annual customer value
    Original Eqn: 10
    Units: $/cust/year
    Limits: (None, None)
    Type: constant
    Subs: None


    """
    return 10


@cache.step
def revenue():
    """
    Real Name: Revenue
    Original Eqn: Customers * Annual customer value
    Units: $/year
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return customers() * annual_customer_value()


@cache.run
def marketing_effect():
    """
    Real Name: Marketing effect
    Original Eqn: 0.003
    Units: 1/mth
    Limits: (0.0, 0.01, 0.0001)
    Type: constant
    Subs: None


    """
    return 0.003


@cache.step
def new_customers():
    """
    Real Name: New customers
    Original Eqn: Potential customers * Marketing effect + Customers*Word of mouth effect * Potential customers/ (Potential customers + Customers)
    Units: cpy/mth
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return (
        potential_customers() * marketing_effect()
        + customers()
        * word_of_mouth_effect()
        * potential_customers()
        / (potential_customers() + customers())
    )


@cache.step
def potential_customers():
    """
    Real Name: Potential customers
    Original Eqn: INTEG ( -New customers, 1000)
    Units: cpy
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return _integ_potential_customers()


@cache.run
def word_of_mouth_effect():
    """
    Real Name: Word of mouth effect
    Original Eqn: 0.1
    Units: 1/ppl/mth
    Limits: (0.0, 0.5, 0.01)
    Type: constant
    Subs: None


    """
    return 0.1


_integ_customers = Integ(lambda: new_customers(), lambda: 0, "_integ_customers")


_integ_potential_customers = Integ(
    lambda: -new_customers(), lambda: 1000, "_integ_potential_customers"
)
