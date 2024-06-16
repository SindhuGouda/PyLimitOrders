from trading_framework.execution_client import ExecutionClient
from trading_framework.price_listener import PriceListener
from trading_framework.execution_client import ExecutionException, Protocol


class LimitOrderAgent(PriceListener):

    def __init__(self, execution_client: ExecutionClient) -> None:
        """

        :param execution_client: can be used to buy or sell - see ExecutionClient protocol definition
        """
        super().__init__()
        self.execution_client = execution_client
        self.orders = []
        self.status = ''
        
    def on_price_tick(self, product_id: str, price: float):
        
        success_list = []
        if product_id == "IBM" and price < 100.0:
            self.execution_client.buy(self, product_id=product_id, amount=1000)
            success_list.append(product_id)
            print('IBM price is less then limit $100.0')
            return success_list
        
        for order in self.orders[:]:
            if order[1] == product_id:
                print('Order ID:',order[1])
                try:
                        print('Buy/Sell flag value: ',order[0])
                        if  order[0] == True and price <= order[3]:
                            try: 
                                print('Limit:',order[3])
                                print('price:',price)
                                self.execution_client.buy(self, product_id=order[1], amount=order[2])
                                self.orders.remove(order)
                                success_list.append(product_id)
                                self.status = "Bought"
                                print("The product is bought")
                                
                            except ExecutionException as e:
                                    print(f"Failed to the buy the order for product {product_id}:{e}")
                                    self.status = "Failed to buy the order"

                        elif  order[0] == False and  price >= order[3] :
                            try :

                                self.execution_client.sell(self, product_id=order[1], amount=order[2])
                                self.orders.remove(order)
                                success_list.append(product_id)
                                self.status = 'Sold'
                                print("The product is sold")
                            
                            except ExecutionException as e:
                                    print(f"Failed to the sell the order for product {product_id}:{e}")
                                    self.status = "Failed to sell the order"
            
                except ExecutionException as e:
                        print(f"Failed to execute order: {e}")
            else:
                raise Exception(f"Product ID '{product_id}' not found in orders. Available products: {[order[1] for order in self.orders]}")
        return success_list
    
    def add_order(self, buy_sell_flag: bool, product_id: str, amount:int, limit:float):
        """
        To add an order in to the  order list
        parameters:
        buy_sell_flag       : flag to indicate buy/sell the order. if it's true it's buy if it's false sell 
        product_id          : the product to buy/sell
        amount              : amount of the product
        limit               : when needs to buy/sell
        return              : None
        """
        
        #Verify that buy_sell_flag is a boolean value, then add a new order to the list of orders with the provided parameters.
        if not isinstance(buy_sell_flag, bool):
            raise ValueError("buy_sell_flag must be a boolean value (True or False)")
        self.orders.append((buy_sell_flag, product_id, amount, limit))
        print(self.orders, "order added successfully")
    
