using System;
using System.Globalization;
using System.Text.Json;
using System.Text.Json.Serialization;
using System.Threading;

public class StatsSnapshot
{
    [JsonPropertyName("speed_up")] public double SpeedUp { get; set; }
    [JsonPropertyName("speed_down")] public double SpeedDown { get; set; }
}

public class Program {
    public static void Main() {
        Thread.CurrentThread.CurrentCulture = new CultureInfo("de-DE");
        string json = "{\"speed_up\": 1.23, \"speed_down\": 4.56}";
        var s = JsonSerializer.Deserialize<StatsSnapshot>(json);
        Console.WriteLine($"up: {s.SpeedUp}, down: {s.SpeedDown}");
    }
}
