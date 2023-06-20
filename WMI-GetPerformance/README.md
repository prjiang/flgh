## Real-time to get remote PC performance system using WMI.

### 本地端

使用 python 進行 WMI 的連線與後續操作，因此須於本地端安裝 python 與其相關套件。

* 安裝 python ，並將其新增至環境變數
    [Python: https://www.python.org/](https://www.python.org/)
  
  

* wmi、matplotlib 不是 Python 的標準套件，因此需要另外安裝
  
  ```
  pip install wmi
  ```
  
  ```
  pip install matplotlib
  ```

---

### 本地端 與 遠端電腦

為了確保 WMI 連線遠端電腦的順利進行，因此建議 本地端 與 遠端電腦 上的 WMI 和 WinRM 服務皆啟用。

* 開啟 WMI
  
  ```
  net start winmgmt
  ```
  
  * 若遇到以下問題，需要使防火牆允許WMI
    
    > the RPC server is unavailable
    
    ```
    Enable-NetFirewallRule -DisplayGroup "Windows Management Instrumentation (WMI)"
    ```
  
  * 若遇到以下問題，禁用UAC遠程限制
    
    > the user name or password is incorrect
    
    ```
    Set-ItemProperty -Path "HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System" -Name "LocalAccountTokenFilterPolicy" -Value 1
    ```
  
  * [Reference: https://www.configserverfirewall.com/windows-10/the-rpc-server-is-unavailable/](https://www.configserverfirewall.com/windows-10/the-rpc-server-is-unavailable/)
    
    

* 開啟 WinRM
  
  ```
  winrm quickconfig
  ```
