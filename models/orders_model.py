class Order:
    def __init__(self, id='', codeOrder='',customerId='', shiperId = '', statusOrderId='', createdAt='', DateOfDeli='' ):
        self.id = id
        self.codeOrder= codeOrder
        self.customerId = customerId
        self.shiperId = shiperId
        self.statusOrderId = statusOrderId
        self.createdAt = createdAt
        self.DateOfDeli = DateOfDeli
    
    def serialize(self, detail):
        return {
            'id'            : self.id,
            'codeOrder'     : self.codeOrder,
            'customer'    : self.customerId,
            'statusOrder' : self.statusOrderId,
            'createdAt'     : self.createdAt,
            'DateOfDeli'    : self.DateOfDeli,
            'detail'        : detail
        }