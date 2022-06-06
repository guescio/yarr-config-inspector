# YARR configuration inspector
*YARR configuration inspector* is a project developed to check the content of YARR configuration files.

# Setup

## Dependencies
The YARR configuration inspector depends on four python packages, which are listed in `requirements.txt`. These are:
- [streamlit](https://docs.streamlit.io/)
- [json](https://docs.python.org/3/library/json.html)
- [numpy](https://numpy.org/)
- [matplotlib](https://matplotlib.org/)

These can be installed by running:
```
pip install -r requirements.txt
```

# Use
The YARR configuration inspector has a grafic user interface that uses the [streamlit](https://docs.streamlit.io/) Python library.

## Graphic User Interface
The tool can be launched by running the command:
```
streamlit run app.py
```
This will open a browser page on `localhost:8501`.


## Online GUI
The tool can be made available online. This has some practical advantages.
- The tool can be accessed from any computer, with some configurable restrictions:
  - restrict the access to a limited set of IPs;
  - use password protection.
- There is no need to run the YARR configuration inspector locally.


### Setup
In order to put the tool online, a host running [Docker](https://docs.docker.com/) is required.

The configuration of the online tool is based on [reverse-proxy](https://github.com/guescio/reverse-proxy/).

Once the reverse proxy is up and running, edit the `.env` file and provide the `HOSTNAME`:
```
HOST = "HOSTNAME"
```

If you wish to apply password protection or restrict the range of allowed IPs, make sure that in `docker-compose.yml` the `allowed-ips@docker` and `auth@docker` Traefik middlewares are used. These are used in the default configuration. The authentication credentials and the allowed IPs are those set in the [reverse-proxy](https://github.com/guescio/reverse-proxy/) configuration.

Now get the tool up and running by using the command:
```
docker-compose up -d
```

That's it. Open `HOSTNAME/yarr` in a browser to use the YARR configuration inspector.


# Documentation

- https://docs.streamlit.io/
- https://docs.docker.com/
- https://doc.traefik.io/traefik/
- https://doc.traefik.io/traefik/providers/docker/
