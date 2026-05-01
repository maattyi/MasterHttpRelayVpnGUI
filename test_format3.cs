using System;

public class TestFormat3 {
    public static string Bytes(double n)
    {
        string[] u = { "B", "KB", "MB", "GB", "TB" };
        int i = 0;
        while (n >= 1024 && i < u.Length - 1) { n /= 1024; i++; }
        return n < 10 && i > 0 ? $"{n:0.00} {u[i]}" : $"{n:0.#} {u[i]}";
    }
    public static string PerSec(double bps) => Bytes(bps) + "/s";

    public static void Main() {
        Console.WriteLine(PerSec(415.7));
    }
}
