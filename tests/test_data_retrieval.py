from app.data_retrieval import get_data, store_metrics
from app.models import MetricLogs
from unittest.mock import patch, MagicMock
import unittest


class TestDataRetrieval(unittest.TestCase):
    # setUp(): get mock data in a json file 
    def setUp(self):
        self.disk_data = {
            "labels":["time","avail","used","reserved for root"],
            "data":[
                [1745375380,100,6,1]
            ]
        }
        self.network_data = {
            "labels":["time","received","sent"],
            "data":[
                [1745376000,15.5,-16.5]
            ]
        }
        self.cpu_data = {
            "labels":["time","guest_nice","guest","steal","softirq","irq","user","system","nice","iowait"],
            "data":[
                [1745376000,0,0,0.5,0.2,0.4,6,3,0,0.05]
            ]
        }
        self.mem_data = {
            "labels":["time","free","used","cached","buffers"],
            "data":[
                [1745376600,95,670,173.5,6.24]
            ]
        }
    
    def tearDown(self):
        pass

    ## get_data() test
    ## patch decorates func with the method being mocked
    @patch('app.data_retrieval.requests.get')   
    def test_get_data(self, mock_get):
        """ 
        Tests:
            * netapi data retrieval

        Asserts:
            * data returned from get_data is equal to test data
            * get_data correctly requesting the url 

        Mocking: 
            * requests.get - mocking a url response, returning test data instead 
        """

        mock_response = MagicMock()
        # set the mock responses json value to the test data
        mock_response.json.return_value = self.cpu_data
        # set the return value of the requests.get function to mock response
        mock_get.return_value = mock_response
        # now call get_data, will mock the request function, so its returning test data
        test_output = get_data("http://45.79.180.177:19999", chart="system.cpu")

        # find expected output, with timestamp stripped
        expected = self.cpu_data['data'][0][1:]

        # assert equality 
        self.assertEqual(test_output, expected, "Data not retrieved correctly")
    
        # assert mocked response came from the correct url 
        expected_url = "http://45.79.180.177:19999/api/v1/data?chart=system.cpu&points=1&format=json"
        mock_get.assert_called_with(expected_url, timeout=5)
    
    ## store_metrics() test
    @patch('app.data_retrieval.scheduler.app.app_context')
    @patch('app.data_retrieval.db.session')
    @patch('app.data_retrieval.get_data')
    def test_store_metrics(self, mock_get_data, mock_db_session, mock_app_context):
        """
        Tests:
            * correct arithmetic is being done on data 
            * data is added to metric log
            * commits are successful
        Asserts:
            * data operations are correct between test data and store metrics function
            # data is being stored correctly 
            * db.session.add is called adding metric logs to db 
            * db session is being committed
        Mocking:
            * get_data function
            * db.session
            * app_context
        """
        mock_context = MagicMock()
        mock_app_context.return_value.__enter__.return_value = mock_context 

        # list to capture all created MetricLogs instances
        mock_log_instances = []

        def create_mock_log(*args, **kwargs):
            mock = MagicMock()
            mock.configure_mock(**kwargs)
            mock_log_instances.append(mock)
            return mock
        
        with patch('app.data_retrieval.MetricLogs', side_effect=create_mock_log):
        # configure mock_get_data to return different values based on chart parameter
            def mock_get_data_side_effect(host, chart, points=1):
                if chart == "system.cpu":
                    return self.cpu_data['data'][0][1:]
                elif chart == "system.net":
                    return self.network_data['data'][0][1:]
                elif chart == "system.ram":
                    return self.mem_data['data'][0][1:]
                elif chart == "disk_space./":
                    return self.disk_data['data'][0][1:]
                return None
            
        
        mock_get_data.side_effect = mock_get_data_side_effect

        store_metrics()

        # check that appropriate metric logs were created for each server
        self.assertEqual(len(mock_log_instances), 2)
        self.assertEqual(mock_log_instances[0].machine_name, "server_1")
        self.assertEqual(mock_log_instances[1].machine_name, "server_2")
        
        # Test CPU Usage calculation
        expected_cpu_usage = sum(self.cpu_data['data'][0][1:])
        self.assertEqual(mock_log_instances[0].cpu_usage, expected_cpu_usage)
        
        # Test Network metrics
        expected_received = self.network_data['data'][0][1] 
        expected_sent = abs(self.network_data['data'][0][2]) 
        self.assertEqual(mock_log_instances[0].network_received, expected_received)
        self.assertEqual(mock_log_instances[0].network_sent, expected_sent)
        
        # Test Memory Usage calculation
        used = self.mem_data['data'][0][2]  
        total = sum(self.mem_data['data'][0][1:])  
        expected_memory_percent = (used / total) * 100
        self.assertAlmostEqual(mock_log_instances[0].memory_usage, expected_memory_percent, places=2)
        
        # Test Disk Usage calculation
        disk_total = sum(self.disk_data['data'][0][1:])  
        disk_used = sum(self.disk_data['data'][0][2:])  
        expected_disk_percent = (disk_used / disk_total) * 100 
        self.assertAlmostEqual(mock_log_instances[0].disk_usage, expected_disk_percent, places=2)
        
        # Check that db.session.add was called twice, once for each serevr 
        self.assertEqual(mock_db_session.add.call_count, 2)
        
        # Ensure commit was called 
        mock_db_session.commit.assert_called_once()


if __name__ == "__main__":
    unittest.main()