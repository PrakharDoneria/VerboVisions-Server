# Flask Image Generator API

This project is a Flask-based web service for generating and serving images using an AI art generator API. It provides endpoints to generate images based on user prompts and serve them to the client.

## Features

- Generate images from text prompts using an AI art generator.
- Serve generated images to the client.
- Automatically delete images after 2 minutes to save storage space.
- CORS support for specific origins.

## Prerequisites

- Python 3.7+
- Flask
- Pillow
- Requests
- Flask-CORS

## Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/yourusername/flask-image-generator.git
    cd flask-image-generator
    ```

2. **Create and activate a virtual environment:**

    ```bash
    python -m venv venv
    source venv/bin/activate
    ```

3. **Install the dependencies:**

    ```bash
    pip install Flask Pillow requests Flask-CORS
    ```

## Usage

1. **Run the Flask application:**

    ```bash
    python main.py
    ```

2. **Access the server:**

    Open your web browser and navigate to `http://localhost:5000`.

## API Endpoints

### Home

- **URL:** `/`
- **Method:** `GET`
- **Description:** Check if the server is alive.
- **Response:**
    ```json
    {
        "status": "Server is alive"
    }
    ```

### Generate Image

- **URL:** `/generate`
- **Method:** `GET`
- **Description:** Generate an image from a text prompt.
- **Query Parameter:** `p` (text prompt)
- **Response:**
    - **Success:** Returns the generated image in base64 format.
        ```json
        {
            "img": "<base64_encoded_image>"
        }
        ```
    - **Error:** Returns an error message.
        ```json
        {
            "error": "Prompt is required"
        }
        ```

### Generate Image for Premium Users

- **URL:** `/image`
- **Method:** `GET`
- **Description:** Generate and save an image from a text prompt. The image will be available for 2 minutes.
- **Query Parameter:** `p` (text prompt)
- **Response:**
    - **Success:** Returns the URL of the generated image.
        ```json
        {
            "url": "/images/<filename>.png"
        }
        ```
    - **Error:** Returns an error message.
        ```json
        {
            "error": "No prompt provided"
        }
        ```

### Serve Image

- **URL:** `/images/<filename>`
- **Method:** `GET`
- **Description:** Serve the generated image.
- **Response:** Returns the image file.


## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [Flask](https://flask.palletsprojects.com/)
- [Pillow](https://python-pillow.org/)
- [Requests](https://docs.python-requests.org/en/master/)
- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/)
- [MagicStudio AI Art Generator]