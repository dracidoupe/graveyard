from enum import Enum

RATING_DESCRIPTIONS = {
    0: "Nepovedené",
    1: "Nic moc",
    2: "Něco to má do sebe",
    3: "Průměr",
    4: "Kvalita",
    5: "Geniální",
    6: "Vítěz soutěže",
}


class ApprovalChoices(Enum):
    APPROVED = "a"
    WAITING = "n"
    WITHDRAWN = "q"
    REJECTED = "z"


# Legacy editors also parked works in "r"/"p"/"h" states; those are still awaiting a decision
PENDING_STATES = ("n", "r", "p", "h")
