from Models.membership import Membership

class VIPMembership(Membership):
    def __init__(self, member_id, name, phone, base_price=1500000):
        super().__init__(member_id, name, phone, base_price)

    def calculate_fee(self) -> float:
        return (self.base_price * 1.2) + 300000

    def to_dict(self) -> dict:
        return {
            "member_id": self.member_id,
            "name": self.name,
            "phone": self.phone,
            "type": "VIP",
            "fee": self.calculate_fee()
        }