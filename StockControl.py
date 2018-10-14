## Advanced Programming, coursework 1: Object Orientation
##
## The stock control system classes are unfinished.
## Work through the 14 steps of the coursework to
## implement and extend the methods and classes.
##
##

## Student's Name: Vuchirii Boniface
## Student's Number: 207013984
## Registration Number: 2013/HD05/468U


from datetime import date

"""A stock control system"""
class StockControlSystemError(Exception):
    """Base class for exceptions in this module."""
    print("stock control system error")

class SoldOutOfStockError(StockControlSystemError):
    """Raised when an item is sold that isn't in stock
    Attributes:
    item -- item being sold
    """
    def __init__(self, item):
        self.item = item
        print( "item is being sold yet its not in stock");

class ItemNotFoundError(StockControlSystemError):
    """Raised when an item is sold that isn't in the stock list
    Attributes:
    barcode -- barcode of item being sold
    """
    def __init__(self, barcode):
        self.barcode = barcode

class StockItem(object):
    """Provides the basic stock item class for the stock control system"""
    
    
    def __init__(self, name, barcode, quantity):
        """Provides the basic stock item class for the stock control system
        name     -- name of product (string)        
        barcode  -- barcode of product item (string)        
        quantity -- number of items in stock (integer)
        """
        self.name = name;
        self.barcode = barcode;
        self.quantity = quantity;        

    def toString(self):
        """Returns a string describing the stock item, its barcode and the quantity remaining"""
        stock_item = "Name:"+ self.name + " Barcode:"+ str(self.barcode) + " Number of items in stock:" + str(self.quantity) + "\n";
        return stock_item;
        
    
    def needRestock(self):
        """Returns true if this item needs restocking (i.e. the quantity<a threshold)"""
        threshold = 5;
        if self.quantity< threshold:
          return True;
        else:
          return False;
    
    def sell(self):
        """Process the sale of an item, generates an exception if an item is sold when its stock is zero"""
        if self.quantity <= 0:
          raise SoldOutOfStockError(self)
        self.quantity -= 1
        print("one item of" + self.toString() + "has been sold")
        #hint: use the raise method to create an exception.

    def restock(self,quantity):
          print("previous quantity is:" + str(self.quantity))
          self.quantity = self.quantity +  quantity;
          print("new stocked quantity is now:"+ str(self.quantity));

class PerishableStockItem(StockItem):
    """ The perishable stockitem class """
    def __init__(self,name,barcode, quantity, sellbydate):
      super(PerishableStockItem,self).__init__(name,barcode,quantity);
      self.sellbydate = sellbydate;

    def pastSellByDate(self):
      if date.today()>self.sellbydate:
        return True;
      else:
        return False;
    
    def needRestock(self):
        """Returns true if this item needs restocking (i.e. the quantity<a threshold or it is out of date)"""
        if super(PerishableStockItem,self).needRestock() or date.today() > self.sellbydate:
          return True;
        else:
          return False;

    def toString(self):
      return super(PerishableStockItem,self).toString()+ " Sell by date:" + str(self.sellbydate);



class StockControl(object):
    """The stock control system"""
    
    def __init__(self):
        """The stock control system"""
        self.stocklist = [] #a list of stock items        
    
    def listRestock(self):
        """Return a string listing items that need restocking"""
        count_of_items_that_need_restocking = 0;
        items_that_need_restocking=""
        for stock_item in self.stocklist:
          if stock_item.needRestock() == True:
            items_that_need_restocking = items_that_need_restocking + stock_item.toString()+ "\n";
            count_of_items_that_need_restocking+= 1;
        if count_of_items_that_need_restocking < 1:
          return "All items stocked"
        else:
          return items_that_need_restocking
    
    def addStockType(self,item):
        """Add an item to the stock list"""
        self.stocklist.append(item);
    
    def sellStock(self,barcode):
        """Process the sale of one item"""
        exsts = False;
        for item in self.stocklist:
          if item.barcode == barcode:
            exsts = True
            item.sell();
        if exsts == False:
          raise ItemNotFoundError(barcode)
        
    
    def displayStockList(self):
      for stock_item in self.stocklist:
        print(stock_item.toString())
      print("total number of items in stock is:" + str(len(self.stocklist)))

    def restock(self,barcode,quantity):
      result = [stock_item for stock_item in self.stocklist if stock_item.barcode == str(barcode)];
      if len(result) <= 0:
        raise ItemNotFoundError(self);
      for item in result:
        item.restock(quantity);


#Below is some code to test the classes. Feel free
#to alter this test-code to test your submission
#more thoroughly.

perishable_stock_item = PerishableStockItem('Milk (500ml)','1191',24,date(2019, 10, 26));

#print(stock_item.toString())
print(perishable_stock_item.toString())
print(perishable_stock_item.needRestock())

#Populate the stock control system
stockctrl = StockControl()
stockctrl.addStockType(StockItem('Bag of Coffee','1234',23))
stockctrl.addStockType(StockItem('Salt and Vinegar Crisps','4434',3))
stockctrl.addStockType(StockItem('Museli','0191',2))
stockctrl.addStockType(StockItem('Flour (1kg)','1191',24))

#uncomment to test the PerishableStockItem class for milk
stockctrl.addStockType(PerishableStockItem('Milk (500ml)','1191',24,date(2013, 10, 26)))
stockctrl.addStockType(StockItem('Cookies','2312',6))
stockctrl.addStockType(StockItem('Bags of grapes','1111',0))
#display all items in stock
print('\n All items in stock:\n')
stockctrl.displayStockList()

#Find out what needs restocking
print("Items that need restocking:\n")
print(stockctrl.listRestock())

#Sell some items
print("\n")
print("Testing sales:")
for barcode in ['1234','2312','1112','1111','2312','1191','0191','2312']:
    try:
        stockctrl.sellStock(barcode)    
    except SoldOutOfStockError as e:
        print("Stock sold which isn't in stock:" + e.item.toString())
    except ItemNotFoundError as e:
        print("Item not found:" + e.barcode)

print("\nItems that need restocking:\n")
print(stockctrl.listRestock())

#stockctrl.restock(4494, 10);

#Uncomment this section to test the restock method
print("\nRestocking...\n")
for barcode in ['1111','0191','2312','4434','2312','9999']:
    try:
        stockctrl.restock(barcode,10)    
    except ItemNotFoundError as e:
        print("Item not found:" + e.barcode)
    
print("\nItems that need restocking:\n")
print(stockctrl.listRestock())





