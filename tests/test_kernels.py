import pytest
import torch
from HIL.optimization.kernel import SE, Matern, kernel


def test_kernel_base_class():
    class TestKernel(kernel):
        def __init__(self):
            super().__init__()
            self.kernel_name = "TestKernel"
            self.n_parms = 1
    
    with pytest.raises(TypeError) as e: 
        test_kernel = TestKernel() # type: ignore

    

def test_get_covr_module():
    class IncompleteKernel(kernel):
        def __init__(self):
            super().__init__()
            self.kernel_name = "IncompleteKernel"
            self.n_parms = 1

        def get_covr_module(self):
            return super().get_covr_module() # type: ignore

        def reset(self):
            return super().reset() # type: ignore

    incomplete_kernel = IncompleteKernel()

    with pytest.raises(NotImplementedError) as exc_info:
        incomplete_kernel.reset()
    
    assert "" in str(exc_info.value)
    
    with pytest.raises(NotImplementedError) as exc_info:
        incomplete_kernel.get_covr_module()
    
    assert "" in str(exc_info.value)

def test_se_reset():
    # Initialize SE kernel with specific constraints
    se_kernel = SE(
        n_parms=1,
        length_scale=(0.1, 10),
        variance_constraints=(0.1, 10)
    )
    
    # Store initial parameters
    initial_covar_module = se_kernel.get_covr_module()
    initial_lengthscale = initial_covar_module.base_kernel.lengthscale.detach().clone()
    initial_outputscale = initial_covar_module.outputscale.detach().clone()
    
    # Modify the covar_module parameters
    with torch.no_grad():
        old_lengthscale = initial_covar_module.base_kernel.lengthscale.detach().clone()
        initial_covar_module.base_kernel.lengthscale += torch.tensor([0.5])
        initial_covar_module.outputscale = torch.tensor([2.0])
    
    # Assert that parameters have been modified
    assert se_kernel.get_covr_module().base_kernel.lengthscale.sum() == old_lengthscale.sum() + 0.5, "Lengthscale not modified correctly."
    assert se_kernel.get_covr_module().outputscale.sum() == 2.0, "Outputscale not modified correctly."
    
    # Call the reset method
    se_kernel.reset()
    
    # Retrieve the covar_module after reset
    reset_covar_module = se_kernel.get_covr_module()
    reset_lengthscale = reset_covar_module.base_kernel.lengthscale
    reset_outputscale = reset_covar_module.outputscale
    
    # Assert that parameters have been reset to initial values
    assert torch.allclose(reset_lengthscale, initial_lengthscale), "Lengthscale was not reset correctly."
    assert torch.allclose(reset_outputscale, initial_outputscale), "Outputscale was not reset correctly."

def test_matern_reset():
    # Initialize Matern kernel with specific constraints
    matern_kernel = Matern(
        n_parms=2,
        length_scale=(0.0, 10.0),
        variance_constraints=(0.0, 10.0)
    )
    
    # Store initial parameters
    initial_covar_module = matern_kernel.get_covr_module()
    initial_lengthscale = initial_covar_module.base_kernel.lengthscale.detach().clone()
    initial_outputscale = initial_covar_module.outputscale.detach().clone()
    
    # Modify the covar_module parameters
    with torch.no_grad():
        initial_covar_module.base_kernel.lengthscale = torch.tensor([10.0, 10.0])
        initial_covar_module.outputscale = torch.tensor([10.0])
    
    # Assert that parameters have been modified
    print(matern_kernel.get_covr_module().base_kernel.lengthscale)
    print(matern_kernel.get_covr_module().outputscale)
    assert matern_kernel.get_covr_module().base_kernel.lengthscale.sum() == 20.0, "Lengthscale not modified correctly."
    assert matern_kernel.get_covr_module().outputscale.sum() == 10.0, "Outputscale not modified correctly."
    
    # Call the reset method
    matern_kernel.reset()
    
    # Retrieve the covar_module after reset
    reset_covar_module = matern_kernel.get_covr_module()
    reset_lengthscale = reset_covar_module.base_kernel.lengthscale
    reset_outputscale = reset_covar_module.outputscale
    
    # Assert that parameters have been reset to initial values
    assert torch.allclose(reset_lengthscale, initial_lengthscale), "Lengthscale was not reset correctly."
    assert torch.allclose(reset_outputscale, initial_outputscale), "Outputscale was not reset correctly."