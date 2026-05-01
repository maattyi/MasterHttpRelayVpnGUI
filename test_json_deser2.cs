using System;
using System.Text.Json;
using System.Text.Json.Serialization;

public class StatsSnapshot
{
    [JsonPropertyName("speed_up")] public double SpeedUp { get; set; }
}

public class Program {
    public static void Main() {
        var s = JsonSerializer.Deserialize<StatsSnapshot>("{\"speed_up\": 12.3}");
        Console.WriteLine(s.SpeedUp);
    }
}
