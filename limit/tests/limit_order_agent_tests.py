import unittest
from execution_client import ExecutionClient
from limit_order_agent import LimitOrderAgent
import re

class LimitOrderAgentTest(unittest.TestCase):

    
    def test_on_price_tick_IBM(self):
        '''Test that a buy order is triggered when the price drops below $100 for IBM.'''
        execution_client = ExecutionClient
        limit_order_client = LimitOrderAgent(execution_client)
        self.assertEqual(limit_order_client.on_price_tick("IBM",99.0), ["IBM"])
        self.assertEqual(limit_order_client.on_price_tick("IBM",100.0), [])
        print('The IBM with price less than 100 testcase passed successfully')

    
    def test_on_price_tick_buy_order(self):
        '''Test that a buy order is executed when the price is below the limit price.'''
        execution_client = ExecutionClient
        limit_order_client = LimitOrderAgent(execution_client)
        limit_order_client.add_order(True, 'IBM', 1000, 180)
        self.assertEqual(limit_order_client.on_price_tick("IBM",110.0), ["IBM"])
        print('The buy order testcase passed successfully')
        

    def test_on_price_tick_sell_order(self):
        '''Test that a sell order is executed when the price is above the limit price.'''
        execution_client = ExecutionClient
        limit_order_client = LimitOrderAgent(execution_client)
        limit_order_client.add_order(False, 'IBM', 1000, 110)
        self.assertEqual(limit_order_client.on_price_tick("IBM",125.0), ["IBM"])
        print('The sell order testcase passed successfully')

    def test_add_order(self):
        '''Test that an order can be added to the agent's order list.'''
        execution_client = ExecutionClient
        limit_order_client = LimitOrderAgent(execution_client)
        limit_order_client.add_order(True, 'Accenture', 1000, 100)
        self.assertEqual(limit_order_client.on_price_tick("Accenture",100.0), ["Accenture"])
        limit_order_client.add_order(False, "EY", 200, 100)
        self.assertEqual(limit_order_client.on_price_tick("EY",100.0), ["EY"])
        limit_order_client.add_order(True, "EY", 200, 100)
        self.assertEqual(limit_order_client.on_price_tick("EY",99.0), ["EY"])
        print('The add order testcase passed successfully')
        
    def test_on_price_tick_product_id_not_present(self):
        '''Test that product id is not present in the orders'''
        execution_client = ExecutionClient
        limit_order_client = LimitOrderAgent(execution_client)
        limit_order_client.add_order(True, 'IBM', 1000, 180)

        with self.assertRaises(Exception) as context:
            limit_order_client.on_price_tick("IBM1", 85.0)
        print(f"Exception raised: {context.exception}")
        self.assertTrue(re.search(r"Product ID '.+' not found in orders", str(context.exception)))
        self.assertIn("Available products: ['IBM']", str(context.exception))
        print('The product id exception testcase passed successfully')

    def test_on_price_tick_buy_sell_flag_not_boolean(self):
        '''Test for checking if the buy_sell_flag has non boolean value '''
        execution_client = ExecutionClient
        limit_order_client = LimitOrderAgent(execution_client)
        with self.assertRaises(ValueError) as cm:
            limit_order_client.add_order("truee", "IBM", 1000, 90.0)  # Add an order with non-boolean buy_sell_flag
            self.fail("Expected ValueError was not raised")  # If no exception is raised, fail the test
        print(f"Caught exception: {cm.exception}")
        print('The buy/sell flag exception testcase passed successfully')


if __name__ == '__main__':
    unittest.main()
