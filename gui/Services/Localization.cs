using System.Collections.Generic;
using System.ComponentModel;
using System.Windows;

namespace MasterRelayVPN.Services;

public class Localization : INotifyPropertyChanged
{
    public static Localization Instance { get; } = new();

    public event PropertyChangedEventHandler? PropertyChanged;

    string _lang = "en";
    public string Lang
    {
        get => _lang;
        set
        {
            if (_lang == value) return;
            _lang = value == "fa" ? "fa" : "en";
            FlowDirection = _lang == "fa" ? FlowDirection.RightToLeft : FlowDirection.LeftToRight;
            PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(string.Empty));
            PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(nameof(FlowDirection)));
            PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(nameof(IsRtl)));
            PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(nameof(LanguageButtonLabel)));
        }
    }

    public FlowDirection FlowDirection { get; private set; } = FlowDirection.LeftToRight;
    public bool IsRtl => FlowDirection == FlowDirection.RightToLeft;
    public string LanguageButtonLabel => _lang == "fa" ? "EN" : "FA";

    static readonly Dictionary<string, Dictionary<string, string>> _t = new()
    {
        ["en"] = new()
        {
            ["app_subtitle"] = "Private relay for everyday browsing",
            ["settings"] = "Settings",
            ["start"] = "Connect",
            ["stop"] = "Disconnect",
            ["connecting"] = "Connecting...",
            ["connected"] = "Connected",
            ["disconnected"] = "Disconnected",
            ["connection_failed"] = "Connection failed",
            ["health"] = "Health",
            ["health_good"] = "Stable",
            ["health_unstable"] = "Unstable",
            ["health_down"] = "Offline",
            ["last_check"] = "Last check",
            ["not_checked"] = "Not checked yet",
            ["checked_now"] = "Checked now",
            ["checked_seconds"] = "Checked {0}s ago",
            ["checked_minutes"] = "Checked {0}m ago",
            ["latency"] = "Latency",
            ["success_rate"] = "Success rate",
            ["active_endpoints"] = "Endpoints",
            ["active_endpoint"] = "Active endpoint",
            ["requests_per_sec"] = "Requests/sec",
            ["diagnostics"] = "Diagnostics",
            ["diagnostics_idle"] = "Start the connection to run diagnostics.",
            ["diag_proxy_reachable"] = "Local proxy is reachable",
            ["diag_proxy_unreachable"] = "Local proxy is not reachable",
            ["cert"] = "Certificate",
            ["cert_trusted"] = "Trusted",
            ["cert_not_trusted"] = "Not trusted",
            ["cert_missing"] = "Missing",
            ["proxy"] = "Proxy",
            ["proxy_on"] = "On",
            ["proxy_off"] = "Off",
            ["download"] = "Download",
            ["upload"] = "Upload",
            ["requests"] = "Requests",
            ["uptime"] = "Uptime",
            ["conns"] = "Connections",
            ["since_start"] = "Since start",
            ["activity"] = "Activity",
            ["copy"] = "Copy",
            ["export"] = "Export",
            ["clear"] = "Clear",
            ["mode"] = "Mode",
            ["front_domain"] = "Front domain (SNI)",
            ["custom_sni"] = "Custom SNI override",
            ["worker_host"] = "Worker host",
            ["auth_key"] = "Auth key",
            ["listen_host"] = "Listen host",
            ["port"] = "Port",
            ["network_tuning"] = "Network tuning",
            ["fragment"] = "Fragment (B)",
            ["chunk"] = "Chunk (B)",
            ["parallel"] = "Parallel",
            ["use_chunked"] = "Use chunked / parallel downloads",
            ["enable_http2"] = "Enable HTTP/2",
            ["verify_ssl"] = "Verify upstream SSL",
            ["install_cert_user"] = "Install Certificate (User)",
            ["install_cert_sys"] = "Install Certificate (System)",
            ["toggle_proxy"] = "Toggle Windows Proxy",
            ["done"] = "Done",
            ["language"] = "Language",
            ["deployment_ids"] = "Deployment IDs",
            ["add_deployment"] = "+ Add Deployment ID",
            ["remove_deployment"] = "Remove Deployment ID",
            ["presets"] = "Connection presets",
            ["preset_stealth"] = "Slow but stealthy",
            ["preset_balanced"] = "Balanced",
            ["preset_speed"] = "Fast",
            ["preset_auto"] = "Auto",
            ["preset_active"] = "Active",
            ["please_wait"] = "Please wait...",
            ["setting_up"] = "Setting things up...",
            ["preparing_cert"] = "Preparing certificate...",
        },
        ["fa"] = new()
        {
            ["app_subtitle"] = "رله خصوصی برای مرور روزمره",
            ["settings"] = "تنظیمات",
            ["start"] = "اتصال",
            ["stop"] = "قطع اتصال",
            ["connecting"] = "در حال اتصال...",
            ["connected"] = "متصل",
            ["disconnected"] = "قطع",
            ["connection_failed"] = "اتصال ناموفق بود",
            ["health"] = "وضعیت",
            ["health_good"] = "پایدار",
            ["health_unstable"] = "ناپایدار",
            ["health_down"] = "آفلاین",
            ["last_check"] = "آخرین بررسی",
            ["not_checked"] = "هنوز بررسی نشده",
            ["checked_now"] = "همین حالا بررسی شد",
            ["checked_seconds"] = "{0} ثانیه پیش بررسی شد",
            ["checked_minutes"] = "{0} دقیقه پیش بررسی شد",
            ["latency"] = "تاخیر",
            ["success_rate"] = "نرخ موفقیت",
            ["active_endpoints"] = "نقاط اتصال",
            ["active_endpoint"] = "نقطه فعال",
            ["requests_per_sec"] = "درخواست در ثانیه",
            ["diagnostics"] = "عیب‌یابی",
            ["diagnostics_idle"] = "برای اجرای عیب‌یابی اتصال را شروع کنید.",
            ["diag_proxy_reachable"] = "پروکسی محلی در دسترس است",
            ["diag_proxy_unreachable"] = "پروکسی محلی در دسترس نیست",
            ["cert"] = "گواهی",
            ["cert_trusted"] = "مورد اعتماد",
            ["cert_not_trusted"] = "مورد اعتماد نیست",
            ["cert_missing"] = "موجود نیست",
            ["proxy"] = "پروکسی",
            ["proxy_on"] = "روشن",
            ["proxy_off"] = "خاموش",
            ["download"] = "دانلود",
            ["upload"] = "آپلود",
            ["requests"] = "درخواست‌ها",
            ["uptime"] = "زمان فعالیت",
            ["conns"] = "اتصالات",
            ["since_start"] = "از زمان شروع",
            ["activity"] = "فعالیت",
            ["copy"] = "کپی",
            ["export"] = "خروجی",
            ["clear"] = "پاک کردن",
            ["mode"] = "حالت",
            ["front_domain"] = "دامنه پیش‌رو (SNI)",
            ["custom_sni"] = "SNI سفارشی",
            ["worker_host"] = "میزبان Worker",
            ["auth_key"] = "کلید احراز هویت",
            ["listen_host"] = "آدرس گوش دادن",
            ["port"] = "پورت",
            ["network_tuning"] = "تنظیمات شبکه",
            ["fragment"] = "اندازه قطعه (B)",
            ["chunk"] = "اندازه بسته (B)",
            ["parallel"] = "همزمانی",
            ["use_chunked"] = "استفاده از دانلود قطعه‌ای / موازی",
            ["enable_http2"] = "فعال‌سازی HTTP/2",
            ["verify_ssl"] = "بررسی SSL سرور",
            ["install_cert_user"] = "نصب گواهی (کاربر)",
            ["install_cert_sys"] = "نصب گواهی (سیستم)",
            ["toggle_proxy"] = "روشن/خاموش کردن پروکسی ویندوز",
            ["done"] = "تمام",
            ["language"] = "زبان",
            ["deployment_ids"] = "شناسه‌های Deployment",
            ["add_deployment"] = "+ افزودن شناسه Deployment",
            ["remove_deployment"] = "حذف شناسه Deployment",
            ["presets"] = "پیش‌تنظیم‌های اتصال",
            ["preset_stealth"] = "کند ولی مخفی‌تر",
            ["preset_balanced"] = "متعادل",
            ["preset_speed"] = "سریع",
            ["preset_auto"] = "خودکار",
            ["preset_active"] = "فعال",
            ["please_wait"] = "لطفا صبر کنید...",
            ["setting_up"] = "در حال راه‌اندازی...",
            ["preparing_cert"] = "آماده‌سازی گواهی...",
        }
    };

    public string this[string key]
    {
        get
        {
            if (_t.TryGetValue(_lang, out var dict) && dict.TryGetValue(key, out var v)) return v;
            if (_t["en"].TryGetValue(key, out var en)) return en;
            return key;
        }
    }

    public void Toggle() => Lang = _lang == "en" ? "fa" : "en";
}
