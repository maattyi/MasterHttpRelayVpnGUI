using System;
using System.Diagnostics;
using System.Net.Sockets;
using System.Threading;
using System.Threading.Tasks;

namespace MasterRelayVPN.Services;

public sealed record HealthCheckResult(
    bool Reachable,
    double LatencyMs,
    DateTime CheckedAt,
    string Message);

public sealed class HealthMonitorService : IDisposable
{
    CancellationTokenSource? _cts;

    public event Action<HealthCheckResult>? Checked;

    public void Start(Func<bool> shouldCheck, Func<(string Host, int Port)> endpoint)
    {
        Stop();
        _cts = new CancellationTokenSource();
        var ct = _cts.Token;

        _ = Task.Run(async () =>
        {
            while (!ct.IsCancellationRequested)
            {
                try
                {
                    HealthCheckResult result;
                    if (!shouldCheck())
                    {
                        result = new HealthCheckResult(false, 0, DateTime.Now, "offline");
                    }
                    else
                    {
                        var (host, port) = endpoint();
                        result = await ProbeAsync(host, port, ct);
                    }

                    Checked?.Invoke(result);
                    await Task.Delay(TimeSpan.FromSeconds(60), ct);
                }
                catch (OperationCanceledException) { }
                catch (Exception ex)
                {
                    Checked?.Invoke(new HealthCheckResult(false, 0, DateTime.Now, ex.Message));
                    try { await Task.Delay(TimeSpan.FromSeconds(60), ct); }
                    catch (OperationCanceledException) { }
                }
            }
        }, ct);
    }

    static async Task<HealthCheckResult> ProbeAsync(string host, int port, CancellationToken ct)
    {
        var sw = Stopwatch.StartNew();
        using var client = new TcpClient();
        using var timeout = CancellationTokenSource.CreateLinkedTokenSource(ct);
        timeout.CancelAfter(TimeSpan.FromSeconds(3));

        try
        {
            await client.ConnectAsync(host, port, timeout.Token);
            sw.Stop();
            return new HealthCheckResult(true, sw.Elapsed.TotalMilliseconds, DateTime.Now, "reachable");
        }
        catch (OperationCanceledException) when (!ct.IsCancellationRequested)
        {
            return new HealthCheckResult(false, 0, DateTime.Now, "timeout");
        }
        catch (Exception ex)
        {
            return new HealthCheckResult(false, 0, DateTime.Now, ex.Message);
        }
    }

    public void Stop()
    {
        try { _cts?.Cancel(); } catch { }
        _cts = null;
    }

    public void Dispose() => Stop();
}
