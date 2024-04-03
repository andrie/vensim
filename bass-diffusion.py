"""
Python model 'bass-diffusion.py'
Translated using PySD
"""

from pathlib import Path
import numpy as np

from pysd.py_backend.statefuls import Integ
from pysd import Component

__pysd_version__ = "3.13.4"

__data = {"scope": None, "time": lambda: 0}

_root = Path(__file__).parent


component = Component()

#######################################################################
#                          CONTROL VARIABLES                          #
#######################################################################

_control_vars = {
    "initial_time": lambda: 0,
    "final_time": lambda: 100,
    "time_step": lambda: 1,
    "saveper": lambda: time_step(),
}


def _init_outer_references(data):
    for key in data:
        __data[key] = data[key]


@component.add(name="Time")
def time():
    """
    Current time of the model.
    """
    return __data["time"]()


@component.add(
    name="FINAL TIME", units="Month", comp_type="Constant", comp_subtype="Normal"
)
def final_time():
    """
    The final time for the simulation.
    """
    return __data["time"].final_time()


@component.add(
    name="INITIAL TIME", units="Month", comp_type="Constant", comp_subtype="Normal"
)
def initial_time():
    """
    The initial time for the simulation.
    """
    return __data["time"].initial_time()


@component.add(
    name="SAVEPER",
    units="Month",
    limits=(0.0, np.nan),
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"time_step": 1},
)
def saveper():
    """
    The frequency with which output is stored.
    """
    return __data["time"].saveper()


@component.add(
    name="TIME STEP",
    units="Month",
    limits=(0.0, np.nan),
    comp_type="Constant",
    comp_subtype="Normal",
)
def time_step():
    """
    The time step for the simulation.
    """
    return __data["time"].time_step()


#######################################################################
#                           MODEL VARIABLES                           #
#######################################################################


@component.add(
    name="Indicated change in staff",
    units="1",
    comp_type="Constant",
    comp_subtype="Normal",
)
def indicated_change_in_staff():
    return 0


@component.add(
    name="Adjustment time", units="Month", comp_type="Constant", comp_subtype="Normal"
)
def adjustment_time():
    return 1


@component.add(
    name="Response time",
    units="Month",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"open_tickets": 1, "new_ticket_rate": 1},
)
def response_time():
    """
    Little's law
    """
    return open_tickets() / new_ticket_rate()


@component.add(
    name="Max closing rate",
    units="tkt/Month",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"open_tickets": 1, "adjustment_time": 1},
)
def max_closing_rate():
    return open_tickets() / adjustment_time()


@component.add(
    name="Closing ticket rate",
    units="tkt/Month",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ticket_closing_capacity": 1, "max_closing_rate": 1},
)
def closing_ticket_rate():
    return np.minimum(ticket_closing_capacity(), max_closing_rate())


@component.add(
    name="Available monthly hours",
    units="Month",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"support_staff": 1, "support_person_hours": 1},
)
def available_monthly_hours():
    return support_staff() * support_person_hours()


@component.add(
    name="Change in support staff",
    units="ppl/Month",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "indicated_change_in_staff": 1,
        "support_staff": 1,
        "staff_hiring_time": 1,
    },
)
def change_in_support_staff():
    return (indicated_change_in_staff() * support_staff()) / staff_hiring_time()


@component.add(
    name="Conversation time hours",
    units="hour/message",
    limits=(0.25, 2.0, 0.25),
    comp_type="Constant",
    comp_subtype="Normal",
)
def conversation_time_hours():
    return 0.5


@component.add(
    name="Support person hours",
    units="Month/ppl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def support_person_hours():
    return 16 * 20 / (30 * 24)


@component.add(
    name="SLA hours", units="hour", comp_type="Constant", comp_subtype="Normal"
)
def sla_hours():
    return 24


@component.add(
    name="Ticket closing capacity",
    units="tkt/Month",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"available_monthly_hours": 1, "time_required_per_ticket": 1},
)
def ticket_closing_capacity():
    return available_monthly_hours() / time_required_per_ticket()


@component.add(
    name="SLA",
    units="Month",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"sla_hours": 1},
)
def sla():
    return sla_hours() / (24 * 30)


@component.add(
    name="Staff hiring time", units="Month", comp_type="Constant", comp_subtype="Normal"
)
def staff_hiring_time():
    return 6


@component.add(
    name="Time per conversation",
    units="mth/msg",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"conversation_time_hours": 1},
)
def time_per_conversation():
    return conversation_time_hours() / (24 * 30)


