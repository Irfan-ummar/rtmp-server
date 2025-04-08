# Camera Setup Guide

This guide explains how to set up your IP cameras to work with the CCTV Camera Manager using RTMP streaming.

## RTMP Configuration

Most modern IP cameras support RTMP streaming. You'll need to configure the following settings in your camera's web interface:

### Required Settings

1. **RTMP Server Settings**:
   - Protocol Type: Standard
   - Stream Type: Main Stream
   - Port: 1935 (default RTMP port)
   - App Name: Usually 'live' or similar
   - Stream ID: A unique identifier for the stream

### Example Configuration

Here's an example of how to configure your camera's RTMP settings:

1. Access your camera's web interface
2. Navigate to the streaming or RTMP configuration section
3. Configure the following:
   ```
   Protocol Type: Standard
   Stream Type: Main Stream
   Server: [Your RTMP server IP]
   Port: 1935
   App Name: live
   Stream ID: camera1
   ```

### Adding to CCTV Manager

Once your camera is configured for RTMP streaming, add it to the CCTV Manager:

1. Click "Add Camera" in the dashboard
2. Fill in the details:
   - Name: Give your camera a descriptive name
   - IP Address: Your camera's IP address
   - RTMP Port: The port configured in your camera (usually 1935)
   - App Name: The application name configured in your camera
   - Stream ID: The stream ID configured in your camera

The system will automatically construct the RTMP URL in the format:
```
rtmp://{camera_ip}:{rtmp_port}/{app_name}/{stream_id}
```

## Troubleshooting

### Common Issues

1. **Stream Not Starting**
   - Verify the camera's RTMP settings are correct
   - Check if the camera's IP is accessible from the server
   - Ensure the RTMP port (1935) is not blocked by firewalls

2. **Poor Stream Quality**
   - Check the camera's video settings (bitrate, resolution)
   - Verify network bandwidth between camera and server
   - Consider lowering the stream quality if network bandwidth is limited

3. **Connection Refused**
   - Verify the camera's RTMP service is enabled
   - Check if authentication is required
   - Ensure the RTMP port is open on the camera

### Testing RTMP Stream

You can test your camera's RTMP stream using VLC media player:

1. Open VLC
2. Go to Media > Open Network Stream
3. Enter your RTMP URL:
   ```
   rtmp://{camera_ip}:1935/live/camera1
   ```
4. Click Play

If VLC can play the stream but the CCTV Manager cannot, the issue might be with the network configuration or firewall settings.

## Camera Compatibility

The following camera brands have been tested and confirmed working:

- Hikvision (with RTMP support)
- Dahua (with RTMP support)
- Axis (with RTMP support)
- Uniview (with RTMP support)

For other camera brands, check if they support RTMP streaming in their documentation. 