from Models.membership import Membership

class PremiumMembership(Membership):
    def __init__(self, member_id, name, phone, base_price=800000):
        super().__init__(member_id, name, phone, base_price)

    def calculate_fee(self) -> float:
        return self.base_price + 200000  # Tính thêm phí dịch vụ hồ bơi

    def to_dict(self) -> dict:
        return {
            "member_id": self.member_id,
            "name": self.name,
            "phone": self.phone,
            "type": "Premium",
            "fee": self.calculate_fee()
        }