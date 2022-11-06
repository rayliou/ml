### How to Enable aptX, aptX-HD, and AAC Bluetooth Codecs on Ubuntu 24.04 with PipeWire

This guide will help you enable the aptX, aptX-HD, and AAC Bluetooth codecs on Ubuntu 24.04, where PipeWire is the default audio system. We will utilize the `pipewire-extra-bt-codecs` PPA and configure PipeWire to support these codecs.

### Step 1: Add the PPA for Extra Bluetooth Codecs

To support additional Bluetooth codecs, add the `pipewire-extra-bt-codecs` PPA:

```bash
sudo add-apt-repository ppa:aglasgall/pipewire-extra-bt-codecs
```

Update the package list and reinstall the necessary PipeWire components:

```bash
sudo apt update
sudo apt install --reinstall -y pipewire pipewire-audio-client-libraries libspa-0.2-bluetooth
```

### Step 2: Configure PipeWire for Bluetooth Codecs

PipeWire's configuration for Bluetooth codecs is located in the `/usr/share/pipewire/bluetooth.conf` file. To enable aptX, aptX-HD, and AAC codecs, follow these steps:

1. **Edit the Bluetooth configuration file**:

   Open the configuration file with `vim`:

   ```bash
   sudo vim /usr/share/pipewire/bluetooth.conf
   ```

2. **Enable aptX, aptX-HD, and AAC codecs**:

   In the configuration file, ensure that the following codecs are enabled by verifying or adding the appropriate lines:

   ```ini
   bluez.codecs = [
       "sbc"
       "aac"
       "aptx"
       "aptx_hd"
   ]
   ```

   This will enable the standard SBC codec along with aptX, aptX-HD, and Apple's AAC codec.

3. **Save and exit**:

   - Press `Esc` to enter command mode.
   - Type `:wq` and press `Enter` to save and exit the file.

### Step 3: Restart PipeWire Services

After modifying the configuration, restart the PipeWire services to apply the changes:

```bash
systemctl --user restart pipewire pipewire-pulse
```

### Step 4: Pair Your Bluetooth Device

Once the services are restarted, re-pair your Bluetooth device. The system should now support the aptX, aptX-HD, and AAC codecs, provided your Bluetooth device also supports them.

### Step 5: Verify the Codec in Use

To check which codec is being used by your Bluetooth device, use the following command:

```bash
pw-cli info all | grep -B8 codec
```

This command will display the codec information being used by your Bluetooth device.

By following this guide, you will ensure that your Ubuntu 24.04 system supports aptX, aptX-HD, and AAC codecs with PipeWire as the default audio system.
## Ref
The pipewire-extra-bt-codecs PPA provides support for several additional Bluetooth audio codecs that are not included in the default PipeWire installation on Ubuntu. These include:

- aptX
- aptX-HD
- AAC (Apple's Advanced Audio Codec)
- FastStream
- LDAC (Sony's high-quality audio codec)
- SBC-XQ (an enhanced version of the standard SBC codec)
