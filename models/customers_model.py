class  Customer:
    def __init__(self, id='', email='', password='', image='', gender='', lastName='', firstName='', city='', distric='', street='', address='', phone='', birthDay='', acc_point='',ok='ok'):
        self.ok         = ok
        self.id         = id
        self.email      = email
        self.password   = password
        self.image      = image
        self.gender     = gender
        self.lastName   = lastName
        self.firstName  = firstName
        self.city       = city
        self.distric    = distric
        self.street     = street 
        self.address    = address
        self.phone      = phone
        self.birthDay   = birthDay
        self.acc_point  = acc_point

    def serialize(self):
        return{
            'id'        : self.id,         
            'email'     : self.email,
            'image'     : self.image,      
            'gender'    : self.gender,     
            'lastName'  : self.lastName,   
            'firstName' : self.firstName,  
            'city'      : self.city,      
            'distric'   : self.distric,    
            'street'    : self.street,     
            'address'   : self.address,    
            'phone'     : self.phone,     
            'birthDay'  : self.birthDay
        }