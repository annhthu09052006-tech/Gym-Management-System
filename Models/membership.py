from abc import ABC, abstractmethod

class Membership(ABC):
    def __init__(self, member_id, name, phone, base_price):
        self._member_id = member_id    # Thuộc tính Private (Tính đóng gói)
        self._name = name              # Thuộc tính Private
        self._phone = phone            # Thuộc tính Private
        
        if base_price < 0:
            raise ValueError("Giá cơ bản không được âm!")
        self._base_price = base_price

    # Các Getters để lấy dữ liệu từ bên ngoài (Encapsulation)
    @property
    def member_id(self): return self._member_id
    
    @property
    def name(self): return self._name
    
    @property
    def phone(self): return self._phone
    
    @property
    def base_price(self): return self._base_price

    @abstractmethod
    def calculate_fee(self) -> float:
        """Phương thức trừu tượng bắt buộc các thẻ con phải ghi đè"""
        pass

    @abstractmethod
    def to_dict(self) -> dict:
        """Chuyển thông tin đối tượng thành dictionary để lưu vào file JSON"""
        pass