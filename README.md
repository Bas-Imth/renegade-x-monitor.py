# rxConfigSetter  
Usage:  

Set a Windows task to run this program at startup with a small delay, never exit the script, run w.e or not someone is logged in, highest permissions and the likes.
Run a batch file with this inside:``"[location of python]" "[location of script]"``.

Install these **pip** requirements:  
requests  
psutil  
  
<br>
  
Script will check the status of the service every second, and if the service is not running, send a message through the webhook and wait 10 seconds before checking the service again.  
The delay is to ensure you don't spam the channel.  
If the service is stopped (remember, a crashed server = exited), it'll wait 10 seconds before checking again and don't send a notification through.