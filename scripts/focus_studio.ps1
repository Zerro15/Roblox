$ErrorActionPreference = "Stop"

Add-Type @"
using System;
using System.Runtime.InteropServices;
public static class Win32Focus {
    [DllImport("user32.dll")]
    public static extern bool SetForegroundWindow(IntPtr hWnd);
    [DllImport("user32.dll")]
    public static extern bool ShowWindowAsync(IntPtr hWnd, int nCmdShow);
}
"@

$processes = Get-Process -Name RobloxStudioBeta -ErrorAction SilentlyContinue
if (-not $processes) {
	Write-Output "No RobloxStudioBeta process found."
	exit 0
}

$shell = New-Object -ComObject WScript.Shell

foreach ($proc in $processes) {
	Write-Output ("Process: {0} Id={1} MainWindowTitle={2}" -f $proc.ProcessName, $proc.Id, $proc.MainWindowTitle)
	if ($proc.MainWindowHandle -ne 0) {
		[Win32Focus]::ShowWindowAsync($proc.MainWindowHandle, 9) | Out-Null
		Start-Sleep -Milliseconds 400
		try {
			$shell.AppActivate($proc.Id) | Out-Null
		} catch {
			Write-Output ("AppActivate failed for process id {0}" -f $proc.Id)
		}
		Start-Sleep -Milliseconds 700
		[Win32Focus]::SetForegroundWindow($proc.MainWindowHandle) | Out-Null
		Start-Sleep -Seconds 1
	}
}
