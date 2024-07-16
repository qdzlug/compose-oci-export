# Docker Image Saver

This project provides a Docker image that takes a Docker Compose file as input, pulls the images defined in the file, and saves them to the local directory in zip format. This allows you to easily move these images to another host.

## Prerequisites

- Docker must be installed on the host machine where you run this container.
- Python must be installed to run the conversion script (only for building the Docker image).

## Build the Docker Image

To build the Docker image for `amd64`, use the following command:

```sh
docker build --platform linux/amd64 -t image-saver .
```

## Usage

### For Linux and macOS Users

1. Ensure your `docker-compose.yml` file is in the current directory.

2. Run the Docker container with the following command:

   ```sh
   docker run --rm --platform linux/amd64 -v /var/run/docker.sock:/var/run/docker.sock -v $(pwd):/data image-saver docker-compose.yml
   ```

   This command will mount the Docker socket and the current directory to the container, allowing it to pull images and save them as zip files in the current directory.

### For Docker Desktop on Windows Users

1. Ensure your `docker-compose.yml` file is in the current directory.

2. Run the Docker container using the following command in PowerShell or Command Prompt:

   ```sh
   docker run --rm --platform linux/amd64 -v //var/run/docker.sock:/var/run/docker.sock -v %cd%:/data image-saver docker-compose.yml
   ```

   This command will mount the Docker socket and the current directory to the container, allowing it to pull images and save them as zip files in the current directory. Note the use of `//var/run/docker.sock` and `%cd%` for compatibility with Windows paths.

## How It Works

1. The container starts and the script `save_images.py` is executed.
2. The script reads the provided Docker Compose file (`docker-compose.yml`).
3. It pulls or builds the Docker images specified in the Compose file.
4. Each image is tagged with its name and tag (or `latest` if no tag is specified).
5. Each image is saved as a tar file and then converted to a zip file in the current directory.

## Loading Images on a New System

To load the images on a new system, follow these steps:

1. Transfer the zip files containing the Docker images to the new system.
2. Extract the tar files from the zip files.
3. Load each tar file into Docker using the following command:

   ```sh
   docker load -i <image-file>.tar
   ```

   For example, to load `app.tar` and `db.tar`, use:

   ```sh
   docker load -i app.tar
   docker load -i db.tar
   ```

4. Verify that the images have been loaded correctly by running `docker images`.

## Adding an Image Key to the Compose File

If your Docker Compose file does not already use the `image` key for each service, you need to add it to ensure that the script works correctly. Here is how you can modify your Compose file:

1. Open your `docker-compose.yml` file.
2. Add an `image` key to each service with the appropriate image name and tag. For example:

   ```yaml
   version: '3'
   services:
     app:
       build: .
       image: myapp:latest
       # Other configuration options
     db:
       build: ./db
       image: mydb:5.7
       # Other configuration options
   ```

   Ensure that each service has an `image` key specifying the image name and tag you want to use. The `build` key specifies the build context, which is used when you are building the image rather than pulling it from a registry.

   **Note:** The script will throw an error if a service has a `build` key but no `image` key. Ensure all services with `build` have an associated `image` key.

## Files

- `Dockerfile`: The Dockerfile used to build the image.
- `save_images.py`: The script that pulls and saves the Docker images.
- `README.md`: This readme file.

## Example

If your `docker-compose.yml` file contains:

```yaml
version: '3'
services:
  app:
    build: .
    image: myapp:latest
  db:
    build: ./db
    image: mydb:5.7
```

Running the Docker container as described in the Usage section will result in `myapp:latest` and `mydb:5.7` being saved as `app.zip` and `db.zip` respectively in the current directory. The images will retain their names and tags when imported.

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.