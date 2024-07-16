#!/usr/bin/env python3

import os
import yaml
import subprocess
import sys
import zipfile

def pull_and_save_images(compose_file_path):
    # Load the Docker Compose file
    with open(compose_file_path, 'r') as file:
        compose_data = yaml.safe_load(file)

    # Get the services and their images
    services = compose_data.get('services', {})
    for service_name, service_data in services.items():
        image = service_data.get('image')
        build = service_data.get('build')

        if build and not image:
            raise ValueError(f"Service '{service_name}' has a 'build' key but no 'image' key. Please provide an 'image' key.")
        
        if image:
            if build:
                # Build the image
                subprocess.run(['docker-compose', 'build', service_name], check=True)
            else:
                # Pull the image
                subprocess.run(['docker', 'pull', image], check=True)
            
            # Tag the image with its name and tag
            image_name_tag = image.split(':')
            if len(image_name_tag) == 2:
                image_name, image_tag = image_name_tag
            else:
                image_name = image_name_tag[0]
                image_tag = 'latest'

            tagged_image = f"{image_name}:{image_tag}"

            # Save the image to a tar file
            tar_file = f"{service_name}.tar"
            subprocess.run(['docker', 'tag', image, tagged_image], check=True)
            subprocess.run(['docker', 'save', '-o', tar_file, tagged_image], check=True)
            print(f"Saved {image} to {tar_file}")

            # Convert the tar file to a zip file
            zip_file = f"{service_name}.zip"
            with zipfile.ZipFile(zip_file, 'w', zipfile.ZIP_DEFLATED) as zf:
                zf.write(tar_file, os.path.basename(tar_file))
            print(f"Converted {tar_file} to {zip_file}")
            os.remove(tar_file)  # Remove the tar file if you only need the zip file

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python save_images.py <docker-compose.yml>")
        sys.exit(1)
    
    compose_file_path = sys.argv[1]
    if not os.path.isfile(compose_file_path):
        print(f"File not found: {compose_file_path}")
        sys.exit(1)

    pull_and_save_images(compose_file_path)
