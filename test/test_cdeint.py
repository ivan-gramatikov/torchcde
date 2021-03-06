import torch
import torchcde


def test_shape():
    for method in ('rk4', 'dopri5'):
        for _ in range(10):
            num_points = torch.randint(low=5, high=100, size=(1,)).item()
            num_channels = torch.randint(low=1, high=3, size=(1,)).item()
            num_hidden_channels = torch.randint(low=1, high=5, size=(1,)).item()
            num_batch_dims = torch.randint(low=0, high=3, size=(1,)).item()
            batch_dims = []
            for _ in range(num_batch_dims):
                batch_dims.append(torch.randint(low=1, high=3, size=(1,)).item())

            t = torch.rand(num_points).sort().values
            values = torch.rand(*batch_dims, num_points, num_channels)

            coeffs = torchcde.natural_cubic_spline_coeffs(values, t)
            spline = torchcde.NaturalCubicSpline(coeffs, t)

            class _Func(torch.nn.Module):
                def __init__(self):
                    super(_Func, self).__init__()
                    self.variable = torch.nn.Parameter(torch.rand(*[1 for _ in range(num_batch_dims)], 1, num_channels))

                def forward(self, t, z):
                    return z.sigmoid().unsqueeze(-1) + self.variable

            f = _Func()
            z0 = torch.rand(*batch_dims, num_hidden_channels)

            num_out_times = torch.randint(low=2, high=10, size=(1,)).item()
            out_times = torch.rand(num_out_times, dtype=torch.float64).sort().values * (t[-1] - t[0]) + t[0]

            options = {}
            if method == 'rk4':
                options['step_size'] = 1. / num_points
            out = torchcde.cdeint(spline, f, z0, out_times, method=method, options=options, rtol=1e-4, atol=1e-6)
            assert out.shape == (*batch_dims, num_out_times, num_hidden_channels)
