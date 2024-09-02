import subprocess

class WifiManager:
    def __init__(self):
        pass

    def get_available_wifi(self):
        """Get a list of available Wi-Fi networks."""
        command = ["netsh", "wlan", "show", "networks"]
        result = subprocess.run(command, capture_output=True, text=True)
        status = re.split(r"\n\n", result.stdout)[1:]
        content = [
                    {cont[0].strip(): cont[1].strip() 
                        for line in lines if len(cont := line.split(':')) == 2
                    } 
                   for wifi in status if (lines := wifi.split('\n'))[0]]
        return content

    def is_connected(self, ssid):
        """Check if the system is connected to the specified Wi-Fi network."""
        command = ["netsh", "wlan", "show", "interfaces"]
        result = subprocess.run(command, capture_output=True, text=True)
        if ssid in result.stdout:
            return True
        return False

    def connect_to_saved_wifi(self, ssid):
        """Connect to a saved Wi-Fi network."""
        command = ["netsh", "wlan", "connect", f"name={ssid}"]
        result = subprocess.run(command, capture_output=True, text=True)
        if "Connection request was completed successfully" in result.stdout:
            return True
        return False

    def connect_to_wifi_with_password(self, ssid, password):
        """Connect to a Wi-Fi network with a password."""
        profile_name = ssid
        profile_xml = f"""
        <WLANProfile xmlns="http://www.microsoft.com/networking/WLAN/profile/v1">
            <name>{profile_name}</name>
            <SSIDConfig>
                <SSID>
                    <name>{ssid}</name>
                </SSID>
            </SSIDConfig>
            <connectionType>ESS</connectionType>
            <connectionMode>auto</connectionMode>
            <MSM>
                <security>
                    <authEncryption>
                        <authentication>WPA2PSK</authentication>
                        <encryption>AES</encryption>
                        <useOneX>false</useOneX>
                    </authEncryption>
                    <sharedKey>
                        <keyType>passPhrase</keyType>
                        <protected>false</protected>
                        <keyMaterial>{password}</keyMaterial>
                    </sharedKey>
                </security>
            </MSM>
        </WLANProfile>
        """
        with open(f"{profile_name}.xml", 'w') as f:
            f.write(profile_xml)
        
        command = ["netsh", "wlan", "add", f"profile={profile_name}.xml"]
        result = subprocess.run(command, capture_output=True, text=True)
        if "successfully added" not in result.stdout:
            return False

        return self.connect_to_saved_wifi(ssid)