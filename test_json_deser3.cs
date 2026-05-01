using System;
using System.Globalization;
using System.Text.Json;
using System.Text.Json.Serialization;
using System.Threading;

public class StatsSnapshot
{
    [JsonPropertyName("speed_up")] public double SpeedUp { get; set; }
}

public class Program {
    public static void Main() {
        Thread.CurrentThread.CurrentCulture = new CultureInfo("de-DE");
        var s = JsonSerializer.Deserialize<StatsSnapshot>("{\"speed_up\": 12.3}");
        Console.WriteLine(s.SpeedUp);
    }
}
