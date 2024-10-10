from unittest.mock import Mock, patch

def test_start_positive(hil_instance):
    
    # Mock input function
    input_mock = Mock(side_effect=['', 'Y', '', 'Y', '', 'Y', '', 'Y', ''])
    
    # Mock the extract_data method to return only two values
    hil_instance.cost.extract_data = Mock(return_value=([0.5], 1234))
    
    with patch('builtins.input', input_mock):
        
        # Run the start method
        hil_instance.start()

    # Add assertions to check the final state of hil_instance
    assert hil_instance.n == 5, f"Expected 5 iterations, but got {hil_instance.n}"
    assert len(input_mock.call_args_list) > 0, "Expected input to be called"
    # Add more assertions as needed

# def test_start_negative(hil_instance):
#     # Mock the input function to simulate keyboard input (including a 'N' to reject a measurement)
#     with patch('builtins.input', side_effect=['', 'Y', '', 'N', 'Y', '', 'Y', '', 'Y', '']):
#         # Mock the _get_cost method to return predetermined values
#         hil_instance._get_cost = Mock()
#         hil_instance.store_cost_data = [1.0, 2.0, 3.0, 4.0, 5.0]
#         hil_instance.cost_time = 100
#         hil_instance.start_time = 0

#         # Run the start method
#         hil_instance.start()

#         # Assert that the optimization completed successfully, but with one rejected measurement
#         assert hil_instance.n == 5
#         assert len(hil_instance.x_opt) == 5
#         assert len(hil_instance.y_opt) == 5
#         assert hil_instance.BO.run.call_count == 2  # Called twice during optimization

# def test_start_warm_up(hil_instance):
#     # Mock the input function to simulate user input
#     with patch('builtins.input', side_effect=['', 'Y', '', 'Y', '', 'Y', '', 'Y', '']):
#         # Mock the _get_cost method to return predetermined values
#         hil_instance._get_cost = Mock()
#         hil_instance.store_cost_data = [1.0, 2.0, 3.0, 4.0, 5.0]
#         hil_instance.cost_time = 100
#         hil_instance.start_time = 0

#         # Ensure warm_up is True
#         hil_instance.warm_up = True
#         print(hil_instance.warm_up)

#         # Run the start method
#         hil_instance.start()

#         # Assert that warm_up became False
#         assert hil_instance.warm_up == False

# def test_start_optimization_transition(hil_instance):
#     # Mock the input function to simulate user input
#     with patch('builtins.input', side_effect=['', 'Y', '', 'Y', '', 'Y', '', 'Y', '']):
#         # Mock the _get_cost method to return predetermined values
#         hil_instance._get_cost = Mock()
#         hil_instance.store_cost_data = [1.0, 2.0, 3.0, 4.0, 5.0]
#         hil_instance.cost_time = 100
#         hil_instance.start_time = 0
#         hil_instance.n = hil_instance.args['Optimization']['n_exploration']
#         hil_instance.OPTIMIZATION = False
#         hil_instance.start()

#         # Assert that OPTIMIZATION became True
#         assert hil_instance.OPTIMIZATION == True
#         # BO.run should have been called
#         assert hil_instance.BO.run.call_count > 0