@component.add(
    name="Time required per ticket",
    units="Month/tkt",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"conversations_per_ticket": 1, "time_per_conversation": 1},
)
def time_required_per_ticket():
    return conversations_per_ticket() * time_per_conversation()


@component.add(
    name="Accumulated tickets",
    units="tkt",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_accumulated_tickets": 1},
    other_deps={
        "_integ_accumulated_tickets": {
            "initial": {},
            "step": {"closing_ticket_rate": 1},
        }
    },
)
def accumulated_tickets():
    return _integ_accumulated_tickets()


_integ_accumulated_tickets = Integ(
    lambda: closing_ticket_rate(), lambda: 0, "_integ_accumulated_tickets"
)


@component.add(
    name="Tickets per new customer",
    units="tkt/logo",
    limits=(0.0, np.nan),
    comp_type="Constant",
    comp_subtype="Normal",
)
def tickets_per_new_customer():
    return 1


@component.add(
    name="Conversations per ticket",
    units="msg/tkt",
    comp_type="Constant",
    comp_subtype="Normal",
)
def conversations_per_ticket():
    return 20


@component.add(
    name="Open tickets",
    units="tkt",
    limits=(0.0, np.nan),
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_open_tickets": 1},
    other_deps={
        "_integ_open_tickets": {
            "initial": {},
            "step": {"new_ticket_rate": 1, "closing_ticket_rate": 1},
        }
    },
)
def open_tickets():
    return _integ_open_tickets()


_integ_open_tickets = Integ(
    lambda: new_ticket_rate() - closing_ticket_rate(), lambda: 0, "_integ_open_tickets"
)


@component.add(
    name="New customers",
    units="logo/Month",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "potential_customers": 3,
        "marketing_effect": 1,
        "word_of_mouth_effect": 1,
        "customers": 2,
    },
)
def new_customers():
    return (
        potential_customers() * marketing_effect()
        + customers()
        * word_of_mouth_effect()
        * potential_customers()
        / (potential_customers() + customers())
    )


@component.add(
    name="New ticket rate",
    units="tkt/Month",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "new_customers": 1,
        "tickets_per_new_customer": 1,
        "tickets_per_existing_customer": 1,
        "customers": 1,
    },
)
def new_ticket_rate():
    return (
        new_customers() * tickets_per_new_customer()
        + customers() * tickets_per_existing_customer()
    )


@component.add(
    name="Tickets per existing customer",
    units="tkt/logo/Month",
    limits=(0.0, 0.1, 0.01),
    comp_type="Constant",
    comp_subtype="Normal",
)
def tickets_per_existing_customer():
    return 0.05


@component.add(
    name="Support staff",
    units="ppl",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_support_staff": 1},
    other_deps={
        "_integ_support_staff": {"initial": {}, "step": {"change_in_support_staff": 1}}
    },
)
def support_staff():
    return _integ_support_staff()


_integ_support_staff = Integ(
    lambda: change_in_support_staff(), lambda: 1, "_integ_support_staff"
)


@component.add(
    name="Revenue",
    units="$/Month",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"customers": 1, "annual_customer_value": 1},
)
def revenue():
    return customers() * annual_customer_value() / 12


@component.add(
    name="Customers",
    units="logo",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_customers": 1},
    other_deps={"_integ_customers": {"initial": {}, "step": {"new_customers": 1}}},
)
def customers():
    return _integ_customers()


_integ_customers = Integ(lambda: new_customers(), lambda: 0, "_integ_customers")


@component.add(
    name="Annual customer value",
    units="$/logo/Month",
    comp_type="Constant",
    comp_subtype="Normal",
)
def annual_customer_value():
    return 10


@component.add(
    name="Marketing effect",
    units="1/Month",
    limits=(0.0, 0.01, 0.0001),
    comp_type="Constant",
    comp_subtype="Normal",
)
def marketing_effect():
    return 0.003


@component.add(
    name="Potential customers",
    units="logo",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_potential_customers": 1},
    other_deps={
        "_integ_potential_customers": {"initial": {}, "step": {"new_customers": 1}}
    },
)
def potential_customers():
    return _integ_potential_customers()


_integ_potential_customers = Integ(
    lambda: -new_customers(), lambda: 1000, "_integ_potential_customers"
)


@component.add(
    name="Word of mouth effect",
    units="1/Month",
    limits=(0.0, 0.5, 0.01),
    comp_type="Constant",
    comp_subtype="Normal",
)
def word_of_mouth_effect():
    return 0.1
