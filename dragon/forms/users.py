from enum import Enum


class RegistrationRequestApproval(Enum):
    APPROVE = "Schválit"
    REJECT = "Zamítnout"


RegistrationRequestApproval.do_not_call_in_templates = True
