import requests
import os

def generate_3d_model(image_path, server_url="https://imageto3d.bloomfinity.net"):
    """
    Send an image to the server and receive a 3D model in response.

    :param image_path: Path to the input image file
    :param server_url: URL of the server (default: http://localhost:8000)
    :return: Path to the saved GLB file
    """
    # Prepare the file for upload
    with open(image_path, "rb") as image_file:
        files = {"file": (os.path.basename(image_path), image_file, "image/jpeg")}
        
        # Send POST request to the server
        response = requests.post(f"{server_url}/generate", files=files)
    
    # Check if the request was successful
    if response.status_code == 200:
        # Get the filename from the Content-Disposition header
        content_disposition = response.headers.get("Content-Disposition")
        filename = "model.glb"  # Default filename
        if content_disposition:
            filename = content_disposition.split("filename=")[1].strip('"')
        
        # Save the GLB file
        output_path = os.path.join(os.getcwd(), filename)
        with open(output_path, "wb") as f:
            f.write(response.content)
        
        print(f"3D model saved as: {output_path}")
        return output_path
    else:
        print(f"Error: Server returned status code {response.status_code}")
        print(response.text)
        return None

if __name__ == "__main__":
    image_path = input("Enter the path to your image file: ")
    generate_3d_model(image_path)