class Product:
    def __init__(self, id='', proName='', content='', proPrice='', proSale='',colors='', supplier='', category='' , proDes='',proSize='' , createdAt='', updateAt=''):
        self.id             =   id
        self.proName        =   proName 
        self.content        =   content
        self.proPrice       =   proPrice
        self.proSale        =   proSale
        self.colors         =   colors
        self.supplier       =   supplier 
        self.category       =   category
        self.proDes         =   proDes
        self.proSize        =   proSize
        self.createdAt      =   createdAt
        self.updateAt       =   updateAt

    def serialize(self):
        return{
            'id'                : self.id, 
            'name'              : self.proName, 
            'sortDes'           : self.content,   
            'price'             : self.proPrice,
            'sale'              : self.proSale,
            'productOptionColors': self.colors,
            'supplier'          : self.supplier,
            'category'          : self.category,
            'des'               : self.proDes,
            'productOptionSizes': self.proSize,
            'createdAt'         : self.createdAt,
            'updateAt'          : self.updateAt
        }
    def serializeHome(self):
        return{
            'id'            : self.id, 
            'name'          : self.proName, 
            'price'         : self.proPrice,
            'sale'          : self.proSale,
            'image'         : self.colors,
        }