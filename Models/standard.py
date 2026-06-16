from Models.membership import Membership

class StandardMembership(Membership):
    def __init__(self, member_id, name, phone, base_price=500000):
        super().__init__(member_id, name, phone, base_price) # Kế thừa lớp cha

    def calculate_fee(self) -> float:
        return self.base_price  # Thẻ thường giữ nguyên giá gốc
    
    def to_dict(self) -> dict:
        return {
            "member_id": self.member_id,
            "name": self.name,
            "phone": self.phone,
            "type": "Standard",
            "fee": self.calculate_fee()
        }