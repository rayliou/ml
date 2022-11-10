
# How to use
- http://IP:8000/
# Setup JupyterHub
## Prerequest
1. Install **/usr/local/node-v18.12.1/** 
1. Modify /etc/profile
```
PATH="/usr/local/python-3.7.13/bin:$PATH"
PATH="/usr/local/node-v18.12.1/bin:$PATH"
PATH="/usr/local/cuda-11.4/bin/:$PATH"
LD_LIBRARY_PATH="/usr/local/cuda-11.4/lib64/:$LD_LIBRARY_PATH"
```

## install
https://jupyterhub.readthedocs.io/en/1.2.0/quickstart.html
```
python3 -m pip install jupyterhub
npm install -g configurable-http-proxy
python3 -m pip install notebook  # needed if running the notebook servers locally
```
## Systemd configure
- [Install JupyterHub Systemd](https://jupyterhub.readthedocs.io/en/1.2.0/installation-guide-hard.html#setup-systemd-service)
```
/home/python-3.7.13/bin/jupyterhub -f /opt/jupyterhub/etc/jupyterhub_config.py
sudo mv jupyterhub_config.py /opt/jupyterhub/etc/
sudo vim /opt/jupyterhub/etc/systemd/jupyterhub.service
sudo ln -s /opt/jupyterhub/etc/systemd/jupyterhub.service /etc/systemd/system/jupyterhub.service
sudo systemctl daemon-reload
sudo systemctl enable jupyterhub.service
sudo systemctl start jupyterhub.service
sudo systemctl status jupyterhub.service
sudo journalctl -u jupyterhub.service
sudo systemctl  restart jupyterhub.service 
sudo systemctl daemon-reload 
sudo systemctl  restart jupyterhub.service 
```
Make sure the following content has been add in the file /opt/jupyterhub/etc/jupyterhub_config.py
```
c = get_config()  # noqa
c.Authenticator.allowed_users = {'user1', 'user2'}
c.Authenticator.admin_users = {'user3','user4' }
c.JupyterHub.proxy_cmd = ["/usr/local/node-v18.12.1/bin/configurable-http-proxy",]
```


