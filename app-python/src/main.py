import time
import os
import sys
import logging
import yaml
import requests
from prometheus_client import start_http_server, Gauge

# Set up basic logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_url_response_data(url):
    """
    get_url_response_data function : send GET request to url, and return the response and its status.

    Parameters
    ----------
    url : str
        URL that will be requested.

    Returns
    -------
    dict
        The response content in YAML format.
    int
        The response code.
    bool
        Whether the response is OK or not.
    """
    try:
        # Send GET request to the specified URL with a timeout of 10 seconds
        response = requests.get(url, timeout=10)
        # Raise an HTTPError if the HTTP request returned an unsuccessful status code
        response.raise_for_status()
        # Decode the response content and load it as YAML
        content = response.content.decode("utf-8")
        yaml_content = yaml.safe_load(content)
        # Return the parsed YAML content, response status code, and a flag indicating success
        return yaml_content, response.status_code, response.ok
    except requests.exceptions.RequestException as error:
        # Log an error message if the request failed
        logging.error("HTTP request failed: %s", error)
        return None, None, False

def exporter(dockerhub_organization, metric_data):
    """
    exporter function : generates Gauge metric data from remote DockerHub URL.

    Parameters
    ----------
    dockerhub_organization : str
        DockerHub organization name.
    metric_data : class
        Gauge module from prometheus_client (https://prometheus.github.io/client_python/instrumenting/gauge/)
    """

    # Construct the DockerHub API URL
    url = f"https://hub.docker.com/v2/repositories/{dockerhub_organization}/?page_size=25&page=1"

    sleep_period = 3 # Time interval between each metric collection in seconds
    while True:
        # Sleep for the specified period
        time.sleep(sleep_period)

        # Send GET request to DockerHub
        yaml_data, response_code, is_ok = get_url_response_data(url)
        if not is_ok:
            # If the request failed, skip to the next iteration
            continue

        try:
            if yaml_data and yaml_data.get('count') > 0:
                # Log successful retrieval of metrics
                logging.info("Successfully retrieved metrics from DockerHub with response code %s", response_code)

                # Iterate through the results and update the Gauge metric
                for data in yaml_data['results']:
                    metric_data.labels(image=data['name'], organization=data['namespace']).set(data['pull_count'])
            else:
                # Log an error if the organization is empty or does not exist
                logging.error("The DOCKERHUB ORGANIZATION %s is empty or does not exist.", dockerhub_organization)
        except AttributeError as invalid_data:
            # Log any exceptions that occur while processing the response
            logging.error("Host responed but data isn't valid, get error while process the reponse %s", {invalid_data})

def main():
    # Get environment variables for DockerHub organization and application port
    dockerhub_organization= os.getenv('DOCKERHUB_ORGANIZATION')
    app_port= os.getenv('app_port', '2113')

    # If dockerhub_organization is not set or empty, exit the program
    if not dockerhub_organization:
        sys.exit("dockerhub_organization must exist")

    # Start the HTTP server to expose the metrics
    start_http_server(int(app_port))

    # Create a Gauge metric for Docker image pulls
    metric_data = Gauge('docker_image_pulls', 'The total number of Docker image pulls', ['image', 'organization'])

    # Start the exporter to collect and expose metrics
    exporter(dockerhub_organization, metric_data)

if __name__ == '__main__':
    # Run the main function if the script is executed directly
    main()
